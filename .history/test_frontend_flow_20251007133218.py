#!/usr/bin/env python3
import requests
import json
import tempfile
import os

# Test the exact frontend flow
BASE_URL = "http://localhost:8000"

print("=== Testing Frontend Authentication Flow ===")

# Step 1: Login like the frontend does
print("1. Logging in...")
login_data = {
    "username": "test_user_58f1a7eb",
    "password": "test123456"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code != 200:
    print(f"   ❌ Login failed: {response.status_code} - {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"   ✅ Login successful, token: {token[:30]}...")

# Step 2: Test the exact manual product upload like frontend
print("\n2. Testing manual product upload (frontend format)...")

# This is what the frontend sends: { products: [product] }
frontend_data = {
    "products": [{
        "name": "Manual Test Product",
        "category": "home", 
        "description": "Testing manual upload method",
        "price": 199.99,
        "image_url": "https://example.com/manual-test.jpg"
    }]
}

# Extract products array like frontend does
products_array = frontend_data["products"]

# Create JSON file like frontend does
json_content = json.dumps(products_array, indent=2)
print(f"   JSON content being sent:")
print(json_content)

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(products_array, f)
    temp_file = f.name

try:
    with open(temp_file, 'rb') as f:
        files = {'file': ('products.json', f, 'application/json')}
        headers = {'Authorization': f'Bearer {token}'}
        
        print(f"\n3. Making request with Authorization header...")
        response = requests.post(
            f"{BASE_URL}/products/upload",
            files=files,
            headers=headers
        )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    
    if response.status_code != 200:
        print(f"\n4. Error analysis:")
        print(f"   Headers sent: {headers}")
        print(f"   Token length: {len(token)}")
        print(f"   Token format: Bearer {token[:20]}...")
        
finally:
    os.unlink(temp_file)

# Step 3: Test direct array format (what backend expects)
print(f"\n5. Testing direct array format (backend format)...")

direct_array = [{
    "name": "Direct Array Product",
    "category": "electronics",
    "description": "Testing direct array format",
    "price": 299.99,
    "image_url": "https://example.com/direct-test.jpg"
}]

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(direct_array, f)
    temp_file = f.name

try:
    with open(temp_file, 'rb') as f:
        files = {'file': ('products.json', f, 'application/json')}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/products/upload",
            files=files,
            headers=headers
        )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    
finally:
    os.unlink(temp_file)