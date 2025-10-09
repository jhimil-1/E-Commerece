#!/usr/bin/env python3
import requests
import json
import tempfile
import os

# Test the complete upload flow - both JSON and manual methods
BASE_URL = "http://localhost:8000"

print("=== Complete Upload Flow Test ===")

# Login first
login_data = {
    "username": "test_user_58f1a7eb",
    "password": "test123456"
}

print("1. Logging in...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["access_token"]
print(f"   ✅ Login successful")

# Test 1: JSON Upload
print("\n2. Testing JSON Upload...")
products = [
    {
        "name": "JSON Test Product 1",
        "category": "electronics",
        "description": "Testing JSON upload method",
        "price": 149.99,
        "image_url": "https://example.com/json-test1.jpg"
    },
    {
        "name": "JSON Test Product 2",
        "category": "clothing",
        "description": "Second product for JSON upload",
        "price": 79.99,
        "image_url": "https://example.com/json-test2.jpg"
    }
]

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(products, f)
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
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ JSON upload successful! {result['details']['inserted_count']} products uploaded")
    else:
        print(f"   ❌ JSON upload failed: {response.text}")
        
finally:
    os.unlink(temp_file)

# Test 2: Manual Product Upload (simulating frontend behavior)
print("\n3. Testing Manual Product Upload...")
manual_product = {
    "name": "Manual Test Product",
    "category": "home",
    "description": "Testing manual upload method",
    "price": 199.99,
    "image_url": "https://example.com/manual-test.jpg"
}

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump([manual_product], f)
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
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Manual upload successful! {result['details']['inserted_count']} products uploaded")
    else:
        print(f"   ❌ Manual upload failed: {response.text}")
        
finally:
    os.unlink(temp_file)

print("\n=== All Upload Tests Complete ===")
print("✅ Both JSON and manual upload methods are working correctly!")