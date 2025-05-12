# Release Branch Update Action

This GitHub Action tracks updates (new commits) to existing release branches and sends notifications to an API.

## Features

- Detects new commits pushed to release branches
- Collects information about recent commits
- Formats commits in a Markdown table
- Sends notifications using the [Post Feed Update](../post-feed-update) action
- Skips notifications for GitHub Actions automated commits
- Handles error cases gracefully

## Usage

Add this action to your workflow file:

```yaml
name: Release Branch Updates

on:
  push:
    branches:
      - "release/**"

jobs:
  notify-release-updates:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify branch update
        uses: augur-ai/augur-actions/actions/release-branch-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_RELEASE_FEED_ID }}
```

## Required Secrets

This action requires the following secrets to be set in your repository:

- `AUGUR_API_URL`: The base URL for the API
- `AUGUR_API_KEY`: Your API key for authentication
- `AUGUR_RELEASE_FEED_ID`: The feed ID to post notifications to

## Inputs

| Input                | Description                               | Required | Default            |
| -------------------- | ----------------------------------------- | -------- | ------------------ |
| `branch_name`        | Branch to analyze for updates             | No       | Current ref name   |
| `api_url`            | API URL for notification service          | Yes      | N/A                |
| `api_key`            | API Key for authentication                | Yes      | N/A                |
| `feed_id`            | Feed ID to post to                        | Yes      | N/A                |
| `repo`               | Repository name (owner/repo)              | No       | Current repository |
| `max_commits`        | Maximum number of recent commits to show  | No       | 5                  |
| `notification_level` | Notification level (INFO, WARNING, ERROR) | No       | INFO               |

## Outputs

| Output        | Description                           |
| ------------- | ------------------------------------- |
| `branch`      | The branch that was analyzed          |
| `commit_list` | Formatted list of recent commits      |
| `post_id`     | ID of the notification post created   |
| `status_code` | HTTP status code from the API request |

## Example Notification

The notification includes:

- Branch name
- Repository information
- Recent commits with links and PR references
- Timestamp

## Architecture

This action uses the modular [Post Feed Update](../post-feed-update) action for the API communication part, making it easy to:

1. Collect and format commit information
2. Send notifications with proper formatting
3. Track changes to existing release branches

## License

MIT
