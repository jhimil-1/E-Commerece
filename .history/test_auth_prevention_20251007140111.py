#!/usr/bin/env python3
"""
Test script to verify authentication prevention works correctly
"""

import requests
import json

# Test API endpoints directly
BASE_URL = "http://localhost:8000"

def test_upload_without_auth():
    """Test that upload fails without authentication"""
    print("=== Testing Upload Without Authentication ===")
    
    # Test data
    test_product = {
        "products": [{
            "name": "Test Ring",
            "category": "Ring", 
            "description": "Test ring without auth",
            "price": 299.99,
            "image_url": "https://example.com/ring.jpg"
        }]
    }
    
    try:
        # Try to upload without authentication
        response = requests.post(
            f"{BASE_URL}/products/upload",
            json=test_product,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✓ PASS: Upload correctly blocked without authentication")
            return True
        else:
            print("✗ FAIL: Upload should be blocked without authentication")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def test_upload_with_auth():
    """Test that upload works with authentication"""
    print("\n=== Testing Upload With Authentication ===")
    
    # First login
    login_data = {
        "username": "test_user_c7665836",
        "password": "test123456"
    }
    
    try:
        # Login to get token
        login_response = requests.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"✗ FAIL: Login failed with status {login_response.status_code}")
            return False
            
        token = login_response.json().get("access_token")
        if not token:
            print("✗ FAIL: No token received")
            return False
            
        print("✓ Login successful")
        
        # Test data
        test_product = {
            "products": [{
                "name": "Auth Test Ring",
                "category": "Ring",
                "description": "Test ring with auth",
                "price": 199.99,
                "image_url": "https://example.com/auth-ring.jpg"
            }]
        }
        
        # Try to upload with authentication
        response = requests.post(
            f"{BASE_URL}/products/upload",
            json=test_product,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ PASS: Upload works with authentication")
            return True
        else:
            print("✗ FAIL: Upload should work with authentication")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing Authentication Prevention...")
    
    test1 = test_upload_without_auth()
    test2 = test_upload_with_auth()
    
    if test1 and test2:
        print("\n✓ All authentication tests passed!")
    else:
        print("\n✗ Some authentication tests failed!")