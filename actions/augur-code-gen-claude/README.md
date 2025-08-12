# Augur Code Generation with Claude

A GitHub Action that leverages Anthropic's Claude AI to generate code changes based on natural language prompts. This action automatically creates pull requests with AI-generated code changes, following your project's existing patterns and conventions.

## 🎯 Overview

The `augur-code-gen-claude` action uses Claude 3.5 Sonnet to understand your codebase and generate high-quality code changes based on natural language descriptions. It can be triggered manually through GitHub's UI or programmatically via repository dispatch events.

## ✨ Features

- **Natural Language Prompts**: Describe coding tasks in plain English
- **Intelligent Code Generation**: Claude analyzes your codebase patterns and conventions
- **Automatic Pull Requests**: Creates PRs with generated code changes
- **Multiple Trigger Methods**: Manual dispatch or programmatic triggers
- **Comprehensive Tooling**: Full access to Git, file operations, and code analysis tools
- **Quality Assurance**: AI reviews generated code for best practices
- **Detailed Documentation**: Auto-generated PR descriptions with execution details

## 🚀 Quick Start

### Manual Trigger

1. Go to your repository's Actions tab
2. Select "Claude Code Agent Trigger" workflow
3. Click "Run workflow"
4. Enter your coding prompt in natural language
5. Click "Run workflow" to execute

### Basic Usage Example

```yaml
name: Generate Code with Claude
on:
  workflow_dispatch:
    inputs:
      claude_prompt:
        description: "Describe the coding task for Claude"
        required: true
        type: string

jobs:
  generate-code:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Claude Code Generation
        uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
```

### Programmatic Trigger

```bash
# Trigger via GitHub API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_ORG/YOUR_REPO/dispatches \
  -d '{
    "event_type": "claude-code-trigger",
    "client_payload": {
      "prompt": "Add error handling to the authentication module"
    }
  }'
```

## 🔧 Configuration

### Required Secrets

| Secret              | Description                  | Example            |
| ------------------- | ---------------------------- | ------------------ |
| `ANTHROPIC_API_KEY` | API key for Anthropic Claude | `sk-ant-api03-...` |

### Input Parameters

| Parameter       | Required | Default | Description                                     |
| --------------- | -------- | ------- | ----------------------------------------------- |
| `claude_prompt` | ✅ Yes   | -       | Natural language description of the coding task |

### Available Tools

Claude has access to the following tools:

- **Git Operations**: Full git command access for version control
- **File Operations**: Read, write, and modify files
- **Code Analysis**: Grep, glob, and batch operations for code exploration
- **View Tools**: Examine file contents and directory structures

## 📋 Usage Examples

### 1. Add New Feature

```yaml
- name: Add user authentication
  uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
  with:
    claude_prompt: |
      Add a user authentication system with the following requirements:
      - JWT token-based authentication
      - Login and logout endpoints
      - Password hashing with bcrypt
      - Middleware for protected routes
      - Follow existing API patterns in the codebase
```

### 2. Fix Bugs

```yaml
- name: Fix authentication bug
  uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
  with:
    claude_prompt: |
      Fix the bug where users are logged out after 5 minutes instead of 1 hour.
      The issue seems to be in the JWT token expiration configuration.
```

### 3. Refactor Code

```yaml
- name: Refactor database layer
  uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
  with:
    claude_prompt: |
      Refactor the database connection code to use a connection pool
      and add proper error handling. Maintain backward compatibility
      with existing functions.
```

### 4. Add Tests

```yaml
- name: Add unit tests
  uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
  with:
    claude_prompt: |
      Add comprehensive unit tests for the user service module.
      Use the existing testing framework and follow the patterns
      used in other test files.
```

### 5. Update Documentation

```yaml
- name: Update API documentation
  uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
  with:
    claude_prompt: |
      Update the API documentation to include the new endpoints
      that were recently added. Generate OpenAPI/Swagger specs
      if they don't exist.
```

## 🔄 Workflow Examples

### Automated Code Generation on Issues

```yaml
name: Claude Code Generation

on:
  issues:
    types: [labeled]

jobs:
  generate-code:
    runs-on: ubuntu-latest
    if: contains(github.event.label.name, 'claude-generate')
    steps:
      - name: Extract prompt from issue
        id: extract_prompt
        run: |
          echo "prompt<<EOF" >> $GITHUB_OUTPUT
          echo "${{ github.event.issue.body }}" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Generate code with Claude
        uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
        with:
          claude_prompt: ${{ steps.extract_prompt.outputs.prompt }}
```

### Scheduled Code Improvements

```yaml
name: Weekly Code Improvements

on:
  schedule:
    - cron: "0 9 * * 1" # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  improve-code:
    runs-on: ubuntu-latest
    steps:
      - name: Generate code improvements
        uses: augur-ai/augur-actions/actions/augur-code-gen-claude@main
        with:
          claude_prompt: |
            Analyze the codebase for potential improvements:
            - Add missing error handling
            - Optimize performance bottlenecks
            - Add missing documentation
            - Improve code organization
            - Add type hints where missing
```

## 🏗️ Architecture

The action follows a structured approach to code generation:

```
augur-code-gen-claude/
├── action.yml          # Action definition and workflow
└── README.md           # This documentation
```

### Execution Flow

1. **Prompt Extraction**: Extracts the coding prompt from manual input or dispatch event
2. **Claude Invocation**: Calls Anthropic's Claude API with the prompt and system instructions
3. **Code Analysis**: Claude explores the codebase structure and patterns
4. **Code Generation**: Generates code changes following existing conventions
5. **Change Detection**: Checks for any modifications to the codebase
6. **PR Creation**: Creates a pull request with the generated changes
7. **Documentation**: Provides detailed PR description with execution details

### Core Components

1. **Trigger Handling**: Supports both manual and programmatic triggers
2. **Prompt Processing**: Extracts and formats prompts for Claude
3. **AI Integration**: Interfaces with Anthropic's Claude Code Base Action
4. **Git Integration**: Handles version control operations
5. **PR Management**: Creates and manages pull requests

## 🔍 System Prompt

Claude operates with the following system prompt:

```
You are a senior software engineer. Focus on writing clean, maintainable,
and well-documented code. Always follow the project's existing patterns
and conventions.

APPROACH:
1. First, explore the codebase structure using ls and find commands
2. Use grep to search for relevant code patterns related to the task
3. Read the relevant files to understand the existing code
4. Make targeted changes following the existing patterns
5. Test your changes and commit with clear messages

Start by exploring - don't assume anything about the project structure.
```

## 🤖 AI Capabilities

Claude has access to:

- **Codebase Exploration**: Can navigate and understand project structure
- **Pattern Recognition**: Identifies and follows existing code patterns
- **Best Practices**: Applies software engineering best practices
- **Documentation**: Generates appropriate comments and documentation
- **Testing**: Can write tests following project conventions
- **Refactoring**: Improves code quality while maintaining functionality

## 🔒 Security Considerations

- **API Key Security**: Store Anthropic API key in GitHub Secrets
- **Code Review**: Always review generated code before merging
- **Branch Protection**: Consider requiring reviews for AI-generated PRs
- **Audit Trail**: All changes are tracked with detailed PR descriptions

## 🧪 Testing

### Manual Testing

1. Create a test repository
2. Add the `ANTHROPIC_API_KEY` secret
3. Trigger the workflow with a simple prompt
4. Review the generated PR

### Example Test Prompts

```yaml
# Simple test
claude_prompt: "Add a hello world function to the main module"

# Complex test
claude_prompt: |
  Add a REST API endpoint for user management with:
  - GET /users - list all users
  - POST /users - create a new user
  - PUT /users/:id - update a user
  - DELETE /users/:id - delete a user
  Include proper error handling and validation
```

## 🚨 Limitations

- **API Rate Limits**: Subject to Anthropic API rate limits
- **Token Limits**: Large codebases may hit token limits
- **Context Window**: Claude has a finite context window
- **Beta Action**: Uses beta version of Claude Code Base Action

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
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Claude Code Base Action](https://github.com/marketplace/actions/claude-code-base-action)

---

**Built with ❤️ by the Augur AI team**
