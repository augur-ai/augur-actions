# Augur Security Scan

**One step. Any language. Optional Augur notifications.**

CodeQL security scanning with automatic language detection. Optionally sends SARIF results to Augur feed. 🚀

## ⚡ One Step Setup

```yaml
# Minimal - just run the scan
- uses: augur-ai/augur-actions/actions/augur-security-scan@main

# With Augur notifications
- uses: augur-ai/augur-actions/actions/augur-security-scan@main
  with:
    api_url: ${{ secrets.AUGUR_API_URL }}
    api_key: ${{ secrets.AUGUR_API_KEY }}
    feed_id: ${{ secrets.AUGUR_FEED_ID }}
```

**What happens automatically:**

- ✅ **Auto-detects** all supported languages in your repo
- ✅ **Runs CodeQL** security analysis with full SARIF output
- ✅ **Optionally sends SARIF results** to Augur feed (if configured)
- ✅ **Never breaks** your build (unless you want it to)

## 🌍 Supported Languages

CodeQL automatically detects and scans:

| Language       | File Extensions       | Security Checks                                |
| -------------- | --------------------- | ---------------------------------------------- |
| **JavaScript** | `.js`, `.jsx`, `.mjs` | XSS, injection, prototype pollution            |
| **TypeScript** | `.ts`, `.tsx`         | Type safety, XSS, injection                    |
| **Python**     | `.py`                 | Code injection, SQL injection, deserialization |
| **Java**       | `.java`               | Injection, deserialization, path traversal     |
| **C#**         | `.cs`                 | SQL injection, XSS, deserialization            |
| **C/C++**      | `.c`, `.cpp`, `.h`    | Buffer overflows, memory issues                |
| **Go**         | `.go`                 | Injection, path traversal                      |
| **Ruby**       | `.rb`                 | Code injection, XSS                            |

## 🎯 Configuration Options

| Input            | Description                | Default         |
| ---------------- | -------------------------- | --------------- |
| `api_url`        | Augur API base URL         | Not set         |
| `api_key`        | Augur API authentication   | Not set         |
| `feed_id`        | Augur feed ID              | Not set         |
| `languages`      | Specific languages to scan | Auto-detect all |
| `fail_on_issues` | Fail if issues found       | `false`         |

## 📝 Usage Examples

### 1. Zero Configuration (Copy & Paste!)

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: augur-ai/augur-actions/actions/augur-security-scan@main
```

### 2. With Augur Feed Notifications

```yaml
- uses: augur-ai/augur-actions/actions/augur-security-scan@main
  with:
    api_url: ${{ secrets.AUGUR_API_URL }}
    api_key: ${{ secrets.AUGUR_API_KEY }}
    feed_id: ${{ secrets.AUGUR_FEED_ID }}
```

### 3. Specific Languages Only

```yaml
- uses: augur-ai/augur-actions/actions/augur-security-scan@main
  with:
    languages: "javascript,python"
```

### 4. Strict Mode (Fail on Issues)

```yaml
- uses: augur-ai/augur-actions/actions/augur-security-scan@main
  with:
    fail_on_issues: "true"
```

## 📊 Augur Feed Data

**When configured, sends comprehensive security data to Augur feed:**

```json
{
  "repository": "owner/repo-name",
  "branch": "main",
  "commit": "abc123def456",
  "scan_type": "codeql",
  "languages": "javascript,python,java",
  "total_files": 245,
  "total_findings": 3,
  "workflow_run": "https://github.com/owner/repo/actions/runs/123456",
  "sarif_data": {
    // Complete SARIF results with all security findings
    "runs": [...],
    "version": "2.1.0"
  }
}
```

**Uses the `augur-feed-update` action internally for reliable delivery.**

## 🔍 What Gets Scanned

**CodeQL Analysis:**

- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Code injection attacks
- Path traversal issues
- Insecure deserialization
- Authentication bypasses
- And 100+ other security patterns!

**Fallback Scan** (if CodeQL unavailable):

- Basic pattern matching for common issues
- Still covers major security anti-patterns

## 📈 Outputs

| Output               | Description        | Example             |
| -------------------- | ------------------ | ------------------- |
| `results_count`      | Number of findings | `5`                 |
| `status`             | Scan status        | `success`           |
| `languages_detected` | Languages found    | `javascript,python` |

## 💰 Cost Analysis

**GitHub Actions Usage:**

- **Setup time**: 30 seconds
- **CodeQL analysis**: 1-3 minutes (depending on codebase size)
- **Total cost**: ~2-4 minutes of runner time per scan

**For most repositories:**

- Small repos (<1000 files): ~1 minute
- Medium repos (1000-10000 files): ~2-3 minutes
- Large repos (10000+ files): ~3-5 minutes

## 🚀 Why Use This Action?

✅ **One step setup** - just add the action, nothing else  
✅ **Auto-detects languages** - JavaScript, Python, Java, C#, Go, Ruby, C/C++  
✅ **Full SARIF to Augur** - complete security findings automatically sent  
✅ **Industry standard** - powered by GitHub CodeQL  
✅ **Never breaks builds** - continues on errors by default  
✅ **Minimal cost** - ~2-3 minutes runner time

## 🔧 Advanced Usage

### Matrix Strategy for Large Monorepos

```yaml
strategy:
  matrix:
    language: [javascript, python, java]
steps:
  - uses: augur-ai/augur-actions/actions/augur-security-scan@main
    with:
      languages: ${{ matrix.language }}
```

### Scheduled Security Scans

```yaml
on:
  schedule:
    - cron: "0 2 * * 1" # Weekly Monday 2 AM
  push:
    branches: [main]
```

### Integration with GitHub Security Tab

The action automatically integrates with GitHub's security features. Results appear in:

- Security tab
- Pull request checks
- Workflow summaries

## 🛠️ Troubleshooting

**No languages detected?**

- Ensure your code files are in the repository root or subdirectories
- Check that file extensions match supported languages

**CodeQL fails?**

- Action automatically falls back to pattern-based scanning
- Check GitHub Actions logs for specific error messages

**Webhook not receiving data?**

- Verify webhook URL is accessible
- Check webhook endpoint accepts POST requests with JSON

## 🔗 Integration Examples

**Slack Notifications:**

```yaml
with:
  webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

**Custom Dashboard:**

```yaml
with:
  webhook_url: https://dashboard.company.com/security-webhook
```

**Multiple Webhooks:** Use the outputs in subsequent steps to send to multiple endpoints.

---

**Get started in 30 seconds!** Just copy the zero-config example above. 🎯
