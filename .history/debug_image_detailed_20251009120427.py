#!/usr/bin/env python3
"""
Detailed debug script to understand image search failure
"""

import requests
import json
import base64
import traceback

def detailed_debug():
    """Detailed debugging of image search"""
    
    session = requests.Session()
    
    try:
        # Login
        print("Step 1: Logging in...")
        login_response = session.post('http://localhost:8000/auth/login', json={
            "username": "test_user_9167a57d",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.text}")
            return False
            
        token = login_response.json().get('access_token')
        session.headers.update({'Authorization': f'Bearer {token}'})
        print(f"Got JWT token: {token[:30]}...")
        
        # Create session
        print("\nStep 2: Creating chat session...")
        session_response = session.post('http://localhost:8000/chat/sessions')
        
        if session_response.status_code not in [200, 201]:
            print(f"Session creation failed: {session_response.text}")
            return False
            
        session_id = session_response.json()['session_id']
        print(f"Created session: {session_id}")
        
        # Test different image types
        print("\nStep 3: Testing different image formats...")
        
        # Test 1: Very small valid PNG (1x1 red pixel)
        print("\nTest 1: 1x1 PNG red pixel")
        small_png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
        
        files = {'image': ('test.png', small_png, 'image/png')}
        data = {'session_id': session_id, 'query': '', 'limit': '2'}
        
        try:
            response = session.post('http://localhost:8000/chat/image-query', files=files, data=data)
            print(f"Response: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")
        
        # Test 2: Slightly larger but still small image (2x2 PNG)
        print("\nTest 2: 2x2 PNG")
        small_png2 = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABM5U7kAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAABZJREFUeNpi/P//PwM6DgYkGZkYGBgAAQYA2tQBZfQhdaMAAAAASUVORK5CYII=')
        
        files = {'image': ('test2.png', small_png2, 'image/png')}
        try:
            response = session.post('http://localhost:8000/chat/image-query', files=files, data=data)
            print(f"Response: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")
        
        # Test 3: Test with invalid session to see if error changes
        print("\nTest 3: Invalid session ID")
        data_invalid = {'session_id': 'invalid-session-123', 'query': '', 'limit': '2'}
        files = {'image': ('test.png', small_png, 'image/png')}
        
        try:
            response = session.post('http://localhost:8000/chat/image-query', files=files, data=data_invalid)
            print(f"Response: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")
            
        # Test 4: Test without image file
        print("\nTest 4: Missing image file")
        try:
            response = session.post('http://localhost:8000/chat/image-query', data=data)
            print(f"Response: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")
            
        # Test 5: Test with wrong content type
        print("\nTest 5: Wrong content type")
        files = {'image': ('test.txt', b'not an image', 'text/plain')}
        try:
            response = session.post('http://localhost:8000/chat/image-query', files=files, data=data)
            print(f"Response: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")
            
    except Exception as e:
        print(f"Error during test: {e}")
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("Detailed Image Search Debug")
    print("=" * 60)
    
    detailed_debug()
    
    print("\n" + "=" * 60)
    print("Debug completed.")