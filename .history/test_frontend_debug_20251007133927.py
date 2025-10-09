#!/usr/bin/env python3
"""
Test script to debug frontend authentication issues
"""
import requests
import json
import time

def test_frontend_like_upload():
    base_url = "http://localhost:8000"
    
    # Step 1: Login
    print("=== Step 1: Login ===")
    login_data = {"username": "testuser1", "password": "testpass123"}
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    print(f"Login status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token = response.json().get("access_token")
    print(f"Token received: {token[:30]}...")
    
    # Step 2: Test upload with exact frontend format
    print("\n=== Step 2: Test frontend-like upload ===")
    
    # Create product data exactly like the frontend does
    product_data = {
        "products": [{
            "name": "Test Ring",
            "category": "Ring", 
            "description": "A beautiful test ring",
            "price": 299.99,
            "image_url": "https://example.com/ring.jpg"
        }]
    }
    
    # Convert to JSON and create file like frontend does
    json_content = json.dumps(product_data, indent=2)
    print(f"JSON content being sent:\n{json_content}")
    
    files = {
        "file": ("products.json", json_content, "application/json")
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"Headers: {headers}")
    print(f"Files: {files}")
    
    response = requests.post(f"{base_url}/products/upload", files=files, headers=headers)
    print(f"Upload status: {response.status_code}")
    print(f"Upload response: {response.text}")
    
    # Step 3: Test with direct array format
    print("\n=== Step 3: Test direct array format ===")
    
    # Test with direct array (backend expects this)
    direct_array = [{
        "name": "Test Ring 2",
        "category": "Ring", 
        "description": "Another beautiful test ring",
        "price": 399.99,
        "image_url": "https://example.com/ring2.jpg"
    }]
    
    json_content2 = json.dumps(direct_array, indent=2)
    files2 = {
        "file": ("products.json", json_content2, "application/json")
    }
    
    response2 = requests.post(f"{base_url}/products/upload", files=files2, headers=headers)
    print(f"Direct array upload status: {response2.status_code}")
    print(f"Direct array upload response: {response2.text}")

if __name__ == "__main__":
    test_frontend_like_upload()