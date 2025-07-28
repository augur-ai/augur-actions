# GitHub Action Generator Prompt

Use this prompt to generate new GitHub Actions for the augur-actions project. This template ensures consistency with the existing architecture and patterns.

## Prompt Template

```
I need to create a new GitHub Action for the augur-actions project. Please generate a complete action following the project's patterns and architecture.

## Action Requirements

**Action Name**: [DESCRIBE THE ACTION NAME]
**Purpose**: [DESCRIBE WHAT THE ACTION DOES]
**Trigger Events**: [LIST THE GITHUB EVENTS THAT SHOULD TRIGGER THIS ACTION]

## Functional Requirements

1. **Input Parameters**:
   - Required: [LIST REQUIRED INPUTS]
   - Optional: [LIST OPTIONAL INPUTS WITH DEFAULTS]

2. **Output Parameters**:
   - [LIST WHAT THE ACTION SHOULD OUTPUT]

3. **Core Functionality**:
   - [DESCRIBE THE MAIN LOGIC THE ACTION SHOULD PERFORM]
   - [DESCRIBE ANY DATA COLLECTION OR PROCESSING]
   - [DESCRIBE HOW IT SHOULD FORMAT OUTPUT]

4. **Integration Requirements**:
   - Should use the `post-feed-update` action for API communication
   - Should follow the project's error handling patterns
   - Should include proper input validation

## Technical Constraints

- Must be a composite action (using `runs.using: "composite"`)
- Must include proper error handling and validation
- Must use bash shell for shell steps
- Should follow the existing project structure
- Should include comprehensive documentation

## Expected Output

Please generate:

1. **action.yml** - Complete action definition with all inputs, outputs, and steps
2. **README.md** - Comprehensive documentation following the project's format
3. **Usage examples** - Show how to integrate the action in workflows
4. **Error handling** - Proper validation and error messages

## Project Context

This action will be part of the augur-actions project which:
- Uses modular architecture with reusable components
- Integrates with API feed systems for notifications
- Follows consistent patterns for input validation and error handling
- Uses the `post-feed-update` action for API communication
- Includes comprehensive documentation for each action

## Existing Actions Reference

- **post-feed-update**: Core notification action with API integration
- **release-branch-notification**: Tracks new release branch creation
- **release-branch-update**: Tracks updates to existing release branches

Please generate the complete action following these patterns and requirements.
```

## Usage Examples

### Example 1: Issue Tracking Action

```
I need to create a new GitHub Action for the augur-actions project. Please generate a complete action following the project's patterns and architecture.

## Action Requirements

**Action Name**: issue-tracking
**Purpose**: Track issue creation and updates, sending notifications to API feed
**Trigger Events**: issues (opened, closed, edited), issue_comment

## Functional Requirements

1. **Input Parameters**:
   - Required: api_url, api_key, feed_id
   - Optional: notification_level (default: INFO), include_comments (default: true)

2. **Output Parameters**:
   - issue_id, action_type, post_id, status_code

3. **Core Functionality**:
   - Collect issue information (title, body, labels, assignees)
   - Format issue data in Markdown
   - Send notifications using post-feed-update action
   - Handle different issue events (created, updated, closed)

4. **Integration Requirements**:
   - Should use the `post-feed-update` action for API communication
   - Should follow the project's error handling patterns
   - Should include proper input validation

## Technical Constraints

- Must be a composite action (using `runs.using: "composite"`)
- Must include proper error handling and validation
- Must use bash shell for shell steps
- Should follow the existing project structure
- Should include comprehensive documentation

Please generate the complete action following these patterns and requirements.
```

### Example 2: Deployment Notification Action

```
I need to create a new GitHub Action for the augur-actions project. Please generate a complete action following the project's patterns and architecture.

## Action Requirements

**Action Name**: deployment-notification
**Purpose**: Track deployment events and send notifications with deployment details
**Trigger Events**: deployment, deployment_status, workflow_run (on deployment workflows)

## Functional Requirements

1. **Input Parameters**:
   - Required: api_url, api_key, feed_id
   - Optional: notification_level (default: INFO), include_environment (default: true)

2. **Output Parameters**:
   - deployment_id, environment, status, post_id, status_code

3. **Core Functionality**:
   - Collect deployment information (environment, status, commit SHA)
   - Format deployment data in Markdown
   - Send notifications using post-feed-update action
   - Handle different deployment statuses (success, failure, pending)

4. **Integration Requirements**:
   - Should use the `post-feed-update` action for API communication
   - Should follow the project's error handling patterns
   - Should include proper input validation

## Technical Constraints

- Must be a composite action (using `runs.using: "composite"`)
- Must include proper error handling and validation
- Must use bash shell for shell steps
- Should follow the existing project structure
- Should include comprehensive documentation

Please generate the complete action following these patterns and requirements.
```

## Action Generation Guidelines

### 1. Action Structure

Every action should follow this structure:

```yaml
name: "Action Name"
description: "Clear description of what the action does"
author: "augur-ai"

inputs:
  # Define all inputs with descriptions and requirements

outputs:
  # Define all outputs with descriptions

runs:
  using: "composite"
  steps:
    - name: Validate inputs
      # Input validation step

    - name: Core functionality
      # Main action logic

    - name: Post to API
      # Use post-feed-update action
```

### 2. Input Validation Pattern

```bash
- name: Validate inputs
  id: validate
  shell: bash
  run: |
    if [[ -z "${{ inputs.required_input }}" ]]; then
      echo "❌ Required input is missing"
      exit 1
    fi
```

### 3. API Communication Pattern

```yaml
- name: Post to API
  id: post-to-api
  uses: augur-ai/augur-actions/actions/post-feed-update@main
  with:
    api_url: ${{ inputs.api_url }}
    api_key: ${{ inputs.api_key }}
    feed_id: ${{ inputs.feed_id }}
    body: ${{ steps.content.outputs.body }}
    level: ${{ inputs.notification_level }}
    topics: ${{ steps.content.outputs.topics }}
```

### 4. Documentation Structure

Every action README should include:

1. **Overview** - What the action does
2. **Features** - Key capabilities
3. **Usage** - How to use the action
4. **Required Secrets** - What secrets are needed
5. **Inputs** - Complete input documentation
6. **Outputs** - Complete output documentation
7. **Examples** - Usage examples
8. **Architecture** - How it fits into the project
9. **License** - MIT license

### 5. Error Handling Patterns

- Validate all required inputs
- Handle API errors gracefully
- Provide clear error messages
- Use proper exit codes
- Include fallback behavior where appropriate

### 6. Markdown Formatting

- Use consistent Markdown formatting
- Include code blocks for examples
- Use tables for inputs/outputs documentation
- Include emojis for visual appeal
- Follow the existing documentation style

## Common Patterns

### Data Collection

```bash
# Collect data from GitHub context
DATA=$(jq -r '.event_data' "$GITHUB_EVENT_PATH")
```

### Markdown Formatting

```bash
# Create formatted content
BODY="## Title\n\n**Key:** Value\n\n### Details\n\n$CONTENT"
```

### JSON Processing

```bash
# Process JSON data safely
if ! echo "$JSON_DATA" | jq empty 2>/dev/null; then
  echo "Warning: Invalid JSON, using default"
  JSON_DATA="{}"
fi
```

### Output Escaping

```bash
# Escape content for GitHub Actions outputs
CONTENT="${CONTENT//'%'/'%25'}"
CONTENT="${CONTENT//$'\n'/'%0A'}"
echo "content=$CONTENT" >> $GITHUB_OUTPUT
```

## Testing Guidelines

When generating actions, include:

1. **Input validation tests**
2. **Error handling scenarios**
3. **API integration examples**
4. **Workflow integration examples**
5. **Edge case handling**

## Integration Checklist

- [ ] Uses `post-feed-update` for API communication
- [ ] Includes proper input validation
- [ ] Follows error handling patterns
- [ ] Includes comprehensive documentation
- [ ] Uses consistent naming conventions
- [ ] Includes usage examples
- [ ] Handles edge cases gracefully
- [ ] Follows the project's architectural patterns

---

**Note**: This prompt template ensures consistency across all actions in the augur-actions project while maintaining flexibility for different use cases.
