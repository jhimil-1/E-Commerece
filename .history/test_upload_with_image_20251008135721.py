#!/usr/bin/env python3
"""Test uploading a product with an image to verify the complete image flow"""

import requests
import json
import base64
from PIL import Image
import io

def get_fresh_token():
    """Get a fresh authentication token"""
    login_data = {
        "username": "test_user2",
        "password": "test123"
    }
    
    response = requests.post("http://localhost:8000/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

def create_test_image():
    """Create a simple test image"""
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return img_base64

def test_upload_with_image():
    """Test uploading a product with an image"""
    print("Getting fresh token...")
    token = get_fresh_token()
    
    print("Creating test image...")
    image_data = create_test_image()
    
    # Create JSON content for the file
    products_data = [{
        "name": "Test Jewelry Item",
        "description": "A beautiful test jewelry piece with red gemstone",
        "price": "299.99",
        "category": "jewelry",
        "image_url": image_data  # Use image_url instead of image
    }]
    
    # Create a JSON file for upload
    json_content = json.dumps(products_data)
    
    # Create FormData with the file
    files = {
        'file': ('products.json', json_content, 'application/json')
    }
    
    print("Uploading product with image...")
    response = requests.post(
        "http://localhost:8000/products/upload",
        files=files,
        headers={'Authorization': f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Upload successful! Inserted count: {result.get('inserted_count', 0)}")
        print(f"Product IDs: {result.get('product_ids', [])}")
        return result.get('product_ids', [])[0] if result.get('product_ids') else None
    else:
        print(f"Upload failed: {response.status_code} - {response.text}")
        return None

def test_search_for_product():
    """Test searching for the uploaded product"""
    print("\nTesting search for uploaded product...")
    token = get_fresh_token()
    
    # Create chat session
    session_response = requests.post(
        "http://localhost:8000/chat/sessions",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if session_response.status_code not in [200, 201]:
        print(f"Failed to create session: {session_response.status_code}")
        return
    
    session_id = session_response.json().get("session_id")
    print(f"Session created: {session_id}")
    
    # Search for the product
    search_data = {
        "session_id": session_id,
        "query": "test jewelry red gemstone",
        "limit": 5
    }
    
    search_response = requests.post(
        "http://localhost:8000/chat/query",
        json=search_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if search_response.status_code == 200:
        result = search_response.json()
        products = result.get('products', [])
        print(f"Found {len(products)} products")
        
        if products:
            product = products[0]
            print(f"First product: {product.get('name')}")
            print(f"Image URL: {product.get('image_url', 'N/A')}")
            print(f"Image Path: {product.get('image_path', 'N/A')}")
            print(f"Image: {product.get('image', 'N/A')}")
            print(f"Payload keys: {list(product.get('payload', {}).keys())}")
    else:
        print(f"Search failed: {search_response.status_code} - {search_response.text}")

if __name__ == "__main__":
    print("Testing product upload with image...")
    product_id = test_upload_with_image()
    
    if product_id:
        test_search_for_product()
    else:
        print("Skipping search test due to upload failure")