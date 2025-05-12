# Initos Post Feed Action

This GitHub Action posts notifications to the Initos API feed system.

## Features

- Sends formatted notifications to Initos API
- Supports markdown content
- Handles API authentication and error handling
- Returns post ID for reference

## Usage

```yaml
- name: Send notification to Initos
  uses: augur-ai/augur-actions/actions/initos-post-feed@main
  with:
    api_url: ${{ secrets.INITOS_API_URL }}
    api_key: ${{ secrets.INITOS_API_KEY }}
    feed_id: ${{ secrets.INITOS_FEED_ID }}
    body: |
      ## Notification Title

      This is a notification with **markdown** support.

      - Bullet point 1
      - Bullet point 2
    level: INFO
```

## Required Secrets

This action requires the following secrets to be set in your repository:

- `INITOS_API_URL`: The base URL for the Initos API
- `INITOS_API_KEY`: Your Initos API key for authentication
- `INITOS_FEED_ID`: The feed ID to post notifications to

## Inputs

| Input     | Description                                          | Required | Default |
| --------- | ---------------------------------------------------- | -------- | ------- |
| `api_url` | Initos API URL                                       | Yes      | N/A     |
| `api_key` | Initos API Key for authentication                    | Yes      | N/A     |
| `feed_id` | Initos Feed ID to post to                            | Yes      | N/A     |
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
  uses: augur-ai/augur-actions/actions/initos-post-feed@main
  with:
    api_url: ${{ secrets.INITOS_API_URL }}
    api_key: ${{ secrets.INITOS_API_KEY }}
    feed_id: ${{ secrets.INITOS_RELEASE_FEED_ID }}
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

## License

MIT
