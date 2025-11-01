# 🌐 CURL & HTTP API Integration Guide

This folder contains everything you need to integrate the Google Maps Lead Generator API into your projects using CURL, HTTP requests, or automation tools.

---

## 📚 **Available Resources**

### 1. **CURL_API_DOCS.md** 📖
Complete API documentation with CURL examples for:
- ✅ Linux/Mac/Windows CURL commands
- ✅ PowerShell examples
- ✅ Python requests examples
- ✅ Node.js/JavaScript examples
- ✅ n8n workflow configuration
- ✅ Postman collection
- ✅ Zapier/Make.com webhooks
- ✅ Error handling guide

**Open this file to get:** Copy-paste ready CURL commands for all platforms

---

### 2. **api_requests.http** 🔌
HTTP request file for VS Code REST Client or similar tools.
Contains ready-to-use requests for:
- Check API status
- Generate leads (quick mode)
- Generate leads (with email)
- Various example queries

**How to use:**
1. Install "REST Client" extension in VS Code
2. Open `api_requests.http`
3. Click "Send Request" above any request

---

### 3. **node_examples.js** 💻
Node.js implementation examples:
- Axios method
- Fetch API method
- Native HTTP module
- Complete example with error handling
- n8n configuration
- Reusable class wrapper

**How to use:**
```bash
npm install axios
node node_examples.js
```

---

### 4. **test_curl_api.ps1** ⚡
PowerShell test script that demonstrates:
- API status check
- Lead generation request
- All CURL command variations
- Response formatting

**How to run:**
```powershell
.\test_curl_api.ps1
```

---

## 🚀 **Quick Start**

### Test the API is Running
```bash
curl -X GET http://localhost:5000/api/status
```

Expected response:
```json
{
  "status": "running",
  "version": "1.0.0"
}
```

### Get 5 Leads (Quick Mode - No Email)
**Linux/Mac:**
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Coffee shops in London", "num_leads": 5, "email": "your@email.com", "require_email": false}'
```

**Windows CMD:**
```cmd
curl -X POST http://localhost:5000/api/leads ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Coffee shops in London\", \"num_leads\": 5, \"email\": \"your@email.com\", \"require_email\": false}"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/leads" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query": "Coffee shops in London", "num_leads": 5, "email": "your@email.com", "require_email": false}'
```

### Get 5 Leads (With Email Extraction)
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Dental clinic, Pune", "num_leads": 5, "email": "your@email.com", "require_email": true}'
```

---

## 📋 **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Check if API is running |
| `/api/leads` | POST | Generate leads from Google Maps |

---

## 📊 **Request Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | What to search for (e.g., "Restaurants in Dubai") |
| `num_leads` | integer | ✅ Yes | 20 | Number of leads (1-100) |
| `email` | string | ✅ Yes | - | Your email address |
| `require_email` | boolean | ❌ No | false | Extract emails from websites |

---

## 🎯 **Use Cases**

### 1. **Automation Tools (n8n, Zapier, Make.com)**
- Use the POST endpoint in HTTP request nodes
- Set method to POST
- Add JSON body with parameters
- Set timeout to 5 minutes

### 2. **Custom Applications**
- Import `node_examples.js` in your Node.js app
- Use the `LeadGenerator` class
- Handle responses in your application logic

### 3. **Testing & Development**
- Use `api_requests.http` in VS Code
- Use `test_curl_api.ps1` for PowerShell testing
- Use Postman with the collection in `CURL_API_DOCS.md`

### 4. **Scripts & Batch Processing**
- Use CURL commands in bash scripts
- Use PowerShell for Windows automation
- Use Python requests for data pipelines

---

## ⏱️ **Expected Response Times**

| Mode | Time | Description |
|------|------|-------------|
| Without Email | 1-3 minutes | Fast - only scrapes Google Maps |
| With Email | 2-5 minutes | Slower - visits websites to find emails |

---

## 🔒 **Important Notes**

1. **Server must be running:** Start with `python app.py`
2. **Port 5000:** Default port is 5000, change in `app.py` if needed
3. **Timeout:** Set HTTP timeout to at least 5 minutes
4. **Rate Limits:** Browser-Use API has rate limits based on your plan
5. **CORS:** Already enabled in the API

---

## 💡 **Tips for HTTP Nodes**

### For n8n:
1. Use HTTP Request node
2. Method: POST
3. URL: `http://localhost:5000/api/leads`
4. Body type: JSON
5. Add timeout: 300000 ms (5 minutes)

### For Zapier:
1. Use Webhooks by Zapier
2. Action: POST
3. URL: Your server URL + `/api/leads`
4. Payload Type: JSON
5. Map fields from previous steps

### For Make.com (Integromat):
1. HTTP module
2. Make a request
3. Method: POST
4. Body type: Raw (application/json)
5. Parse response: Yes

---

## 📞 **Getting Help**

If you encounter issues:

1. **Check server status:**
   ```bash
   curl -X GET http://localhost:5000/api/status
   ```

2. **Check server logs:** Look at terminal where `python app.py` is running

3. **Test with minimal request:**
   ```bash
   curl -X POST http://localhost:5000/api/leads \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "num_leads": 1, "email": "test@test.com", "require_email": false}'
   ```

4. **Review documentation:** See `CURL_API_DOCS.md` for detailed examples

---

## 🎉 **You're Ready!**

Choose your preferred method:
- 📖 See `CURL_API_DOCS.md` for complete documentation
- 🔌 Use `api_requests.http` for quick testing
- 💻 Use `node_examples.js` for Node.js integration
- ⚡ Run `test_curl_api.ps1` to see it in action

**Happy integrating!** 🚀
