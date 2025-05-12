# Post Feed Update Action

This GitHub Action posts notifications to API feed systems with support for Markdown formatting.

## Features

- Sends formatted notifications to API
- Supports markdown content
- Handles API authentication and error handling
- Returns post ID for reference
- Safely validates and processes JSON parameters

## Usage

```yaml
- name: Send notification to API
  uses: augur-ai/augur-actions/actions/post-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    body: |
      ## Notification Title

      This is a notification with **markdown** support.

      - Bullet point 1
      - Bullet point 2
    level: INFO
```

## Required Secrets

This action requires the following secrets to be set in your repository:

- `API_URL`: The base URL for the API
- `API_KEY`: Your API key for authentication
- `FEED_ID`: The feed ID to post notifications to

## Inputs

| Input     | Description                                          | Required | Default |
| --------- | ---------------------------------------------------- | -------- | ------- |
| `api_url` | API URL                                              | Yes      | N/A     |
| `api_key` | API Key for authentication                           | Yes      | N/A     |
| `feed_id` | Feed ID to post to                                   | Yes      | N/A     |
| `body`    | Content body in Markdown format                      | Yes      | N/A     |
| `level`   | Notification level (INFO, WARNING, ERROR)            | No       | INFO    |
| `topics`  | JSON string of topics to include in the notification | No       | {}      |

## Outputs

| Output        | Description                           |
| ------------- | ------------------------------------- |
| `post_id`     | ID of the created post                |
| `status_code` | HTTP status code from the API request |

## Example: Send a Release Notification

```yaml
- name: Send Release Notification
  uses: augur-ai/augur-actions/actions/post-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.RELEASE_FEED_ID }}
    body: |
      ## 🚀 New Release: v1.0.0

      **Date:** 2023-05-01

      ### What's New:

      - New feature 1
      - Bug fix 2
      - Performance improvement 3
    level: INFO
    topics: '{"release": true, "version": "1.0.0"}'
```

## Error Handling

This action includes improved error handling:

- Validates required inputs before execution
- Checks JSON format of the topics parameter
- Falls back to empty object `{}` if topics JSON is invalid
- Provides clear error messages and status codes

## License

MIT
