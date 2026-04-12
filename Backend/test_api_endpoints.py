"""
Test backend API endpoints
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*70)
print("TESTING BACKEND API ENDPOINTS")
print("="*70 + "\n")

# Test 1: Health check
print("Test 1: Health Check")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    try:
        data = response.json()
        print(f"Valid JSON: YES")
        print(f"Data: {data}")
    except:
        print(f"Valid JSON: NO")
except Exception as e:
    print(f"ERROR: {e}")

print("\n")

# Test 2: Recommendations endpoint
print("Test 2: Recommendations Endpoint")
print("-" * 70)
try:
    url = f"{BASE_URL}/recommendations?emotion=happy"
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'NOT SET')}")
    print(f"Response length: {len(response.text)} chars")
    print(f"First 300 chars: {response.text[:300]}")
    
    try:
        data = response.json()
        print(f"\nValid JSON: YES")
        print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'NOT A DICT'}")
        if "recommendations" in data:
            print(f"Number of recommendations: {len(data['recommendations'])}")
            if data['recommendations']:
                print(f"First song: {data['recommendations'][0]}")
    except json.JSONDecodeError as e:
        print(f"\nValid JSON: NO")
        print(f"JSON Error: {e}")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*70 + "\n")
