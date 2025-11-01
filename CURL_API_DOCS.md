# Google Maps Lead Generator - CURL API Documentation

## Base URL
```
http://localhost:5000
```

---

## 📍 **Endpoints**

### 1. Check API Status
**Endpoint:** `GET /api/status`

**CURL Command:**
```bash
curl -X GET http://localhost:5000/api/status
```

**PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/status" -Method GET | Select-Object Content
```

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0"
}
```

---

### 2. Generate Leads (Without Email Extraction)
**Endpoint:** `POST /api/leads`

**CURL Command (Linux/Mac):**
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Dental clinic, Pune",
    "num_leads": 5,
    "email": "your@email.com",
    "require_email": false
  }'
```

**CURL Command (Windows CMD):**
```cmd
curl -X POST http://localhost:5000/api/leads ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Dental clinic, Pune\", \"num_leads\": 1, \"email\": \"your@email.com\", \"require_email\": false}"
```

**PowerShell:**
```powershell
$body = @{
    query = "Dental clinic, Pune"
    num_leads = 5
    email = "your@email.com"
    require_email = $false
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/leads" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Response:**
```json
{
  "success": true,
  "leads": [
    {
      "name": "Deccan Dental Clinic",
      "address": "759/53, 1st floor, Fergusson College Rd...",
      "phone": "+91 73870 40464",
      "website": "http://www.bestorthodontistbracespune.in/",
      "email": ""
    }
  ],
  "count": 5,
  "email": "your@email.com"
}
```

---

### 3. Generate Leads (WITH Email Extraction)
**Endpoint:** `POST /api/leads`

**CURL Command (Linux/Mac):**
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Restaurants in Singapore",
    "num_leads": 10,
    "email": "your@email.com",
    "require_email": true
  }'
```

**CURL Command (Windows CMD):**
```cmd
curl -X POST http://localhost:5000/api/leads ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Restaurants in Singapore\", \"num_leads\": 10, \"email\": \"your@email.com\", \"require_email\": true}"
```

**PowerShell:**
```powershell
$body = @{
    query = "Restaurants in Singapore"
    num_leads = 10
    email = "your@email.com"
    require_email = $true
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/leads" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json -Depth 10
```

---

## 📋 **Request Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | Search query (e.g., "Coffee shops in London") |
| `num_leads` | integer | ✅ Yes | 20 | Number of leads to fetch (1-100) |
| `email` | string | ✅ Yes | - | Your email address for notifications |
| `require_email` | boolean | ❌ No | false | Enable email extraction from websites |

---

## 🌐 **Node.js / HTTP Node Examples**

### Using Axios (Node.js)
```javascript
const axios = require('axios');

const getLeads = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/leads', {
      query: 'Dental clinic, Pune',
      num_leads: 5,
      email: 'your@email.com',
      require_email: true
    });
    
    console.log('Success:', response.data);
    console.log('Total leads:', response.data.count);
    
    response.data.leads.forEach((lead, index) => {
      console.log(`\n${index + 1}. ${lead.name}`);
      console.log(`   Address: ${lead.address}`);
      console.log(`   Phone: ${lead.phone}`);
      console.log(`   Website: ${lead.website}`);
      console.log(`   Email: ${lead.email}`);
    });
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
};

getLeads();
```

### Using Fetch API (Node.js 18+)
```javascript
const getLeads = async () => {
  const response = await fetch('http://localhost:5000/api/leads', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: 'Hotels in Dubai',
      num_leads: 20,
      email: 'your@email.com',
      require_email: false
    })
  });
  
  const data = await response.json();
  console.log(data);
};

getLeads();
```

### Using Request (Node.js - Legacy)
```javascript
const request = require('request');

const options = {
  url: 'http://localhost:5000/api/leads',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  json: true,
  body: {
    query: 'Gyms in Los Angeles',
    num_leads: 15,
    email: 'your@email.com',
    require_email: true
  }
};

request(options, (error, response, body) => {
  if (error) {
    console.error('Error:', error);
  } else {
    console.log('Success:', body);
  }
});
```

---

## 🐍 **Python Examples**

### Using Requests
```python
import requests
import json

url = "http://localhost:5000/api/leads"

payload = {
    "query": "Dental clinic, Pune",
    "num_leads": 5,
    "email": "your@email.com",
    "require_email": True
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Success! Found {data['count']} leads")
    
    for i, lead in enumerate(data['leads'], 1):
        print(f"\n{i}. {lead['name']}")
        print(f"   Address: {lead['address']}")
        print(f"   Phone: {lead['phone']}")
        print(f"   Website: {lead['website']}")
        print(f"   Email: {lead['email']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Using urllib (No dependencies)
```python
import urllib.request
import json

url = "http://localhost:5000/api/leads"

data = {
    "query": "Coffee shops in Seattle",
    "num_leads": 10,
    "email": "your@email.com",
    "require_email": False
}

headers = {"Content-Type": "application/json"}
request = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers=headers,
    method='POST'
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode('utf-8'))
    print(json.dumps(result, indent=2))
```

---

## 🔧 **n8n Workflow Node**

### HTTP Request Node Configuration

**Method:** POST

**URL:** `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads`

**Authentication:** None

**Send Body:** Yes

**Body Content Type:** JSON

**Specify Body:** Using JSON

**JSON Parameters:**

| Name | Value | Type |
|------|-------|------|
| `query` | `{{ $json.query }}` or `"Dental clinic, Pune"` | String |
| `num_leads` | `{{ $json.num_leads }}` or `5` | **Number** (NOT String) |
| `email` | `{{ $json.email }}` or `"your@email.com"` | String |
| `require_email` | `{{ $json.require_email }}` or `false` | Boolean |

**⚠️ IMPORTANT for n8n:**
- `num_leads` must be a **NUMBER**, not a string
- `require_email` must be a **BOOLEAN** (true/false), not a string
- Don't wrap numbers in quotes in n8n JSON

**Example JSON Body:**
```json
{
  "query": "Dental clinic, Pune",
  "num_leads": 5,
  "email": "shyammawalweb@gmail.com",
  "require_email": false
}
```

**Alternative: Using Fields**

If using "Fields to Send" option in n8n:
- Set "Body Content Type" to "JSON"
- Add fields:
  - query (String): "Dental clinic, Pune"
  - num_leads (Number): 5
  - email (String): "shyammawalweb@gmail.com"
  - require_email (Boolean): false

**Importing CURL in n8n:**

When importing this CURL command:
```bash
curl -X POST http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Dental clinic, Pune", "num_leads": 1, "email": "shyammawalweb@gmail.com", "require_email": false}'
```

After import:
1. Check the JSON body in n8n
2. Ensure `num_leads` is a number (no quotes)
3. Ensure `require_email` is boolean (no quotes)

---

## 🌊 **Postman Collection**

### Import this JSON into Postman:

```json
{
  "info": {
    "name": "Google Maps Lead Generator API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Check API Status",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/api/status",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "status"]
        }
      }
    },
    {
      "name": "Generate Leads (No Email)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"Dental clinic, Pune\",\n  \"num_leads\": 5,\n  \"email\": \"your@email.com\",\n  \"require_email\": false\n}"
        },
        "url": {
          "raw": "http://localhost:5000/api/leads",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "leads"]
        }
      }
    },
    {
      "name": "Generate Leads (With Email)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"Restaurants in Singapore\",\n  \"num_leads\": 10,\n  \"email\": \"your@email.com\",\n  \"require_email\": true\n}"
        },
        "url": {
          "raw": "http://localhost:5000/api/leads",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "leads"]
        }
      }
    }
  ]
}
```

---

## 📡 **Webhook / API Integration Examples**

### Zapier Webhook
```
URL: http://localhost:5000/api/leads
Method: POST
Headers: Content-Type: application/json
Body: 
{
  "query": "{{query}}",
  "num_leads": {{num_leads}},
  "email": "{{email}}",
  "require_email": {{require_email}}
}
```

### Make.com (Integromat) HTTP Module
```json
{
  "url": "http://localhost:5000/api/leads",
  "method": "POST",
  "headers": [
    {
      "name": "Content-Type",
      "value": "application/json"
    }
  ],
  "body": {
    "query": "{{query}}",
    "num_leads": "{{numberOfLeads}}",
    "email": "{{userEmail}}",
    "require_email": "{{extractEmails}}"
  }
}
```

---

## ⚡ **Quick Test Commands**

### Test Without Email Extraction (Fast - 1-3 minutes)
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Coffee shops in London", "num_leads": 3, "email": "test@example.com", "require_email": false}'
```

### Test With Email Extraction (Slower - 2-5 minutes)
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Dental clinic, Pune", "num_leads": 3, "email": "test@example.com", "require_email": true}'
```

### Windows PowerShell Quick Test
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/leads" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query": "Hotels in Dubai", "num_leads": 5, "email": "test@example.com", "require_email": false}' | ConvertTo-Json -Depth 10
```

---

## 🔍 **Error Responses**

### Missing Required Field
**Status Code:** 400

**Response:**
```json
{
  "error": "Query is required"
}
```

### Server Error
**Status Code:** 500

**Response:**
```json
{
  "error": "Error message details here"
}
```

---

## 📊 **Response Format**

### Success Response Structure
```json
{
  "success": true,
  "leads": [
    {
      "name": "Business Name",
      "address": "Full Address Here",
      "phone": "+1234567890",
      "website": "https://example.com",
      "email": "contact@example.com"
    }
  ],
  "count": 5,
  "email": "your@email.com"
}
```

### Lead Object Structure
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Business name |
| `address` | string | Full business address |
| `phone` | string | Phone number (may be empty) |
| `website` | string | Website URL (may be empty) |
| `email` | string | Email address (may be empty unless require_email is true) |

---

## 🚀 **Production Deployment Notes**

If you deploy this to a production server, replace `localhost:5000` with your actual domain:

```
http://your-domain.com/api/leads
https://api.your-domain.com/leads
```

Remember to:
1. Update CORS settings if needed
2. Use HTTPS in production
3. Add rate limiting
4. Add authentication if needed
5. Set proper environment variables

---

## 💡 **Tips**

1. **For HTTP nodes in automation tools:** Use the POST endpoint with JSON body
2. **For webhooks:** Point to `/api/leads` endpoint
3. **For testing:** Use the `/api/status` endpoint to verify the server is running
4. **Email extraction:** Set to `false` for faster results, `true` for complete contact info
5. **Timeout settings:** Set timeout to at least 5 minutes when `require_email` is true

---

## 📞 **Support**

For issues or questions about the API, check the server logs or contact support.

**API Version:** 1.0.0  
**Last Updated:** November 2, 2025
