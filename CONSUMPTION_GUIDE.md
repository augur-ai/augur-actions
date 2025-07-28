# Consuming the Augur Feed Update Action

This guide explains how to use the `augur-feed-update` action in your repositories.

## 🚀 Quick Setup

### 1. Required Secrets

Add these secrets to your repository (`Settings` → `Secrets and variables` → `Actions`):

| Secret Name     | Description                 | Example                                           |
| --------------- | --------------------------- | ------------------------------------------------- |
| `AUGUR_API_URL` | Base URL for your Augur API | `https://api.augur.ai` or `http://localhost:8000` |
| `AUGUR_API_KEY` | Your API authentication key | `your-api-key-here`                               |
| `AUGUR_FEED_ID` | Target feed ID for events   | `10fe784a-4572-4ea7-b28b-24061269d962`            |

### 2. Basic Workflow Example

Create `.github/workflows/augur-notifications.yml`:

```yaml
name: Augur Feed Notifications

on:
  workflow_dispatch:
    inputs:
      event_type:
        description: "Event type"
        required: true
        default: "DEPLOYMENT"
      custom_data:
        description: "Custom data (JSON)"
        required: false
        default: '{"environment": "production"}'

jobs:
  send-notification:
    runs-on: ubuntu-latest
    steps:
      - name: Send Augur notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_FEED_ID }}
          event_type: ${{ github.event.inputs.event_type }}
          data_variables: ${{ github.event.inputs.custom_data }}
          source: "github-workflow"
```

## 📋 Common Use Cases

### 1. Deployment Notifications

```yaml
name: Deployment Notifications

on:
  push:
    branches: [main, develop]

jobs:
  notify-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Send deployment notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_FEED_ID }}
          event_type: "DEPLOYMENT"
          source: "github-deployment"
          data_variables: |
            {
              "environment": "${{ github.ref_name }}",
              "commit_id": "${{ github.sha }}",
              "author": "${{ github.actor }}",
              "repository": "${{ github.repository }}"
            }
```

### 2. Release Notifications

```yaml
name: Release Notifications

on:
  release:
    types: [published, created]

jobs:
  notify-release:
    runs-on: ubuntu-latest
    steps:
      - name: Send release notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_FEED_ID }}
          event_type: "RELEASE"
          source: "github-release"
          data_variables: |
            {
              "version": "${{ github.event.release.tag_name }}",
              "title": "${{ github.event.release.name }}",
              "author": "${{ github.actor }}",
              "prerelease": ${{ github.event.release.prerelease }},
              "draft": ${{ github.event.release.draft }}
            }
```

### 3. Pull Request Notifications

```yaml
name: PR Notifications

on:
  pull_request:
    types: [opened, closed, merged]

jobs:
  notify-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Send PR notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_FEED_ID }}
          event_type: "PULL_REQUEST"
          source: "github-pr"
          data_variables: |
            {
              "action": "${{ github.event.action }}",
              "pr_number": ${{ github.event.pull_request.number }},
              "title": "${{ github.event.pull_request.title }}",
              "author": "${{ github.event.pull_request.user.login }}",
              "base_branch": "${{ github.event.pull_request.base.ref }}",
              "head_branch": "${{ github.event.pull_request.head.ref }}"
            }
```

### 4. Issue Notifications

```yaml
name: Issue Notifications

on:
  issues:
    types: [opened, closed, reopened]

jobs:
  notify-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Send issue notification
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: ${{ secrets.AUGUR_API_URL }}
          api_key: ${{ secrets.AUGUR_API_KEY }}
          feed_id: ${{ secrets.AUGUR_FEED_ID }}
          event_type: "ISSUE"
          source: "github-issue"
          data_variables: |
            {
              "action": "${{ github.event.action }}",
              "issue_number": ${{ github.event.issue.number }},
              "title": "${{ github.event.issue.title }}",
              "author": "${{ github.event.issue.user.login }}",
              "labels": ${{ toJSON(github.event.issue.labels.*.name) }}
            }
```

## 🔧 Configuration Options

### Input Parameters

| Parameter        | Required | Default         | Description                  |
| ---------------- | -------- | --------------- | ---------------------------- |
| `api_url`        | ✅ Yes   | -               | Base URL for your Augur API  |
| `api_key`        | ✅ Yes   | -               | API authentication key       |
| `feed_id`        | ✅ Yes   | -               | Target feed ID               |
| `event_type`     | ✅ Yes   | `TEST`          | Type of event being sent     |
| `source`         | ❌ No    | `github-action` | Source identifier            |
| `data_variables` | ❌ No    | `{}`            | JSON object with custom data |
| `timestamp`      | ❌ No    | Current time    | Custom timestamp (ISO 8601)  |

### Example with All Options

```yaml
- name: Send comprehensive notification
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  with:
    api_url: ${{ secrets.AUGUR_API_URL }}
    api_key: ${{ secrets.AUGUR_API_KEY }}
    feed_id: ${{ secrets.AUGUR_FEED_ID }}
    event_type: "CUSTOM_EVENT"
    source: "my-app-deployment"
    data_variables: |
      {
        "service": "user-api",
        "version": "1.2.3",
        "environment": "staging",
        "deployment_id": "deploy-123",
        "metrics": {
          "response_time": 150,
          "error_rate": 0.01
        }
      }
    timestamp: "2025-07-28T21:37:17.708Z"
```

## 🧪 Testing Locally

### Using Act (Recommended)

1. **Install Act**: `brew install act` (macOS) or follow [act installation guide](https://github.com/nektos/act)

2. **Create test workflow** `.github/workflows/test-augur.yml`:

```yaml
name: Test Augur Action

on:
  workflow_dispatch:
    inputs:
      event_type:
        description: "Event type to test"
        required: true
        default: "TEST"
      data_variables:
        description: "Test data (JSON)"
        required: false
        default: '{"test": "data"}'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Test Augur action
        uses: augur-ai/augur-actions/actions/augur-feed-update@main
        with:
          api_url: "http://localhost:8000"
          api_key: "your-test-api-key"
          feed_id: "your-test-feed-id"
          event_type: ${{ github.event.inputs.event_type }}
          data_variables: ${{ github.event.inputs.data_variables }}
```

3. **Run test**:

```bash
act workflow_dispatch -W .github/workflows/test-augur.yml \
  --input event_type=TEST \
  --input data_variables='{"test": "value"}' \
  --container-architecture linux/amd64 \
  --network host
```

## 🔒 Security Best Practices

### 1. Secret Management

- ✅ Use repository secrets for sensitive data
- ✅ Never hardcode API keys in workflows
- ✅ Rotate API keys regularly

### 2. Data Validation

- ✅ Validate `data_variables` JSON before sending
- ✅ Sanitize user inputs
- ✅ Limit data size to prevent abuse

### 3. Error Handling

- ✅ Monitor action failures
- ✅ Set up alerts for API errors
- ✅ Use retry logic for transient failures

## 📊 Monitoring & Debugging

### 1. Check Action Logs

- Go to your repository → `Actions` tab
- Click on the workflow run
- Review step logs for errors

### 2. Common Issues

| Issue               | Solution                                     |
| ------------------- | -------------------------------------------- |
| `API key invalid`   | Check secret value and API key format        |
| `Feed ID not found` | Verify feed ID exists in your Augur instance |
| `Network timeout`   | Check API URL and network connectivity       |
| `JSON parse error`  | Validate `data_variables` JSON format        |

### 3. Debug Mode

Add this to your workflow for detailed logging:

```yaml
- name: Debug notification
  uses: augur-ai/augur-actions/actions/augur-feed-update@main
  env:
    ACTIONS_STEP_DEBUG: true
  with:
    # ... your parameters
```

## 🚀 Production Checklist

Before using in production:

- [ ] API credentials configured as secrets
- [ ] Feed ID verified and accessible
- [ ] Network connectivity tested
- [ ] Error handling implemented
- [ ] Monitoring set up
- [ ] Rate limits understood
- [ ] Data validation in place

## 📞 Support

- **Documentation**: Check the action's README for detailed usage
- **Issues**: Report problems in the action repository
- **Examples**: See workflow examples in this guide

---

**Ready to integrate!** 🎉
