# augur-actions

GitHub Actions for running [gitx](https://github.com/augur-ai/augur-jobs) procedures in CI using Claude Code as the execution engine.

## Actions

### `gitx-procedure-run`

Runs a gitx procedure end-to-end:
1. Installs gitx and Claude Code CLI
2. Authenticates with the gitx registry
3. Starts the gitx gateway (for Live Log event relay)
4. Builds the procedure exec prompt
5. Runs `claude -p` with MCP tools wired in
6. Prints a live run URL so you can follow along in the UI

## Quick Start

```yaml
jobs:
  run-procedure:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      GITX_API_TOKEN: ${{ secrets.GITX_API_TOKEN }}
    steps:
      - uses: actions/checkout@v4

      - uses: augur-ai/augur-actions/actions/gitx-procedure-run@main
        with:
          procedure: my-procedure
          params: |
            repo_path=${{ github.workspace }}
```

See [CONSUMPTION_GUIDE.md](./CONSUMPTION_GUIDE.md) for full configuration options and examples.
