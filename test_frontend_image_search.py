#!/usr/bin/env python3
"""
Test script to simulate the frontend image search functionality
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image

def create_test_image_base64(width=100, height=100, color=(255, 0, 0)):
    """Create a test image and return as base64"""
    img = Image.new('RGB', (width, height), color)
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def test_frontend_image_search():
    base_url = "http://localhost:8000"
    
    # Step 1: Login
    print("Step 1: Logging in...")
    login_data = {
        "username": "test_user_9167a57d",
        "password": "test123456"
    }
    
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data.get("access_token")
    print(f"Got JWT token: {access_token[:20]}...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Step 2: Create chat session
    print("\nStep 2: Creating chat session...")
    response = requests.post(f"{base_url}/chat/sessions", headers=headers)
    if response.status_code not in [200, 201]:
        print(f"Session creation failed: {response.status_code} - {response.text}")
        return
    
    session_data = response.json()
    session_id = session_data.get("session_id")
    print(f"Got session: {session_id}")
    
    # Step 3: Test the OLD way (JSON with base64) - should fail
    print("\nStep 3: Testing OLD way (JSON with base64) - should fail...")
    
    image_base64 = create_test_image_base64(100, 100, (0, 0, 255))  # Blue image
    
    # This simulates the old broken frontend method
    old_request_data = {
        "session_id": session_id,
        "query": "blue jewelry",
        "image": image_base64
    }
    
    response = requests.post(
        f"{base_url}/chat/query",  # Wrong endpoint!
        headers={**headers, "Content-Type": "application/json"},
        json=old_request_data
    )
    
    print(f"Old method response: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected failure: {response.text}")
    else:
        print("Unexpected success - this should have failed!")
    
    # Step 4: Test the NEW way (FormData) - should work
    print("\nStep 4: Testing NEW way (FormData) - should work...")
    
    # Create image bytes for FormData
    img = Image.new('RGB', (100, 100), (0, 0, 255))  # Blue image
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # This simulates the new fixed frontend method
    form_data = {
        'session_id': session_id,
        'query': 'blue jewelry',
        'category': 'rings'
    }
    
    files = {
        'image': ('image.png', img_buffer.getvalue(), 'image/png')
    }
    
    response = requests.post(
        f"{base_url}/chat/image-query",  # Correct endpoint!
        headers=headers,
        data=form_data,
        files=files
    )
    
    print(f"New method response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Found {len(result.get('products', []))} products")
        print(f"Response: {result.get('response', 'No response')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_frontend_image_search()