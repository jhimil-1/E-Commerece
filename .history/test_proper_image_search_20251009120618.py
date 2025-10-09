#!/usr/bin/env python3
"""
Test script to verify image search functionality with properly sized images
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image

def create_test_image(width=100, height=100, color=(255, 0, 0)):
    """Create a proper test image"""
    img = Image.new('RGB', (width, height), color)
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer.getvalue()

def test_image_search():
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
    if response.status_code != 200:
        print(f"Session creation failed: {response.status_code} - {response.text}")
        return
    
    session_data = response.json()
    session_id = session_data.get("session_id")
    print(f"Created session: {session_id}")
    
    # Step 3: Test with proper sized image
    print("\nStep 3: Testing with proper 100x100 red image...")
    
    # Create a proper test image (100x100 pixels)
    image_bytes = create_test_image(100, 100, (255, 0, 0))  # Red square
    
    # Prepare form data
    form_data = {
        'session_id': session_id,
        'query': 'red jewelry',
        'category': 'rings'
    }
    
    files = {
        'image': ('test_image.png', image_bytes, 'image/png')
    }
    
    response = requests.post(
        f"{base_url}/chat/image-query",
        headers=headers,
        data=form_data,
        files=files
    )
    
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Found {len(result.get('products', []))} products")
        print(f"Response message: {result.get('response', 'No response')}")
        if result.get('products'):
            print(f"First product: {result['products'][0].get('name', 'No name')}")
    else:
        print(f"Error: {response.text}")
    
    # Step 4: Test with jewelry-like image (blue gradient)
    print("\nStep 4: Testing with blue gradient image...")
    
    # Create a more jewelry-like image
    image_bytes = create_test_image(150, 150, (0, 100, 200))  # Blue gradient-like
    
    files = {
        'image': ('jewelry_test.png', image_bytes, 'image/png')
    }
    
    response = requests.post(
        f"{base_url}/chat/image-query",
        headers=headers,
        data=form_data,
        files=files
    )
    
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Found {len(result.get('products', []))} products")
        print(f"Response message: {result.get('response', 'No response')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_image_search()