"""
Test the API with real query
"""
import requests
import json

url = "http://localhost:5000/api/leads"

data = {
    "query": "Dental clinic, Pune",
    "num_leads": 5,
    "email": "shyammawalweb@gmail.com",
    "require_email": True  # Enable email extraction
}

print("=" * 60)
print("Testing Google Maps Lead Generator")
print("=" * 60)
print(f"Query: {data['query']}")
print(f"Number of Leads: {data['num_leads']}")
print(f"Email: {data['email']}")
print(f"Require Email Extraction: {data['require_email']}")
print("=" * 60)
print("\nSending request to API...")
print("This will take 2-5 minutes as the browser visits websites...")
print("to extract email addresses.\n")

try:
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"Total leads found: {result['count']}")
        print("=" * 60)
        
        for i, lead in enumerate(result['leads'], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Address: {lead['address']}")
            print(f"   Phone: {lead['phone'] or 'N/A'}")
            print(f"   Website: {lead['website'] or 'N/A'}")
            print(f"   Email: {lead['email'] or 'N/A'}")
        
        print("\n" + "=" * 60)
        print(f"Results sent to: {result['email']}")
        print("=" * 60)
        
        # Save to file
        with open('leads_output.json', 'w') as f:
            json.dump(result['leads'], f, indent=2)
        print("\n✅ Results also saved to: leads_output.json")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
