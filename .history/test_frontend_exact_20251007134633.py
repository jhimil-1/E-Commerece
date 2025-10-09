#!/usr/bin/env python3
"""
Test script to exactly replicate frontend upload behavior
"""

import requests
import json
import base64

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "test_user_c7665836"
PASSWORD = "test123456"

# Step 1: Login
print("=== Step 1: Login ===")
login_data = {
    "username": USERNAME,
    "password": PASSWORD
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Login status: {response.status_code}")

if response.status_code != 200:
    print(f"Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"Token received: {token[:20]}...")

# Step 2: Test JSON upload (exact frontend format)
print("\n=== Step 2: Test JSON upload (frontend format) ===")

# This is what the frontend sends: { products: [...] }
frontend_data = {
    "products": [
        {
            "name": "Test Ring",
            "category": "Ring",
            "description": "A beautiful test ring",
            "price": 299.99,
            "image_url": "https://example.com/ring.jpg"
        }
    ]
}

# Create JSON file content (this is what the frontend creates internally)
json_content = json.dumps(frontend_data["products"], indent=2)  # Extract just the array
print(f"JSON content being sent: {json_content[:100]}...")

# Create file-like object
import io
json_file = io.BytesIO(json_content.encode('utf-8'))

files = {
    'file': ('products.json', json_file, 'application/json')
}

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.post(f"{BASE_URL}/products/upload", files=files, headers=headers)
print(f"Upload status: {response.status_code}")
print(f"Upload response: {response.text}")

# Step 3: Test with malformed data to see error details
print("\n=== Step 3: Test with malformed data ===")

# Send the wrapped format directly (this should fail)
malformed_content = json.dumps(frontend_data)  # Don't extract the array
malformed_file = io.BytesIO(malformed_content.encode('utf-8'))

malformed_files = {
    'file': ('products.json', malformed_file, 'application/json')
}

response = requests.post(f"{BASE_URL}/products/upload", files=malformed_files, headers=headers)
print(f"Malformed upload status: {response.status_code}")
print(f"Malformed upload response: {response.text}")

print("\n=== Test completed ===")