# Release Branch Notification Action

This GitHub Action collects commit information when a release branch is created and sends a notification to the Initos API.

## Features

- Automatically detects release branches
- Collects commit information since the last release tag
- Formats commits in a Markdown table
- Sends notification to Initos API using the [Initos Post Feed](../initos-post-feed) action
- Handles error cases gracefully

## Usage

Add this action to your workflow file:

```yaml
name: Release Branch Notifications

on:
  create:
    branches:
      - "release/**"
  workflow_dispatch:
    inputs:
      branch_name:
        description: "Branch to analyze"
        required: true
        default: "main"
      previous_tag:
        description: "Previous tag to compare against"
        required: false
        default: ""

jobs:
  notify-release-commits:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify release commits
        uses: augur-ai/augur-actions/actions/release-branch-notification@main
        with:
          branch_name: ${{ github.event.inputs.branch_name || github.ref_name }}
          previous_tag: ${{ github.event.inputs.previous_tag || '' }}
          api_url: ${{ secrets.INITOS_API_URL }}
          api_key: ${{ secrets.INITOS_API_KEY }}
          feed_id: ${{ secrets.INITOS_RELEASE_FEED_ID }}
```

## Required Secrets

This action requires the following secrets to be set in your repository:

- `INITOS_API_URL`: The base URL for the Initos API
- `INITOS_API_KEY`: Your Initos API key for authentication
- `INITOS_RELEASE_FEED_ID`: The feed ID to post notifications to

## Inputs

| Input                | Description                               | Required | Default                    |
| -------------------- | ----------------------------------------- | -------- | -------------------------- |
| `branch_name`        | Branch to analyze for commits             | No       | Current ref name           |
| `previous_tag`       | Previous tag to compare against           | No       | Latest tag with v\* prefix |
| `api_url`            | Initos API URL                            | Yes      | N/A                        |
| `api_key`            | Initos API Key                            | Yes      | N/A                        |
| `feed_id`            | Initos Release Feed ID                    | Yes      | N/A                        |
| `repo`               | Repository name (owner/repo)              | No       | Current repository         |
| `max_commits`        | Maximum number of commits to include      | No       | 30                         |
| `notification_level` | Notification level (INFO, WARNING, ERROR) | No       | INFO                       |

## Outputs

| Output         | Description                           |
| -------------- | ------------------------------------- |
| `branch`       | The branch that was analyzed          |
| `previous_tag` | The previous tag used for comparison  |
| `commit_list`  | Formatted list of commits (Markdown)  |
| `post_id`      | ID of the notification post created   |
| `status_code`  | HTTP status code from the API request |

## Example Notification

The notification includes:

- Branch name
- Repository information
- Commit list with links to commits and PRs
- Release date

## Architecture

This action uses the modular [Initos Post Feed](../initos-post-feed) action for the API communication part, making it easy to:

1. Collect and format commit information
2. Send notifications with proper formatting
3. Reuse the post-to-feed functionality in other actions

## License

MIT
