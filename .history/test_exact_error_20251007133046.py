#!/usr/bin/env python3
import requests
import json
import tempfile
import os

# Test the exact error that's happening
BASE_URL = "http://localhost:8000"

# Login first
login_data = {
    "username": "test_user_58f1a7eb",
    "password": "test123456"
}

print("=== Testing Exact Error ===")
print("1. Logging in...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["access_token"]
print(f"   ✅ Login successful, token: {token[:30]}...")

# Test manual product upload with the exact format from frontend
manual_product = {
    "name": "Manual Test Product",
    "category": "home",
    "description": "Testing manual upload method",
    "price": 199.99,
    "image_url": "https://example.com/manual-test.jpg"
}

# Create the exact file that frontend would create
products_array = [manual_product]
json_content = json.dumps(products_array, indent=2)
print(f"\n2. JSON content being sent:")
print(json_content)

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(products_array, f)
    temp_file = f.name

try:
    with open(temp_file, 'rb') as f:
        files = {'file': ('products.json', f, 'application/json')}
        headers = {'Authorization': f'Bearer {token}'}
        
        print(f"\n3. Making request...")
        response = requests.post(
            f"{BASE_URL}/products/upload",
            files=files,
            headers=headers
        )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    
    if response.status_code != 200:
        print(f"\n4. Error details:")
        try:
            error_data = response.json()
            print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
finally:
    os.unlink(temp_file)