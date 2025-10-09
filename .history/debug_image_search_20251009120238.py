#!/usr/bin/env python3
"""
Simple test to check what's wrong with image search
"""

import requests
import json
import base64

def debug_image_search():
    """Debug the image search step by step"""
    
    session = requests.Session()
    
    try:
        # First, login to get a JWT token
        print("Step 1: Logging in...")
        login_response = session.post('http://localhost:8000/auth/login', json={
            "username": "test_user_9167a57d",
            "password": "test123456"
        })
        
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.text}")
            return False
            
        login_data = login_response.json()
        token = login_data.get('access_token')
        print(f"Got JWT token: {token[:30]}...")
        
        # Set the Authorization header for subsequent requests
        session.headers.update({'Authorization': f'Bearer {token}'})
        
        # Test a simple text query first to make sure basic chat works
        print("\nStep 2: Testing basic text query...")
        text_response = session.post('http://localhost:8000/chat/query', json={
            "session_id": "test-session-123",
            "query": "laptop",
            "limit": 5
        })
        
        print(f"Text query status: {text_response.status_code}")
        if text_response.status_code == 200:
            text_data = text_response.json()
            print(f"Text query successful! Found {len(text_data.get('products', []))} products")
        else:
            print(f"Text query failed: {text_response.text}")
        
        # Now test image search
        print("\nStep 3: Testing image search...")
        
        # Create a simple test image (1x1 pixel red image)
        test_image_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
        
        # Prepare FormData
        files = {
            'image': ('test_image.png', test_image_data, 'image/png')
        }
        
        data = {
            'session_id': 'test-session-123',
            'query': '',  # Optional text query
            'limit': '5'
        }
        
        print(f"Sending request to /chat/image-query...")
        print(f"Files: {list(files.keys())}")
        print(f"Data: {data}")
        
        response = session.post('http://localhost:8000/chat/image-query', files=files, data=data)
        
        print(f"Image search status: {response.status_code}")
        print(f"Image search response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Image search successful!")
            print(f"Found {len(result.get('products', []))} products")
            return True
        else:
            print(f"Image search failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("Debugging Image Search")
    print("=" * 50)
    
    success = debug_image_search()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ Image search is working!")
    else:
        print("✗ Image search has issues.")