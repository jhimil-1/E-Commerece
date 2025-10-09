#!/usr/bin/env python3
"""
Final integration test to verify all fixes are working correctly
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image
import os

def test_authentication():
    """Test user authentication"""
    print("Testing authentication...")
    
    # Test login
    login_data = {
        "username": "testuser1",
        "password": "password123"
    }
    
    response = requests.post('http://localhost:8000/auth/login', json=login_data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Login successful")
            token = result.get('token')
            return token
        else:
            print(f"❌ Login failed: {result.get('error')}")
            return None
    else:
        print(f"❌ Login request failed: {response.status_code}")
        return None

def create_session(token):
    """Create a chat session"""
    print("Creating session...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post('http://localhost:8000/chat/sessions', headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        session_id = result.get('session_id')
        print(f"✅ Session created: {session_id}")
        return session_id
    else:
        print(f"❌ Session creation failed: {response.status_code}")
        return None

def test_text_search(token, session_id):
    """Test text search functionality"""
    print("\nTesting text search...")
    
    headers = {'Authorization': f'Bearer {token}'}
    search_data = {
        "query": "smartphone",
        "session_id": session_id
    }
    
    response = requests.post('http://localhost:8000/chat/query', json=search_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            products = result.get('products', [])
            print(f"✅ Text search successful - found {len(products)} results")
            if products:
                print(f"   First result: {products[0].get('name', 'N/A')}")
            return True
        else:
            print(f"❌ Text search failed: {result.get('response', 'Unknown error')}")
            return False
    else:
        print(f"❌ Text search request failed: {response.status_code}")
        return False

def test_category_filtering(token, session_id):
    """Test category filtering"""
    print("\nTesting category filtering...")
    
    headers = {'Authorization': f'Bearer {token}'}
    search_data = {
        "query": "smartphones in electronics category",
        "session_id": session_id
    }
    
    response = requests.post('http://localhost:8000/chat/query', json=search_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            products = result.get('products', [])
            print(f"✅ Category filtering successful - found {len(products)} results")
            if products:
                categories = [p.get('category', 'N/A') for p in products[:3]]
                print(f"   Sample categories: {categories}")
            return True
        else:
            print(f"❌ Category filtering failed: {result.get('response', 'Unknown error')}")
            return False
    else:
        print(f"❌ Category filtering request failed: {response.status_code}")
        return False

def test_json_upload(token):
    """Test JSON upload functionality"""
    print("\nTesting JSON upload...")
    
    # Create test product data
    test_products = [
        {
            "name": "Test Product 1",
            "description": "A test product for integration testing",
            "price": 99.99,
            "category": "Electronics",
            "image_url": "https://example.com/test1.jpg"
        },
        {
            "name": "Test Product 2", 
            "description": "Another test product",
            "price": 149.99,
            "category": "Home",
            "image_url": "https://example.com/test2.jpg"
        }
    ]
    
    headers = {'Authorization': f'Bearer {token}'}
    upload_data = {"products": test_products}
    
    
    # Convert to file upload format expected by the API
    files = {'file': ('products.json', json.dumps(upload_data), 'application/json')}
    response = requests.post('http://localhost:8000/products/upload', files=files, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            details = result.get('details', {})
            print(f"✅ JSON upload successful - inserted {details.get('inserted_count', 0)} products")
            return True
        else:
            print(f"❌ JSON upload failed: {result.get('error')}")
            return False
    else:
        print(f"❌ JSON upload request failed: {response.status_code}")
        return False

def test_image_search(token, session_id):
    """Test image search functionality"""
    print("\nTesting image search...")
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    headers = {'Authorization': f'Bearer {token}'}
    files = {'image': ('test.png', img_buffer, 'image/png')}
    data = {'session_id': session_id, 'query': 'red colored item'}
    
    response = requests.post('http://localhost:8000/chat/image-query', files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            products = result.get('products', [])
            print(f"✅ Image search successful - found {len(products)} results")
            return True
        else:
            print(f"❌ Image search failed: {result.get('response', 'Unknown error')}")
            return False
    else:
        print(f"❌ Image search request failed: {response.status_code}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting final integration test...\n")
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("❌ Authentication failed - cannot proceed with other tests")
        return
    
    tests_passed = 0
    total_tests = 4
    
    # Test text search
    if test_text_search(token):
        tests_passed += 1
    
    # Test category filtering
    if test_category_filtering(token):
        tests_passed += 1
    
    # Test JSON upload
    if test_json_upload(token):
        tests_passed += 1
    
    # Test image search
    if test_image_search(token):
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The application is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the application.")

if __name__ == "__main__":
    main()