# n8n HTTP Node Setup Guide

## 🎯 Quick Fix for Your Error

**Error:** `'>' not supported between instances of 'str' and 'int'`

**Cause:** n8n was sending `num_leads` as a string instead of a number

**Solution:** ✅ Backend now automatically converts string to integer

---

## 🔧 n8n HTTP Request Node Configuration

### Option 1: Import from CURL (Recommended)

1. Add **HTTP Request** node to your workflow
2. Click **"Import cURL Command"**
3. Paste this command:

```bash
curl -X POST http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads \
  -H "Content-Type: application/json" \
  -d '{"query": "Dental clinic, Pune", "num_leads": 1, "email": "shyammawalweb@gmail.com", "require_email": false}'
```

4. After import, **verify** the JSON body shows numbers without quotes:
   - ✅ Good: `"num_leads": 1`
   - ❌ Bad: `"num_leads": "1"`

5. Click **"Execute Node"** to test

---

### Option 2: Manual Configuration

**Step 1: Basic Settings**
- **Method:** `POST`
- **URL:** `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads`

**Step 2: Authentication**
- **Authentication:** `None`

**Step 3: Send Body**
- **Send Body:** `Yes` ✅
- **Body Content Type:** `JSON`

**Step 4: Specify Body**
- **Specify Body:** `Using JSON`

**Step 5: Add JSON Parameters**

Click **"Add Field"** and add these:

| Field Name | Value | Type |
|------------|-------|------|
| `query` | `Dental clinic, Pune` | Expression: `{{ $json.query }}` |
| `num_leads` | `5` | Expression: `{{ $json.num_leads }}` |
| `email` | `shyammawalweb@gmail.com` | Expression: `{{ $json.email }}` |
| `require_email` | `false` | Expression: `{{ $json.require_email }}` |

---

### Option 3: Using JSON Editor

1. Toggle to **"JSON"** mode
2. Paste this:

```json
{
  "query": "Dental clinic, Pune",
  "num_leads": 5,
  "email": "shyammawalweb@gmail.com",
  "require_email": false
}
```

**⚠️ CRITICAL:**
- `num_leads` must be a **NUMBER** (no quotes)
- `require_email` must be a **BOOLEAN** (true/false, no quotes)

---

## 🔄 Using Variables from Previous Nodes

If you want to use data from previous nodes:

```json
{
  "query": "{{ $json.searchQuery }}",
  "num_leads": {{ $json.numberOfLeads }},
  "email": "{{ $json.userEmail }}",
  "require_email": {{ $json.extractEmails }}
}
```

**Note:** No quotes around `{{ }}` for numbers and booleans!

---

## 📊 Expected Response

**Success (200 OK):**
```json
{
  "success": true,
  "leads": [
    {
      "name": "Deccan Dental Clinic",
      "address": "759/53, 1st floor, Fergusson College Rd, Pune",
      "phone": "+91 73870 40464",
      "website": "http://www.bestorthodontistbracespune.in/",
      "email": ""
    }
  ],
  "count": 5,
  "email": "shyammawalweb@gmail.com"
}
```

**Error (400/500):**
```json
{
  "error": "Query is required"
}
```

---

## 🐛 Troubleshooting

### Error: `'>' not supported between instances of 'str' and 'int'`

**Solution:** ✅ Already fixed! Backend now handles string conversion.

But to prevent this, ensure in n8n:
- Don't wrap numbers in quotes in JSON mode
- Use Number type when adding fields manually

### Error: `Query is required`

**Solution:** Make sure `query` field is not empty

### Error: `Email is required`

**Solution:** Add `email` parameter to the request

### No response / Timeout

**Causes:**
- Without email extraction: Takes 1-3 minutes ⏱️
- With email extraction: Takes 2-5 minutes ⏱️

**Solution:** 
1. In n8n HTTP Request node settings
2. Go to **"Options"**
3. Set **"Timeout"** to `300000` (5 minutes)

---

## 🚀 Complete n8n Workflow Example

### Workflow: Google Maps Lead Generator

**Node 1: Manual Trigger**
- Trigger the workflow manually

**Node 2: Set Variables**
- Add **"Set"** node
- Add these values:
  - `searchQuery`: "Dental clinic, Pune"
  - `numberOfLeads`: `5` (number)
  - `userEmail`: "shyammawalweb@gmail.com"
  - `extractEmails`: `false` (boolean)

**Node 3: HTTP Request (Lead Scraper)**
- Method: POST
- URL: `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads`
- Body:
```json
{
  "query": "{{ $json.searchQuery }}",
  "num_leads": {{ $json.numberOfLeads }},
  "email": "{{ $json.userEmail }}",
  "require_email": {{ $json.extractEmails }}
}
```

**Node 4: Process Results**
- Add **"Split Out"** node
- Split: `{{ $json.leads }}`
- This creates one item per lead

**Node 5: Google Sheets (Optional)**
- Add leads to spreadsheet
- Map fields: name, address, phone, website, email

---

## 📋 Request Parameters Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | ✅ Yes | - | Search query (e.g., "Coffee shops in London") |
| `num_leads` | **Number** | ✅ Yes | 20 | Number of leads (1-100) |
| `email` | String | ✅ Yes | - | Your email address |
| `require_email` | Boolean | ❌ No | false | Extract emails from websites |

---

## ⚡ Performance Tips

### Fast Scraping (1-3 minutes)
```json
{
  "query": "Dental clinic, Pune",
  "num_leads": 5,
  "email": "your@email.com",
  "require_email": false
}
```

### Complete Data with Emails (2-5 minutes)
```json
{
  "query": "Dental clinic, Pune",
  "num_leads": 5,
  "email": "your@email.com",
  "require_email": true
}
```

---

## 🔗 Production URLs

- **API Endpoint:** `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/leads`
- **Status Check:** `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/status`
- **Debug Info:** `http://hgck40g4go4c800kk08wow00.185.245.182.223.sslip.io/api/debug`

---

## ✅ Test Your Setup

Before running full workflows, test with:

```json
{
  "query": "Coffee shop, Pune",
  "num_leads": 1,
  "email": "shyammawalweb@gmail.com",
  "require_email": false
}
```

Expected: 1 real coffee shop from Pune in ~1 minute

---

## 📞 Need Help?

- Check `/api/status` to verify server is running
- Check `/api/debug` to see API key configuration
- Review n8n execution logs for detailed error messages
- Ensure timeout is set to 5 minutes minimum

**Last Updated:** November 2, 2025
