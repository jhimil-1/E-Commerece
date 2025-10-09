#!/usr/bin/env python3
"""
Test script to verify image search functionality after the fix
"""

import requests
import json
import base64
import sys
from pathlib import Path

def test_image_search():
    """Test the image search endpoint with proper FormData"""
    
    # Create a simple test image (1x1 pixel red image)
    test_image_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
    
    session = requests.Session()
    
    try:
        # First, login to get a JWT token
        print("Logging in...")
        login_response = session.post('http://localhost:8000/auth/login', json={
            "username": "test_user_9167a57d",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
        login_data = login_response.json()
        token = login_data.get('access_token')
        print(f"Login successful. Got JWT token: {token[:20]}...")
        
        # Set the Authorization header for subsequent requests
        session.headers.update({'Authorization': f'Bearer {token}'})
        
        # Test image search with FormData
        print("\nTesting image search with FormData...")
        
        # Prepare FormData
        files = {
            'image': ('test_image.png', test_image_data, 'image/png')
        }
        
        data = {
            'limit': '5'
        }
        
        # Send to the correct endpoint
        response = session.post('http://localhost:8000/chat/image-query', files=files, data=data)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Image search successful!")
            print(f"Found {len(result.get('products', []))} products")
            
            if result.get('products'):
                for i, product in enumerate(result.get('products', [])[:3]):
                    print(f"Product {i+1}: {product.get('name', 'Unknown')}")
                    if product.get('description'):
                        print(f"  Description: {product.get('description')[:100]}...")
                    if product.get('image_url'):
                        print(f"  Image URL: {product.get('image_url')}")
            return True
        else:
            print(f"Image search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during test: {e}")
        return False
    finally:
        session.close()

def test_old_broken_way():
    """Test the old broken way to confirm it fails"""
    
    session = requests.Session()
    
    try:
        # Login first
        login_response = session.post('http://localhost:8000/auth/login', json={
            "username": "test_user_9167a57d",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print("Login failed for old way test")
            return False
            
        print("\nTesting old broken way (sending as JSON to /chat/query)...")
        
        # This should fail - sending image data as JSON to wrong endpoint
        test_image_data = base64.b64encode(b'test_image_data').decode('utf-8')
        
        response = session.post('http://localhost:8000/chat/query', json={
            "query": "",  # Empty query
            "imageData": test_image_data,
            "limit": 5
        })
        
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400 and "Query cannot be empty" in response.text:
            print("✓ Confirmed: Old way correctly fails with 'Query cannot be empty'")
            return True
        else:
            print("✗ Unexpected: Old way didn't fail as expected")
            return False
            
    except Exception as e:
        print(f"Error testing old way: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("Testing Image Search Fix")
    print("=" * 50)
    
    # Test the new fixed way
    success = test_image_search()
    
    # Test the old broken way to confirm it fails
    old_way_fails = test_old_broken_way()
    
    print("\n" + "=" * 50)
    if success and old_way_fails:
        print("✓ All tests passed! Image search fix is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Image search may still have issues.")
        sys.exit(1)