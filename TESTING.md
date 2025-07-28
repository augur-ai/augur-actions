# Testing Augur Feed Update Action

This guide explains how to test the `augur-feed-update` action both locally and using GitHub Actions.

## 🧪 Local Testing

### Option 1: Using the Test Script

The easiest way to test the action locally is using the provided test script:

```bash
# Make sure the script is executable
chmod +x test-local.sh

# Run the test
./test-local.sh
```

The test script includes your provided test data:

- **API URL**: `http://localhost:8000`
- **API Key**: `bd7e5a7cfd396159a3d67711ea80f05b1765790bc93391a8638591b6fb2857ea1e7885b85cc6966ccbebdb394859e464`
- **Feed ID**: `10fe784a-4572-4ea7-b28b-24061269d962`
- **Event Type**: `TEST`
- **Data Variables**: `{"data.name": "Test User5", "commit_id": "34dd1r4a"}`

### Option 2: Manual Curl Testing

You can also test manually using curl:

```bash
curl --location 'http://localhost:8000/api/v1/webhook/feed/events/10fe784a-4572-4ea7-b28b-24061269d962' \
--header 'Content-Type: application/json' \
--header 'x-api-key: bd7e5a7cfd396159a3d67711ea80f05b1765790bc93391a8638591b6fb2857ea1e7885b85cc6966ccbebdb394859e464' \
--data '{
    "type": "TEST",
    "timestamp": "2025-07-28T00:28:22.898Z",
    "source": "curl_test",
    "data": {
      "data.name": "Test User5",
      "commit_id": "34dd1r4a"
    }
  }'
```

### Option 3: Custom Test Data

To test with different data, modify the variables in `test-local.sh`:

```bash
# Edit the script to change test data
nano test-local.sh

# Or create a custom test
API_URL="http://localhost:8000"
API_KEY="your-api-key"
FEED_ID="your-feed-id"
EVENT_TYPE="CUSTOM_EVENT"
SOURCE="custom_test"
DATA_VARIABLES='{"custom_field": "custom_value"}'
TIMESTAMP="2025-01-15T10:30:00.000Z"

# Then run the same logic as in test-local.sh
```

## 🚀 GitHub Actions Testing

### Using the Test Workflow

1. **Add the test workflow** to your repository:

   - Copy `test-augur-feed-update.yml` to `.github/workflows/`
   - Or use the workflow directly in your repository

2. **Run the test**:
   - Go to your repository's Actions tab
   - Select "Test Augur Feed Update Action"
   - Click "Run workflow"
   - Fill in the inputs or use defaults
   - Click "Run workflow"

### Test Workflow Features

The test workflow includes:

- **Manual trigger** with customizable inputs
- **Default test data** matching your provided example
- **Result display** showing status code and response
- **Error handling** for failed requests

### Customizing the Test

You can modify the test workflow inputs:

```yaml
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
        default: '{"data.name": "Test User5", "commit_id": "34dd1r4a"}'
      custom_timestamp:
        description: "Custom timestamp (optional)"
        required: false
        default: ""
```

## 🔍 What the Tests Validate

### Input Validation

- ✅ Required parameters (api_url, api_key, feed_id)
- ✅ JSON format validation for data_variables
- ✅ Timestamp format validation (if provided)

### Request Validation

- ✅ Proper HTTP headers (Content-Type, x-api-key)
- ✅ Correct API endpoint construction
- ✅ JSON payload formatting
- ✅ Retry logic for failed requests

### Response Validation

- ✅ HTTP status code checking
- ✅ Response body capture
- ✅ Success/failure determination

## 📊 Expected Test Results

### Successful Test

```
🧪 Testing Augur Feed Update Action Locally
==========================================
✅ Validating inputs...
✅ Input validation passed
📦 Preparing request payload...
📋 Request payload:
{
  "type": "TEST",
  "timestamp": "2025-07-28T00:28:22.898Z",
  "source": "local_test",
  "data": {
    "data.name": "Test User5",
    "commit_id": "34dd1r4a"
  }
}
🌐 Sending request to: http://localhost:8000/api/v1/webhook/feed/events/10fe784a-4572-4ea7-b28b-24061269d962
📤 Sending request...
📊 Response Summary:
- Status Code: 200
- Response Body: {"status": "success"}
✅ Request successful!
🎉 Action simulation completed successfully
```

### Failed Test (Example)

```
❌ Request failed
💥 Action simulation failed
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Refused**

   - Ensure your API server is running on `localhost:8000`
   - Check if the port is correct

2. **Authentication Failed**

   - Verify the API key is correct
   - Check if the API key has proper permissions

3. **Invalid JSON**

   - Ensure data_variables is valid JSON
   - Check for proper escaping of special characters

4. **Feed ID Not Found**
   - Verify the feed ID exists in your system
   - Check if the feed ID format is correct

### Debug Mode

To enable debug output, modify the test script:

```bash
# Add debug flag to curl
curl -v --location "$FULL_API_URL" \
  --header "Content-Type: application/json" \
  --header "x-api-key: $API_KEY" \
  --data "$PAYLOAD"
```

## 🎯 Next Steps

After successful testing:

1. **Deploy the action** to your repository
2. **Set up secrets** in your repository settings
3. **Create production workflows** using the action
4. **Monitor logs** for any issues

## 📝 Test Data Reference

Your provided test data:

- **Endpoint**: `http://localhost:8000/api/v1/webhook/feed/events/10fe784a-4572-4ea7-b28b-24061269d962`
- **API Key**: `bd7e5a7cfd396159a3d67711ea80f05b1765790bc93391a8638591b6fb2857ea1e7885b85cc6966ccbebdb394859e464`
- **Payload**: See the JSON structure in the test script

---

**Happy Testing! 🚀**
