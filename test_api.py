"""
Test script for the Lead Generator API
Run this to test the backend without the web interface
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_status():
    """Test if the API is running"""
    print("Testing API status...")
    response = requests.get(f"{BASE_URL}/api/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_lead_generation():
    """Test lead generation"""
    print("Testing lead generation...")
    
    data = {
        "query": "Coffee shops in New York",
        "num_leads": 5,
        "email": "test@example.com"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/leads",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lead count: {result.get('count')}")
        print(f"\nFirst lead:")
        if result.get('leads'):
            print(json.dumps(result['leads'][0], indent=2))
    else:
        print(f"Error: {response.json()}")
    print()

def test_invalid_request():
    """Test error handling"""
    print("Testing error handling...")
    
    data = {
        "query": "",  # Empty query should fail
        "num_leads": 5,
        "email": "test@example.com"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/leads",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Google Maps Lead Generator - API Tests")
    print("=" * 50)
    print()
    
    try:
        test_status()
        test_lead_generation()
        test_invalid_request()
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server.")
        print("Make sure the Flask app is running with: python app.py")
    except Exception as e:
        print(f"ERROR: {e}")
