# Augur SARIF Minimizer

Converts full CodeQL SARIF files to minimal format for efficient transport and storage while maintaining SARIF compliance.

## What it does

This action takes a full SARIF file (typically 2-3MB) and creates a minimal version (typically 50-100KB) by:

- ✅ Keeping essential fields: file paths, rule IDs, descriptions, severity levels
- ❌ Removing verbose content: detailed markdown, examples, references, metadata
- 🗜️ Achieving 95%+ size reduction
- 📋 Maintaining valid SARIF 2.1.0 format

## Usage

### Basic Usage

```yaml
- name: Minimize SARIF
  uses: augur-ai/augur-actions/actions/augur-sarif-minimizer@main
```

### Advanced Usage

```yaml
- name: Minimize SARIF with Custom Paths
  uses: augur-ai/augur-actions/actions/augur-sarif-minimizer@main
  with:
    input_sarif: "path/to/large.sarif"
    output_sarif: "path/to/minimal.sarif"
    keep_original: true
```

## Inputs

| Input           | Description                   | Required | Default              |
| --------------- | ----------------------------- | -------- | -------------------- |
| `input_sarif`   | Path to input SARIF file      | No       | `feed_data.json`     |
| `output_sarif`  | Path for output minimal SARIF | No       | `minimal_sarif.json` |
| `keep_original` | Keep original SARIF file      | No       | `false`              |

## Outputs

| Output              | Description                      |
| ------------------- | -------------------------------- |
| `original_size`     | Size of original SARIF in bytes  |
| `minimized_size`    | Size of minimized SARIF in bytes |
| `compression_ratio` | Compression ratio percentage     |

## Examples

### In Security Scan Workflow

```yaml
- name: Run CodeQL Analysis
  uses: github/codeql-action/analyze@v3
  with:
    output: sarif-results

- name: Process Results
  # ... your existing processing that creates feed_data.json ...

- name: Minimize SARIF for Transport
  uses: augur-ai/augur-actions/actions/augur-sarif-minimizer@main
  with:
    input_sarif: feed_data.json
    output_sarif: feed_data.json # Overwrite with minimal version
    keep_original: false

- name: Send to API
  # ... your existing send step that reads the now-minimal feed_data.json ...
```

### Standalone Usage

```yaml
- name: Minimize Any SARIF
  uses: augur-ai/augur-actions/actions/augur-sarif-minimizer@main
  with:
    input_sarif: "results.sarif"
    output_sarif: "minimal.sarif"
    keep_original: true
```

## What Gets Preserved

- **File paths** (`artifactLocation.uri`)
- **Rule IDs** (`rule.id`)
- **Basic descriptions** (`message.text`)
- **Severity levels** (`level`)
- **SARIF structure** (valid 2.1.0 format)

## What Gets Removed

- **Detailed markdown** (examples, code snippets)
- **Security severity scores** (properties)
- **CWE tags** and metadata
- **Tool configuration details**
- **Execution metadata**
- **Verbose descriptions**

## Benefits

- 🚀 **Faster uploads** to APIs
- 💾 **Less storage** in databases
- 📊 **Easier processing** of essential data
- 🔄 **Maintains compatibility** with SARIF tools
- ⚡ **95%+ size reduction**

## Requirements

- **Ubuntu runner** (for apt-get)
- **jq** (installed automatically)
- **Valid SARIF 2.0/2.1** input file

## Error Handling

The action will fail if:

- Input SARIF file doesn't exist
- Input file is not valid JSON
- Input file doesn't have required SARIF structure
- jq installation fails

## License

MIT License - see [LICENSE](../../LICENSE) for details.
