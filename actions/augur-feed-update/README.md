# Augur Feed Update

A GitHub Action for sending webhook requests to Augur API endpoints with dynamic data variables. This action allows you to send custom events with any number of data variables to your Augur feed system.

## 🎯 Overview

The `augur-feed-update` action sends HTTP POST requests to Augur API webhook endpoints with customizable event data. It's designed to be flexible and can handle any number of dynamic data variables while maintaining proper error handling and validation.

## ✨ Features

- **Dynamic Data Variables**: Send any number of custom data fields
- **Flexible Event Types**: Customize event types for different use cases
- **Automatic Timestamping**: Uses current timestamp or accepts custom timestamps
- **Robust Error Handling**: Comprehensive validation and error reporting
- **Retry Logic**: Automatic retries for failed requests
- **JSON Validation**: Ensures all data is properly formatted
- **Detailed Outputs**: Provides status codes and response bodies

## 🚀 Quick Start

### Basic Usage

```yaml
name: Send Test Event
on:
  workflow_dispatch:

jobs:
  send-event:
    runs-on: ubuntu-latest
    steps:
      - name: Send webhook event
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: "TEST"
          source: "github-action"
          data_variables: '{"data.name": "Test User", "commit_id": "abc123"}'
```

### Advanced Usage

```yaml
name: Send Custom Event
on:
  workflow_dispatch:

jobs:
  send-custom-event:
    runs-on: ubuntu-latest
    steps:
      - name: Send custom webhook event
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: "DEPLOYMENT"
          source: "production-deploy"
          timestamp: "2025-01-15T10:30:00.000Z"
          data_variables: |
            {
              "environment": "production",
              "version": "1.2.3",
              "commit_sha": "${{ github.sha }}",
              "deployed_by": "${{ github.actor }}",
              "deployment_time": "2025-01-15T10:30:00.000Z"
            }
```

## 🔧 Configuration

### Required Secrets

| Secret    | Description                       | Example                                |
| --------- | --------------------------------- | -------------------------------------- |
| `API_URL` | Base URL for your Augur API       | `https://api.example.com`              |
| `API_KEY` | Authentication key for the API    | `your-api-key-here`                    |
| `FEED_ID` | Target feed ID for webhook events | `10fe784a-4572-4ea7-b28b-24061269d962` |

### Input Parameters

| Parameter        | Required | Default           | Description                             |
| ---------------- | -------- | ----------------- | --------------------------------------- |
| `api_url`        | ✅ Yes   | -                 | Base URL for the Augur API              |
| `api_key`        | ✅ Yes   | -                 | API key for authentication              |
| `feed_id`        | ✅ Yes   | -                 | Feed ID for the webhook endpoint        |
| `event_type`     | ✅ Yes   | `"TEST"`          | Type of event being sent                |
| `source`         | ✅ Yes   | `"github-action"` | Source identifier for the event         |
| `data_variables` | ❌ No    | `"{}"`            | JSON object with dynamic data variables |
| `timestamp`      | ❌ No    | Current time      | Custom timestamp (ISO 8601 format)      |

### Output Parameters

| Output          | Description                                     |
| --------------- | ----------------------------------------------- |
| `status_code`   | HTTP status code from the API response          |
| `response_body` | Response body from the API                      |
| `success`       | Whether the request was successful (true/false) |

## 📋 Usage Examples

### 1. Simple Test Event

```yaml
- name: Send test event
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    event_type: "TEST"
    data_variables: '{"message": "Hello World"}'
```

### 2. Deployment Notification

```yaml
- name: Notify deployment
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    event_type: "DEPLOYMENT"
    source: "production"
    data_variables: |
      {
        "environment": "production",
        "version": "1.2.3",
        "commit_sha": "${{ github.sha }}",
        "deployed_by": "${{ github.actor }}",
        "repository": "${{ github.repository }}"
      }
```

### 3. Issue Tracking

```yaml
- name: Track issue creation
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    event_type: "ISSUE_CREATED"
    source: "github-issues"
    data_variables: |
      {
        "issue_number": "${{ github.event.issue.number }}",
        "issue_title": "${{ github.event.issue.title }}",
        "issue_author": "${{ github.event.issue.user.login }}",
        "repository": "${{ github.repository }}"
      }
```

### 4. Custom Timestamp

```yaml
- name: Send event with custom timestamp
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    event_type: "CUSTOM_EVENT"
    timestamp: "2025-01-15T10:30:00.000Z"
    data_variables: '{"custom_field": "custom_value"}'
```

## 🔄 Workflow Examples

### Complete Deployment Tracking

```yaml
name: Deployment Tracking

on:
  push:
    branches:
      - main
  workflow_run:
    workflows: ["Deploy to Production"]

jobs:
  track-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Send deployment notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: "DEPLOYMENT"
          source: "production-deploy"
          data_variables: |
            {
              "environment": "production",
              "version": "${{ github.sha }}",
              "deployed_by": "${{ github.actor }}",
              "repository": "${{ github.repository }}",
              "branch": "${{ github.ref_name }}"
            }
```

### Issue and PR Tracking

```yaml
name: Issue and PR Tracking

on:
  issues:
    types: [opened, closed, edited]
  pull_request:
    types: [opened, closed, merged]

jobs:
  track-issues:
    runs-on: ubuntu-latest
    if: github.event_name == 'issues'
    steps:
      - name: Track issue event
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: "ISSUE_${{ github.event.action | upper }}"
          source: "github-issues"
          data_variables: |
            {
              "issue_number": "${{ github.event.issue.number }}",
              "issue_title": "${{ github.event.issue.title }}",
              "issue_author": "${{ github.event.issue.user.login }}",
              "action": "${{ github.event.action }}"
            }

  track-prs:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Track PR event
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: "PR_${{ github.event.action | upper }}"
          source: "github-prs"
          data_variables: |
            {
              "pr_number": "${{ github.event.pull_request.number }}",
              "pr_title": "${{ github.event.pull_request.title }}",
              "pr_author": "${{ github.event.pull_request.user.login }}",
              "action": "${{ github.event.action }}"
            }
```

## 🏗️ Architecture

The action follows the project's modular architecture:

```
augur-feed-update/
├── action.yml          # Action definition
└── README.md           # This documentation
```

### Core Components

1. **Input Validation**: Validates all required inputs and JSON format
2. **Data Preparation**: Generates timestamps and formats payload
3. **Request Sending**: Sends HTTP POST with retry logic
4. **Response Handling**: Processes and validates API responses

### Integration Points

- **API Communication**: Direct HTTP POST to Augur API endpoints
- **Error Handling**: Comprehensive validation and error reporting
- **Data Formatting**: JSON payload generation with proper escaping
- **Output Management**: Structured outputs for workflow integration

## 🔍 Error Handling

The action includes comprehensive error handling:

- **Input Validation**: Validates all required inputs and data formats
- **JSON Validation**: Ensures data_variables is valid JSON
- **Timestamp Validation**: Validates custom timestamp format
- **Network Retries**: Automatic retries for failed requests
- **Status Code Checking**: Validates HTTP response codes
- **Detailed Error Messages**: Clear error reporting for debugging

## 🧪 Testing

### Manual Testing

```yaml
name: Test Augur Feed Update

on:
  workflow_dispatch:
    inputs:
      event_type:
        description: "Event type to test"
        required: true
        default: "TEST"
      data_variables:
        description: "Data variables (JSON)"
        required: false
        default: '{"test": "value"}'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Test webhook
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          event_type: ${{ github.event.inputs.event_type }}
          data_variables: ${{ github.event.inputs.data_variables }}
```

### Validation Testing

The action validates:

- Required input parameters
- JSON format for data_variables
- Timestamp format (if provided)
- API response status codes
- Network connectivity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - see the main project README for details.

## 🔗 Related

- [Augur Actions Documentation](../README.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Composite Actions Guide](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)

---

**Built with ❤️ by the Augur AI team**
