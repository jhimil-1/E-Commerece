#!/usr/bin/env python3
import requests
import json

# Test the complete authentication and upload flow like the frontend would
BASE_URL = "http://localhost:8000"

print("=== Testing Frontend Authentication Flow ===")

# Step 1: Login (like the frontend does)
login_data = {
    "username": "test_user_58f1a7eb",
    "password": "test123456"
}

print(f"1. Logging in with: {login_data}")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"   Status: {response.status_code}")

if response.status_code != 200:
    print(f"   ❌ Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"   ✅ Login successful, token: {token[:30]}...")

# Step 2: Test the uploadProducts API method (like the frontend does)
print("\n2. Testing uploadProducts API method...")

# Create a JSON file for upload (like the frontend does)
products_data = [{
    "name": "Frontend Test Product",
    "category": "test",
    "description": "Testing frontend upload method",
    "price": 29.99,
    "image_url": "https://example.com/frontend-test.jpg"
}]

# Create FormData with JSON file (like the frontend does)
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(products_data, f)
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
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Upload successful!")
        print(f"   - Products uploaded: {result.get('details', {}).get('inserted_count', 0)}")
    else:
        print(f"   ❌ Upload failed: {response.text}")
        
finally:
    os.unlink(temp_file)

print("\n=== Frontend Authentication Test Complete ===")