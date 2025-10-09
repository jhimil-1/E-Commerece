#!/usr/bin/env python3

import requests
import json
import tempfile
import os

def upload_products_as_testuser1():
    # Login as testuser1
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    login_response = requests.post(
        "http://localhost:8000/auth/login",
        json=login_data
    )
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token_data = login_response.json()
    token = token_data["access_token"]
    
    print(f"Logged in as testuser1")
    
    # Create a JSON file with products
    products = [
        {
            "name": "Diamond Ring",
            "price": 1200.0,
            "category": "Rings",
            "description": "Beautiful diamond ring with 1 carat diamond",
            "image_url": ""
        },
        {
            "name": "Gold Necklace",
            "price": 800.0,
            "category": "Necklaces", 
            "description": "Elegant gold necklace with pendant",
            "image_url": ""
        },
        {
            "name": "Pearl Earrings",
            "price": 300.0,
            "category": "Earrings",
            "description": "Classic pearl earrings for any occasion",
            "image_url": ""
        }
    ]
    
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(products, f)
        temp_file_path = f.name
    
    try:
        # Upload the JSON file
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        with open(temp_file_path, 'rb') as f:
            files = {'file': ('products.json', f, 'application/json')}
            
            response = requests.post(
                "http://localhost:8000/products/upload",
                headers=headers,
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully uploaded: {result}")
        else:
            print(f"Failed to upload products: {response.text}")
    
    finally:
        # Clean up temp file
        os.unlink(temp_file_path)

if __name__ == "__main__":
    upload_products_as_testuser1()