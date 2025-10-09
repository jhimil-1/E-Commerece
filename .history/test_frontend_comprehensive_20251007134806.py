#!/usr/bin/env python3
"""
Comprehensive test to verify frontend upload formats work correctly
"""

import requests
import json
import io

BASE_URL = "http://localhost:8000"
USERNAME = "test_user_c7665836"
PASSWORD = "test123456"

def login():
    """Login and return token"""
    login_data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Login failed: {response.text}")

def upload_products(token, products_data, description):
    """Upload products and return result"""
    print(f"\n=== Testing {description} ===")
    
    # Create JSON file content
    json_content = json.dumps(products_data, indent=2)
    print(f"Content format: {json_content[:100]}...")
    
    json_file = io.BytesIO(json_content.encode('utf-8'))
    
    files = {'file': ('products.json', json_file, 'application/json')}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f"{BASE_URL}/products/upload", files=files, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

def main():
    """Main test function"""
    print("=== Frontend Upload Format Tests ===")
    
    # Login
    token = login()
    print(f"Logged in successfully")
    
    # Test 1: Direct array format (what backend expects)
    direct_array = [
        {
            "name": "Direct Array Ring",
            "category": "Ring", 
            "description": "Test ring from direct array",
            "price": 299.99,
            "image_url": "https://example.com/direct.jpg"
        }
    ]
    
    success1 = upload_products(token, direct_array, "Direct Array Format")
    
    # Test 2: Frontend wrapped format (what frontend sends)
    frontend_wrapped = {
        "products": [
            {
                "name": "Frontend Ring",
                "category": "Ring",
                "description": "Test ring from frontend format", 
                "price": 199.99,
                "image_url": "https://example.com/frontend.jpg"
            }
        ]
    }
    
    success2 = upload_products(token, frontend_wrapped, "Frontend Wrapped Format")
    
    # Test 3: Multiple products in frontend format
    multiple_products = {
        "products": [
            {
                "name": "Ring 1",
                "category": "Ring",
                "description": "First test ring",
                "price": 150.00,
                "image_url": "https://example.com/ring1.jpg"
            },
            {
                "name": "Necklace 1", 
                "category": "Necklace",
                "description": "First test necklace",
                "price": 250.00,
                "image_url": "https://example.com/necklace1.jpg"
            }
        ]
    }
    
    success3 = upload_products(token, multiple_products, "Multiple Products Frontend Format")
    
    # Summary
    print("\n=== Test Results ===")
    print(f"Direct Array Format: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"Frontend Wrapped Format: {'✓ PASS' if success2 else '✗ FAIL'}")  
    print(f"Multiple Products Format: {'✓ PASS' if success3 else '✗ FAIL'}")
    
    if success1 and not success2:
        print("\n⚠️  ISSUE CONFIRMED: Backend expects direct array, frontend sends wrapped format")
        print("However, frontend's uploadProducts method should extract the array correctly.")
    elif success1 and success2:
        print("\n✓ All formats work correctly!")
    else:
        print("\n⚠️  Unexpected results - further investigation needed")

if __name__ == "__main__":
    main()