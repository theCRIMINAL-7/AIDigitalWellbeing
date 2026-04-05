# API Debugging Guide 🔍

## 📋 **Enhanced Error Handling Added**

I've added comprehensive logging and error handling to help debug the "API Error: null" issue. Here's what to check:

## 🔍 **Debugging Steps**

### **1. Check LogCat Messages**
Run the app and filter LogCat by tag `MainActivity`. Look for these messages:

```
D/MainActivity: Sending API request with data: UsageData{...}
D/MainActivity: API Connectivity Test - Response Code: XXX
D/MainActivity: API Response Code: XXX
D/MainActivity: API Response Message: XXX
D/MainActivity: API Response Body: ApiResponse{...}
```

### **2. Common Issues & Solutions**

#### **Issue A: Network Connectivity**
**LogCat Shows:** `API Connectivity Test Failed`
**Causes:**
- No internet connection
- Firewall blocking requests
- DNS resolution issues

**Solutions:**
- Check device internet connection
- Try accessing the API URL in browser
- Test with different network

#### **Issue B: Server Response Error**
**LogCat Shows:** `HTTP Error: 404/500/403`
**Causes:**
- Wrong endpoint URL
- Server is down
- CORS issues
- Authentication required

**Solutions:**
- Verify API endpoint: `https://ai-digital-wellbeing-s-backend-web-dev-pbl.up.railway.app/analyze-usage`
- Check server status
- Test with Postman/curl

#### **Issue C: Response Parsing Error**
**LogCat Shows:** `API Error: null` with successful response code
**Causes:**
- Response format doesn't match expected structure
- Missing fields in response
- JSON parsing issues

**Expected Response Format:**
```json
{
  "success": true,
  "message": "Analysis complete",
  "data": "AI suggestions here"
}
```

#### **Issue D: Timeout Issues**
**LogCat Shows:** `SocketTimeoutException` or `Request timeout`
**Causes:**
- Slow server response
- Large data payload
- Network latency

**Solutions:**
- Increase timeout values
- Check server performance
- Reduce data payload

### **3. Test API Manually**

#### **Using curl:**
```bash
curl -X POST https://ai-digital-wellbeing-s-backend-web-dev-pbl.up.railway.app/analyze-usage \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test123",
    "total_screen_time": 120,
    "unlock_count": 15,
    "app_usage": [
      {"app": "WhatsApp", "minutes": 45},
      {"app": "Instagram", "minutes": 30}
    ],
    "sessions": [
      {"start": "09:00", "end": "09:30"},
      {"start": "14:00", "end": "14:15"}
    ],
    "notifications": {
      "WhatsApp": 5,
      "Instagram": 3
    }
  }'
```

#### **Using Postman:**
1. Method: POST
2. URL: `https://ai-digital-wellbeing-s-backend-web-dev-pbl.up.railway.app/analyze-usage`
3. Headers: `Content-Type: application/json`
4. Body: Raw JSON (same as above)

### **4. Check App Configuration**

#### **Network Security:**
- ✅ Added `network_security_config.xml`
- ✅ Configured domain for cleartext traffic
- ✅ Added internet permissions

#### **Data Serialization:**
- ✅ UsageData model matches API spec
- ✅ Added toString() methods for logging
- ✅ Proper JSON annotations

### **5. Enhanced Logging Features**

#### **Request Logging:**
- Shows complete UsageData structure
- Counts of app usage, sessions, notifications
- User ID and screen time

#### **Response Logging:**
- HTTP status codes
- Response messages
- Full response body
- Error body details

#### **Error Classification:**
- Network errors (timeout, unreachable)
- HTTP errors (4xx, 5xx)
- Business logic errors
- Parsing errors

### **6. Quick Debug Checklist**

- [ ] Internet connection working
- [ ] API URL accessible in browser
- [ ] Server responding to POST requests
- [ ] Response format matches expected structure
- [ ] No authentication required
- [ ] CORS properly configured
- [ ] SSL certificate valid

### **7. If Still Failing**

#### **Add More Logging:**
```java
// In sendToAPI method, add this before the call:
Log.d(TAG, "API URL: " + ApiClient.getClient().baseUrl().url());
Log.d(TAG, "Request Headers: " + call.request().headers());
```

#### **Test with Mock Data:**
Create a simple test with minimal data to isolate the issue.

#### **Check Server Logs:**
If you have access to the Railway server, check the server logs for incoming requests.

## 🚀 **Next Steps**

1. **Run the app** and check LogCat
2. **Identify the specific error** from the logs
3. **Test API manually** with curl/Postman
4. **Apply the appropriate solution** based on the error type

The enhanced logging will give you detailed information about what's happening at each step of the API call process. This should help identify exactly where the "null" error is coming from.
