# Augur Actions

A collection of GitHub Actions for automated notifications and release tracking, designed to integrate with API feed systems for real-time project updates.

## 🎯 Overview

Augur Actions provides a modular set of GitHub Actions that help teams stay informed about their development activities through automated notifications. The actions are designed to work with API feed systems (like Initos) to provide real-time updates about releases, commits, and project changes.

## 🏗️ Architecture

The project follows a modular architecture with reusable components:

```
augur-actions/
├── actions/
│   ├── post-feed-update/          # Core notification action
│   ├── release-branch-notification/ # Release branch creation tracking
│   └── release-branch-update/     # Release branch update tracking
```

### Core Components

1. **Post Feed Update** (`post-feed-update/`)

   - **Purpose**: Core notification action that sends formatted messages to API endpoints
   - **Features**: Markdown support, error handling, JSON payload formatting
   - **Reusability**: Used by other actions for API communication

2. **Release Branch Notification** (`release-branch-notification/`)

   - **Purpose**: Tracks when new release branches are created
   - **Features**: Collects commit history, formats in Markdown tables, sends notifications
   - **Triggers**: Branch creation events

3. **Release Branch Update** (`release-branch-update/`)
   - **Purpose**: Tracks updates to existing release branches
   - **Features**: Monitors PR merges, collects commit diffs, sends update notifications
   - **Triggers**: Push events to release branches

## 🚀 Quick Start

### Prerequisites

- GitHub repository with release branches
- API endpoint for notifications (e.g., Initos API)
- API credentials

### Basic Setup

1. **Add the Post Feed Update action** to your workflow:

```yaml
name: Send Notification
on:
  workflow_dispatch:

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send notification
        uses: augur-ai/augur-actions/actions/post-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          body: |
            ## Test Notification

            This is a test notification with **markdown** support.
          level: INFO
```

2. **Set up release branch tracking**:

```yaml
name: Release Tracking

on:
  create:
    branches:
      - "release/**"
  push:
    branches:
      - "release/**"

jobs:
  release-notification:
    runs-on: ubuntu-latest
    if: github.event_name == 'create'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify release branch creation
        uses: augur-ai/augur-actions/actions/release-branch-notification@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.RELEASE_FEED_ID }}

  release-update:
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify release branch update
        uses: augur-ai/augur-actions/actions/release-branch-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.RELEASE_FEED_ID }}
```

## 🔧 Configuration

### Required Secrets

All actions require these secrets to be configured in your repository:

| Secret    | Description                        | Example                   |
| --------- | ---------------------------------- | ------------------------- |
| `API_URL` | Base URL for your notification API | `https://api.example.com` |
| `API_KEY` | Authentication key for the API     | `your-api-key-here`       |
| `FEED_ID` | Target feed ID for notifications   | `feed-123`                |

### Optional Configuration

- **Notification Levels**: `INFO`, `WARNING`, `ERROR`
- **Commit Limits**: Control how many commits to include in notifications
- **Topics**: JSON metadata for categorizing notifications

## 📋 Available Actions

### Post Feed Update

**Purpose**: Send formatted notifications to API endpoints

**Key Features**:

- Markdown content support
- JSON payload formatting
- Error handling and validation
- Configurable notification levels

**Usage**:

```yaml
- uses: augur-ai/augur-actions/actions/post-feed-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.FEED_ID }}
    body: "Your notification content"
    level: INFO
    topics: '{"category": "release"}'
```

### Release Branch Notification

**Purpose**: Track new release branch creation

**Key Features**:

- Automatic commit collection
- Markdown table formatting
- PR link detection
- Previous tag comparison

**Usage**:

```yaml
- uses: augur-ai/augur-actions/actions/release-branch-notification@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.RELEASE_FEED_ID }}
    branch_name: ${{ github.ref_name }}
    max_commits: 30
```

### Release Branch Update

**Purpose**: Track updates to existing release branches

**Key Features**:

- PR merge detection
- Commit diff collection
- Automated commit filtering
- Update notifications

**Usage**:

```yaml
- uses: augur-ai/augur-actions/actions/release-branch-update@main
  with:
    api_url: ${{ secrets.API_URL }}
    api_key: ${{ secrets.API_KEY }}
    feed_id: ${{ secrets.RELEASE_FEED_ID }}
    max_commits: 50
```

## 🔄 Workflow Examples

### Complete Release Tracking

```yaml
name: Complete Release Tracking

on:
  create:
    branches:
      - "release/**"
  push:
    branches:
      - "release/**"
  pull_request:
    types: [closed]
    branches:
      - "release/**"

jobs:
  # Track new release branches
  release-created:
    runs-on: ubuntu-latest
    if: github.event_name == 'create'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify release branch creation
        uses: augur-ai/augur-actions/actions/release-branch-notification@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.RELEASE_FEED_ID }}

  # Track updates to release branches
  release-updated:
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Notify release branch update
        uses: augur-ai/augur-actions/actions/release-branch-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.RELEASE_FEED_ID }}
```

### Custom Notifications

```yaml
name: Custom Notifications

on:
  workflow_dispatch:
    inputs:
      message:
        description: "Notification message"
        required: true
      level:
        description: "Notification level"
        required: false
        default: "INFO"
        type: choice
        options:
          - INFO
          - WARNING
          - ERROR

jobs:
  send-notification:
    runs-on: ubuntu-latest
    steps:
      - name: Send custom notification
        uses: augur-ai/augur-actions/actions/post-feed-update@main
        with:
          api_url: ${{ secrets.API_URL }}
          api_key: ${{ secrets.API_KEY }}
          feed_id: ${{ secrets.FEED_ID }}
          body: ${{ github.event.inputs.message }}
          level: ${{ github.event.inputs.level }}
          topics: '{"manual": true, "user": "${{ github.actor }}"}'
```

## 🛠️ Development

### Project Structure

```
augur-actions/
├── actions/
│   ├── post-feed-update/
│   │   ├── action.yml          # Action definition
│   │   └── readme.md           # Action documentation
│   ├── release-branch-notification/
│   │   ├── action.yml
│   │   └── readme.md
│   └── release-branch-update/
│       ├── action.yml
│       └── README.md
└── README.md                   # This file
```

### Adding New Actions

1. Create a new directory in `actions/`
2. Add `action.yml` with action definition
3. Add `README.md` with documentation
4. Follow the modular pattern using `post-feed-update` for API communication

### Testing

Actions can be tested by:

1. Creating a test workflow in your repository
2. Using `workflow_dispatch` triggers for manual testing
3. Setting up test API endpoints for validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your action following the existing patterns
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - see individual action README files for details.

## 🔗 Related

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Composite Actions Guide](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [GitHub CLI](https://cli.github.com/) (used by some actions)

---

**Built with ❤️ by the Augur AI team**
