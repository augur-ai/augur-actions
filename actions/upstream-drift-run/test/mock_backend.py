"""Tiny stub of Augur's release-monitoring callback API.

Exists only so the action's CI smoke workflow can exercise the full
sequence (mint -> compute diff -> POST items -> /fail on error)
without standing up the real backend. Validates request shapes and
asserts the X-Callback-Token round-trip.

Run with: python mock_backend.py [--port 8000]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


# In-memory state. The smoke workflow expects exactly one run end-to-end.
_RUNS: dict[str, dict] = {}


def _h(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stdout.write("[mock] " + (fmt % args) + "\n")
        sys.stdout.flush()

    def _read_json(self):
        n = int(self.headers.get("content-length", "0"))
        if n == 0:
            return {}
        return json.loads(self.rfile.read(n).decode())

    def _send(self, code: int, body: dict | None = None):
        payload = b"" if body is None else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def do_POST(self):  # noqa: N802 (BaseHTTPRequestHandler API)
        path = urlparse(self.path).path

        # ── Mint a delegated run ────────────────────────────────────
        if path.endswith("/release-monitoring/runs"):
            body = self._read_json()
            if body.get("mode") != "delegated":
                return self._send(400, {"detail": "smoke backend only handles delegated mode"})
            run_id = str(uuid.uuid4())
            raw = secrets.token_urlsafe(32)
            _RUNS[run_id] = {
                "id": run_id,
                "token_hash": _h(raw),
                "consumed": False,
                "items": [],
                "status": "pending",
                "config": body,
            }
            return self._send(
                201,
                {
                    "id": run_id,
                    "items_count": 0,
                    "target_commit_sha": None,
                    "baseline_commit_sha": None,
                    "callback_url": f"http://{self.headers.get('host','localhost')}/api/v1/orgs/test-org/release-monitoring/runs/{run_id}/callback",
                    "callback_token": raw,
                },
            )

        # ── /callback (success) ─────────────────────────────────────
        if path.endswith("/callback"):
            run_id = path.split("/")[-2]
            run = _RUNS.get(run_id)
            if not run:
                return self._send(404, {"detail": "run not found"})
            if run["consumed"]:
                return self._send(403, {"detail": "token already used"})
            tok = self.headers.get("X-Callback-Token", "")
            if _h(tok) != run["token_hash"]:
                return self._send(403, {"detail": "bad token"})
            body = self._read_json()
            run["items"].extend(body.get("items", []))
            if body.get("final"):
                run["consumed"] = True
                run["status"] = "done"
            return self._send(204)

        # ── /callback/fail ─────────────────────────────────────────
        if path.endswith("/callback/fail"):
            run_id = path.split("/")[-3]
            run = _RUNS.get(run_id)
            if not run:
                return self._send(404, {"detail": "run not found"})
            if run["consumed"]:
                return self._send(403, {"detail": "token already used"})
            tok = self.headers.get("X-Callback-Token", "")
            if _h(tok) != run["token_hash"]:
                return self._send(403, {"detail": "bad token"})
            body = self._read_json()
            run["consumed"] = True
            run["status"] = "failed"
            run["error"] = body.get("error", "")
            return self._send(204)

        return self._send(404, {"detail": "no route"})

    def do_GET(self):  # noqa: N802
        # Test-only: dump server state so the smoke workflow can assert.
        if self.path == "/__state":
            return self._send(200, {"runs": list(_RUNS.values())})
        return self._send(404, {"detail": "no route"})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args()
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"[mock] listening on :{args.port}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
