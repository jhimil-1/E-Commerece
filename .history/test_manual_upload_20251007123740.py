#!/usr/bin/env python3
import requests
import json
import tempfile
import os

# Test manual product upload
BASE_URL = "http://localhost:8000"

# Login first
login_data = {
    "username": "test_user_58f1a7eb",
    "password": "test123456"
}

print("Logging in...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code != 200:
    print(f"Login failed: {response.status_code} - {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"Login successful, token: {token[:20]}...")

# Create a sample product with image_url
product = {
    "name": "Test Product",
    "category": "electronics",
    "description": "A test product for manual upload",
    "price": 99.99,
    "image_url": "https://example.com/test-image.jpg"
}

# Create temporary JSON file
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump([product], f)
    temp_file = f.name

try:
    print(f"Uploading product: {product}")
    
    # Upload as file
    with open(temp_file, 'rb') as f:
        files = {'file': ('products.json', f, 'application/json')}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/products/upload",
            files=files,
            headers=headers
        )
    
    print(f"Response status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Product uploaded successfully!")
        print(f"Inserted count: {result.get('details', {}).get('inserted_count', 0)}")
        print(f"Product IDs: {result.get('details', {}).get('product_ids', [])}")
    else:
        print(f"❌ Upload failed: {response.text}")
        
finally:
    # Clean up temporary file
    os.unlink(temp_file)