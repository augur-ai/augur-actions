# orb-procedure-run: Consumption Guide

## Setup

### 1. Configure secrets

Add these to your repository (`Settings` → `Secrets and variables` → `Actions`):

| Secret | Required | Description |
|--------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude |
| `ORB_API_TOKEN` | Yes | orb registry API token |
| `ORB_BACKEND_URL` | No | orb backend URL — defaults to `https://app.getaugur.ai` |

### 2. Add a workflow

```yaml
name: Run orb Procedure

on:
  workflow_dispatch:
    inputs:
      procedure:
        description: 'Procedure ID'
        required: true

jobs:
  run:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      ORB_API_TOKEN: ${{ secrets.ORB_API_TOKEN }}
      # ORB_BACKEND_URL: ${{ secrets.ORB_BACKEND_URL }}  # optional, defaults to https://app.getaugur.ai
    steps:
      - uses: actions/checkout@v4

      - uses: augur-ai/augur-actions/actions/orb-procedure-run@main
        with:
          procedure: ${{ github.event.inputs.procedure }}
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `procedure` | Yes | — | Procedure ID to run (e.g. `todo-app-ci`) |
| `params` | No | `''` | Newline-separated `key=value` pairs passed as `--param` flags |
| `model` | No | `claude-sonnet-4-5` | Claude model to use |
| `max_turns` | No | unlimited | Max agentic turns Claude can take |
| `orb_version` | No | `latest` | orb version to install |
| `orb_binary_path` | No | `''` | Path to pre-built binary (for local act testing) |

## Outputs

| Output | Description |
|--------|-------------|
| `session_id` | orb session ID for this run |
| `run_status` | `PASS`, `FAIL`, or `UNKNOWN` from the procedure's final report |

## Passing parameters

```yaml
- uses: augur-ai/augur-actions/actions/orb-procedure-run@main
  with:
    procedure: my-procedure
    params: |
      repo_path=${{ github.workspace }}
      node_version=20
      environment=staging
```

## Checking the result

```yaml
- id: orb
  uses: augur-ai/augur-actions/actions/orb-procedure-run@main
  with:
    procedure: my-procedure

- name: Check result
  if: steps.orb.outputs.run_status == 'FAIL'
  run: echo "Procedure failed" && exit 1
```

## Live Log UI

When `ORB_BACKEND_URL` is set (or left as default), the action prints a clickable link after session bind:

```
📊 Live run: https://your-backend/workflow-run?session_id=<id>
```

Open the link to follow task progress and logs in real time.

## Local testing with act

```bash
# .act.env
ANTHROPIC_API_KEY=sk-...
ORB_API_TOKEN=...
# ORB_BACKEND_URL=https://app.getaugur.ai  # optional override

act workflow_dispatch \
  --env-file .act.env \
  --input procedure=my-procedure \
  --container-architecture linux/arm64 \
  --network host
```

---

# `upstream-drift-run`: Consumption Guide

Use this action to detect API contract drift between two refs of an OpenAPI
spec from your CI and report it to Augur Release Monitor. The diff runs in
your workflow (so we never see your private repo); only drift items + a
one-time callback token cross the wire.

## Setup

### 1. Configure secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `AUGUR_TOKEN`        | Yes | Augur API token (Bearer auth) |
| `AUGUR_ORG_ID`       | Yes | Org id this run reports to |
| `AUGUR_BACKEND_URL`  | No  | Defaults to `https://app.getaugur.ai` |

### 2. Add a workflow

The action expects you to check out **both** refs yourself and place
each spec at:

```
${{ github.workspace }}/.augur/baseline.<spec_path>
${{ github.workspace }}/.augur/target.<spec_path>
```

Where `<spec_path>` matches the `spec_path` input (default `openapi.json`).

Canonical PR-vs-base workflow:

```yaml
name: Augur Drift on PR

on:
  pull_request:
    paths: ['openapi.json']

jobs:
  drift:
    runs-on: ubuntu-latest
    env:
      AUGUR_TOKEN:    ${{ secrets.AUGUR_TOKEN }}
      AUGUR_ORG_ID:   ${{ secrets.AUGUR_ORG_ID }}
      # AUGUR_BACKEND_URL: ${{ secrets.AUGUR_BACKEND_URL }}  # optional

    steps:
      - name: Check out target (PR head)
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          path: target

      - name: Check out baseline (PR base)
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.sha }}
          path: baseline

      - name: Stage specs for the action
        run: |
          mkdir -p .augur
          cp target/openapi.json   .augur/target.openapi.json
          cp baseline/openapi.json .augur/baseline.openapi.json

      - uses: augur-ai/augur-actions/actions/upstream-drift-run@main
        with:
          repo:          ${{ github.repository }}
          target_ref:    ${{ github.event.pull_request.head.sha }}
          target_kind:   commit
          baseline_ref:  ${{ github.event.pull_request.base.sha }}
          baseline_kind: commit
          focus_areas:   rest_api
          spec_path:     openapi.json
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `repo`            | No  | `${{ github.repository }}` | `owner/name` |
| `target_ref`      | Yes | — | Target ref (PR head SHA, release tag, branch) |
| `target_kind`     | No  | `commit` | `branch` / `commit` / `release` / `pr` |
| `baseline_ref`    | Yes | — | Baseline ref the diff is computed *from* |
| `baseline_kind`   | No  | `main` | `branch` / `commit` / `release` / `main` |
| `focus_areas`     | No  | `rest_api` | Comma list: `rest_api,ui,playwright,code` |
| `spec_path`       | No  | `openapi.json` | Path under repo root (relative) |
| `oasdiff_version` | No  | `latest` | oasdiff release tag to install |

## Outputs

| Output | Description |
|--------|-------------|
| `run_id`      | Drift run id created on the Augur backend |
| `run_url`     | Direct link to the run-detail page |
| `items_count` | Number of drift items reported |

## Example: gate the PR on breaking changes

```yaml
- id: drift
  uses: augur-ai/augur-actions/actions/upstream-drift-run@main
  with:
    target_ref:   ${{ github.event.pull_request.head.sha }}
    baseline_ref: ${{ github.event.pull_request.base.sha }}

- name: Comment + fail on breaking
  if: steps.drift.outputs.items_count != '0'
  run: |
    echo "::warning::Drift detected — see ${{ steps.drift.outputs.run_url }}"
```

## How it talks to Augur

1. `POST /api/v1/orgs/$AUGUR_ORG_ID/release-monitoring/runs` with
   `mode=delegated` → returns `id`, `callback_url`, `callback_token`.
2. Run `oasdiff changelog baseline target --format json` and translate
   each change into an Augur `DriftItem` (severity: `error → breaking`,
   `warning → warning`, else `info`).
3. `POST $callback_url` with header `X-Callback-Token: $callback_token`
   and body `{items, final:true}` → backend marks the run `done`.
4. On failure, `POST $callback_url/fail` with the error string → backend
   marks the run `failed` with the message.

The callback token is one-time use and scoped to this single run id; it
can't be replayed.
