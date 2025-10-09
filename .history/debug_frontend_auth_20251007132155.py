#!/usr/bin/env python3
"""
Debug script to test frontend authentication and upload flow
"""
import requests
import json
import tempfile
import os

def test_frontend_auth_flow():
    """Test the complete frontend authentication and upload flow"""
    
    # Test credentials
    test_username = "test_user_debug"
    test_password = "test123456"
    
    print("=== Frontend Authentication Debug ===")
    
    # 1. Create test user if not exists
    print("1. Creating test user...")
    signup_data = {
        "username": test_username,
        "email": f"{test_username}@example.com",
        "password": test_password
    }
    
    response = requests.post('http://localhost:8000/auth/signup', json=signup_data)
    if response.status_code == 200:
        print("   ✅ Test user created")
    else:
        print(f"   ⚠️  User might already exist: {response.text}")
    
    # 2. Login to get token
    print("2. Logging in to get token...")
    login_data = {
        "username": test_username,
        "password": test_password
    }
    
    response = requests.post('http://localhost:8000/auth/login', json=login_data)
    if response.status_code != 200:
        print(f"   ❌ Login failed: {response.text}")
        return False
    
    login_result = response.json()
    token = login_result.get('access_token')
    if not token:
        print("   ❌ No token received")
        return False
    
    print(f"   ✅ Login successful, token: {token[:50]}...")
    
    # 3. Test manual upload with frontend format
    print("3. Testing manual upload format...")
    
    # Create product data in frontend format (object with products property)
    product_data = {
        "products": [{
            "name": "Debug Test Product",
            "category": "debug",
            "description": "Testing frontend authentication",
            "price": 19.99,
            "image_url": "https://example.com/debug-test.jpg"
        }]
    }
    
    # Create temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(product_data, f)
        temp_file = f.name
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'file': ('products.json', f, 'application/json')}
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.post('http://localhost:8000/products/upload', 
                                   files=files, headers=headers)
            
            print(f"   Manual upload status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Manual upload successful")
                result = response.json()
                print(f"   Inserted count: {result.get('details', {}).get('inserted_count', 0)}")
            else:
                print("   ❌ Manual upload failed")
                return False
    
    finally:
        os.unlink(temp_file)
    
    # 4. Test token validation
    print("4. Testing token validation...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:8000/chat/sessions', headers=headers)
    print(f"   Token validation status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Token is valid")
    else:
        print("   ❌ Token validation failed")
        print(f"   Response: {response.text}")
    
    print("\n=== Debug Complete ===")
    return True

if __name__ == "__main__":
    test_frontend_auth_flow()