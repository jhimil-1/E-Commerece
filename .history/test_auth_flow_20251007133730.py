#!/usr/bin/env python3
"""
Test script to debug authentication flow and 401 errors
"""
import requests
import json
import sys

def test_auth_flow():
    base_url = "http://localhost:8000"
    
    # Test 1: Try to access protected endpoint without token
    print("=== Test 1: Access without token ===")
    try:
        response = requests.post(f"{base_url}/products/upload", files={"file": ("test.json", "[]", "application/json")})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Login and get token
    print("\n=== Test 2: Login ===")
    login_data = {"username": "testuser1", "password": "testpass123"}
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Token received: {token[:20]}..." if token else "No token received")
            
            # Test 3: Access protected endpoint with token
            print("\n=== Test 3: Access with token ===")
            headers = {"Authorization": f"Bearer {token}"}
            test_products = [{"name": "Test Product", "category": "Ring", "price": 99.99, "description": "A beautiful test ring", "image_url": "https://example.com/image.jpg"}]
            files = {"file": ("test.json", json.dumps(test_products), "application/json")}
            
            response = requests.post(f"{base_url}/products/upload", files=files, headers=headers)
            print(f"Upload status: {response.status_code}")
            print(f"Upload response: {response.text}")
            
            # Test 4: Test token validation
            print("\n=== Test 4: Token validation ===")
            response = requests.get(f"{base_url}/auth/me", headers=headers)
            print(f"Auth check status: {response.status_code}")
            if response.status_code == 200:
                print(f"User info: {response.json()}")
            else:
                print(f"Auth error: {response.text}")
                
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth_flow()