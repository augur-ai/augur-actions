# augur-actions

GitHub Actions for running [orb](https://github.com/augur-ai/augur-jobs) procedures in CI using Claude Code as the execution engine.

## Actions

### `orb-procedure-run`

Runs an orb procedure end-to-end:
1. Installs orb and Claude Code CLI
2. Authenticates with the orb registry
3. Starts the orb gateway (for Live Log event relay)
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
