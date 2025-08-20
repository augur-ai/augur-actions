# Augur Code Generation with Augment

A GitHub Action that leverages Augment's industry-leading context engine and AI agent to generate code changes based on natural language prompts. This action automatically creates pull requests with AI-generated code changes, following your project's existing patterns and conventions with superior context awareness.

## 🎯 Overview

The `augur-code-gen-augment` action uses Augment's powerful AI agent through the Auggie CLI to understand your codebase and generate high-quality code changes based on natural language descriptions. It can be triggered manually through GitHub's UI or programmatically via repository dispatch events.

## ✨ Features

- **🧠 Advanced Context Engine**: Leverages Augment's world-leading context engine for superior code understanding
- **🤖 Intelligent Code Generation**: Generates code that follows your existing patterns and conventions
- **🔄 Automated Workflow**: Creates pull requests automatically with detailed descriptions
- **🎯 Flexible Triggers**: Support for both manual and programmatic triggers
- **📊 Comprehensive Logging**: Detailed execution logs and status reporting
- **🏷️ Smart Labeling**: Automatic PR labeling for easy identification

## 🚀 Quick Start

### Prerequisites

- GitHub repository with appropriate permissions
- Augment account and API key
- Node.js 22+ (automatically installed by the action)

### Setup

1. **Add the Augment API Key** to your repository secrets:
   - Go to your repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add a new secret named `AUGMENT_API_KEY` with your Augment API key

2. **Create a workflow file** (e.g., `.github/workflows/augment-code-gen.yml`):

```yaml
name: Augment Code Generation

on:
  workflow_dispatch:
    inputs:
      augment_prompt:
        description: "Describe the coding task for Augment Agent"
        required: true
        type: string

jobs:
  generate-code:
    uses: augur-ai/augur-actions/actions/augur-code-gen-augment@main
    secrets:
      AUGMENT_API_KEY: ${{ secrets.AUGMENT_API_KEY }}
```

## 📋 Usage Examples

### 1. Add New Feature

```yaml
- name: Add user authentication
  uses: augur-ai/augur-actions/actions/augur-code-gen-augment@main
  with:
    augment_prompt: |
      Add a user authentication system with the following requirements:
      - JWT token-based authentication
      - Login and logout endpoints
      - Password hashing with bcrypt
      - Middleware for protected routes
      - Follow existing API patterns in the codebase
```

### 2. Fix Bug

```yaml
- name: Fix authentication bug
  uses: augur-ai/augur-actions/actions/augur-code-gen-augment@main
  with:
    augment_prompt: |
      Fix the authentication bug where users are not properly logged out:
      - Clear all session data on logout
      - Invalidate JWT tokens
      - Redirect to login page
      - Add proper error handling
```

### 3. Refactor Code

```yaml
- name: Refactor database layer
  uses: augur-ai/augur-actions/actions/augur-code-gen-augment@main
  with:
    augment_prompt: |
      Refactor the database layer to use a repository pattern:
      - Create repository interfaces
      - Implement concrete repositories
      - Update existing code to use repositories
      - Maintain existing functionality
```

## 🔧 Configuration

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `augment_prompt` | Natural language description of the coding task | Yes | - |

### Secrets

| Secret | Description | Required |
|--------|-------------|----------|
| `AUGMENT_API_KEY` | Your Augment API key for authentication | Yes |

### Outputs

| Output | Description |
|--------|-------------|
| `pull-request-number` | The number of the created pull request |
| `pull-request-url` | The URL of the created pull request |
| `changes-detected` | Whether any changes were made to the codebase |

## 🔄 Trigger Methods

### 1. Manual Trigger (Workflow Dispatch)

Trigger the action manually from the GitHub Actions tab:

```yaml
on:
  workflow_dispatch:
    inputs:
      augment_prompt:
        description: "Coding task description"
        required: true
        type: string
```

### 2. Repository Dispatch

Trigger programmatically via API:

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "augment-code-trigger",
    "client_payload": {
      "prompt": "Add error handling to the payment processing module"
    }
  }'
```

## 🏗️ Architecture

The action follows a structured approach to code generation:

```
augur-code-gen-augment/
├── action.yml          # Action definition and workflow
└── README.md           # This documentation
```

### Execution Flow

1. **Environment Setup**: Installs Node.js 22+ and Auggie CLI
2. **Authentication**: Authenticates with Augment using the provided API key
3. **Prompt Processing**: Extracts and formats prompts for Augment Agent
4. **Code Generation**: Runs Auggie CLI with the prompt in automation mode
5. **Change Detection**: Checks for any modifications to the codebase
6. **PR Creation**: Creates a pull request with the generated changes
7. **Documentation**: Provides detailed PR description with execution details

### Core Components

1. **Trigger Handling**: Supports both manual and programmatic triggers
2. **CLI Integration**: Uses Auggie CLI for seamless Augment integration
3. **Context Engine**: Leverages Augment's advanced context understanding
4. **Git Integration**: Handles version control operations
5. **PR Management**: Creates and manages pull requests

## 🔍 Augment Agent Capabilities

Augment Agent operates with advanced capabilities:

- **Context Awareness**: Deep understanding of your entire codebase
- **Pattern Recognition**: Identifies and follows existing code patterns
- **Best Practices**: Applies industry and project-specific best practices
- **Integration Intelligence**: Understands how different parts of your system interact
- **Quality Assurance**: Ensures generated code meets your standards

## 🚨 Limitations

- **API Dependencies**: Requires valid Augment API key and active subscription
- **Node.js Requirement**: Requires Node.js 22+ (automatically installed)
- **Repository Access**: Needs appropriate GitHub repository permissions
- **CLI Availability**: Depends on Auggie CLI availability and compatibility

## 🔒 Security

- API keys are handled securely through GitHub Secrets
- No sensitive information is logged or exposed
- All operations are performed in isolated GitHub Actions environment
- Generated code is reviewed through standard PR process

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - see the main project README for details.

## 🔗 Related

- [Augur Actions Documentation](../README.md)
- [Augment Documentation](https://docs.augmentcode.com/)
- [Auggie CLI Documentation](https://docs.augmentcode.com/cli/overview)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
