# augur-actions

GitHub Actions for [orb](https://github.com/augur-ai/augur-jobs) (procedure execution via Claude Code) and Augur Release Monitor (API contract drift detection from your CI).

## Actions

### `orb-procedure-run`

Runs an orb procedure end-to-end:
1. Installs orb and Claude Code CLI
2. Authenticates with the orb registry
3. Starts the orb gateway (for Live Log event relay)
4. Builds the procedure exec prompt
5. Runs `claude -p` with MCP tools wired in
6. Prints a live run URL so you can follow along in the UI

### `upstream-drift-run`

Runs an Augur Release Monitor "compare" drift run against two refs in your CI
and reports the drift items back through the delegated-callback path.

1. Mints a delegated drift run on the Augur backend (`POST /release-monitoring/runs`)
2. Installs `oasdiff` and computes the diff between two spec files you check
   out yourself in your workflow
3. Translates oasdiff output into Augur's `DriftItem` shape and POSTs it to
   the callback URL with the one-time token

See [`actions/upstream-drift-run/`](./actions/upstream-drift-run/action.yml)
for inputs/outputs and the CONSUMPTION_GUIDE section below for a full
workflow example.

## Quick Start

```yaml
jobs:
  run-procedure:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      ORB_API_TOKEN: ${{ secrets.ORB_API_TOKEN }}
    steps:
      - uses: actions/checkout@v4

      - uses: augur-ai/augur-actions/actions/orb-procedure-run@main
        with:
          procedure: my-procedure
          params: |
            repo_path=${{ github.workspace }}
```

See [CONSUMPTION_GUIDE.md](./CONSUMPTION_GUIDE.md) for full configuration options and examples.
