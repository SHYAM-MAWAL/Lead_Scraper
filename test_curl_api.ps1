# CURL API Test Script
# This script demonstrates all the ways to call the API

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  Google Maps Lead Generator - API Tests" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check API Status
Write-Host "Test 1: Checking API Status..." -ForegroundColor Yellow
Write-Host "Command: GET /api/status" -ForegroundColor Gray
Write-Host ""

$statusResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method GET
Write-Host "Response:" -ForegroundColor Green
$statusResponse | ConvertTo-Json
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Test 2: Generate Leads WITHOUT Email Extraction
Write-Host "Test 2: Generate Leads (WITHOUT email extraction)" -ForegroundColor Yellow
Write-Host "Command: POST /api/leads" -ForegroundColor Gray
Write-Host ""

$body1 = @{
    query = "Coffee shops in London"
    num_leads = 3
    email = "test@example.com"
    require_email = $false
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Magenta
Write-Host $body1 -ForegroundColor Gray
Write-Host ""
Write-Host "Sending request... (This will take 1-3 minutes)" -ForegroundColor Yellow
Write-Host ""

try {
    $response1 = Invoke-RestMethod -Uri "http://localhost:5000/api/leads" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body1

    Write-Host "Response:" -ForegroundColor Green
    Write-Host "Success: $($response1.success)" -ForegroundColor Green
    Write-Host "Total Leads: $($response1.count)" -ForegroundColor Green
    Write-Host ""
    
    foreach ($lead in $response1.leads) {
        Write-Host "  - $($lead.name)" -ForegroundColor White
        Write-Host "    Address: $($lead.address)" -ForegroundColor Gray
        Write-Host "    Phone: $($lead.phone)" -ForegroundColor Gray
        Write-Host "    Website: $($lead.website)" -ForegroundColor Gray
        Write-Host "    Email: $($lead.email)" -ForegroundColor Gray
        Write-Host ""
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Test 3: CURL Command Example (for copying)
Write-Host "Test 3: CURL Command Examples" -ForegroundColor Yellow
Write-Host ""

Write-Host "Linux/Mac CURL Command:" -ForegroundColor Magenta
Write-Host @"
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Dental clinic, Pune",
    "num_leads": 5,
    "email": "your@email.com",
    "require_email": true
  }'
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "Windows CMD CURL Command:" -ForegroundColor Magenta
Write-Host @"
curl -X POST http://localhost:5000/api/leads ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Dental clinic, Pune\", \"num_leads\": 5, \"email\": \"your@email.com\", \"require_email\": true}"
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "PowerShell Command:" -ForegroundColor Magenta
Write-Host @"
`$body = @{
    query = "Dental clinic, Pune"
    num_leads = 5
    email = "your@email.com"
    require_email = `$true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/leads" ``
    -Method POST ``
    -ContentType "application/json" ``
    -Body `$body
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ All test examples completed!" -ForegroundColor Green
Write-Host ""
Write-Host "For more examples, see: CURL_API_DOCS.md" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
