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
