# gitx-procedure-run: Consumption Guide

## Setup

### 1. Configure secrets

Add these to your repository (`Settings` → `Secrets and variables` → `Actions`):

| Secret | Required | Description |
|--------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude |
| `GITX_API_TOKEN` | Yes | gitx registry API token |
| `GITX_BACKEND_URL` | No | gitx backend URL — enables Live Log UI and event relay |
| `GITX_ORG_ID` | No | Organization ID — required when `GITX_BACKEND_URL` is set |

### 2. Add a workflow

```yaml
name: Run gitx Procedure

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
      GITX_API_TOKEN: ${{ secrets.GITX_API_TOKEN }}
      GITX_BACKEND_URL: ${{ secrets.GITX_BACKEND_URL }}
      GITX_ORG_ID: ${{ secrets.GITX_ORG_ID }}
    steps:
      - uses: actions/checkout@v4

      - uses: augur-ai/augur-actions/actions/gitx-procedure-run@main
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
| `gitx_version` | No | `latest` | gitx version to install |
| `gitx_binary_path` | No | `''` | Path to pre-built binary (for local act testing) |

## Outputs

| Output | Description |
|--------|-------------|
| `session_id` | gitx session ID for this run |
| `ci_status` | `PASS`, `FAIL`, or `UNKNOWN` from the procedure's final report |

## Passing parameters

```yaml
- uses: augur-ai/augur-actions/actions/gitx-procedure-run@main
  with:
    procedure: my-procedure
    params: |
      repo_path=${{ github.workspace }}
      node_version=20
      environment=staging
```

## Checking the result

```yaml
- id: gitx
  uses: augur-ai/augur-actions/actions/gitx-procedure-run@main
  with:
    procedure: my-procedure

- name: Check result
  if: steps.gitx.outputs.ci_status == 'FAIL'
  run: echo "Procedure failed" && exit 1
```

## Live Log UI

When `GITX_BACKEND_URL` is set, the action prints a clickable link after session bind:

```
📊 Live run: https://your-backend/workflow-run?session_id=<id>
```

Open the link to follow task progress and logs in real time.

## Local testing with act

```bash
# .act.env
ANTHROPIC_API_KEY=sk-...
GITX_API_TOKEN=...
GITX_BACKEND_URL=https://your-backend
GITX_ORG_ID=...

act workflow_dispatch \
  --env-file .act.env \
  --input procedure=my-procedure \
  --var GITX_BINARY_PATH=/path/to/gitx-linux-arm64 \
  --container-architecture linux/arm64 \
  --network host
```
