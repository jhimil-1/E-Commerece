#!/usr/bin/env python3

import requests
import json

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
    
    # Upload some products
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    products = [
        {
            "name": "Diamond Ring",
            "price": 1200.0,
            "category": "Rings",
            "description": "Beautiful diamond ring with 1 carat diamond"
        },
        {
            "name": "Gold Necklace",
            "price": 800.0,
            "category": "Necklaces", 
            "description": "Elegant gold necklace with pendant"
        },
        {
            "name": "Pearl Earrings",
            "price": 300.0,
            "category": "Earrings",
            "description": "Classic pearl earrings for any occasion"
        }
    ]
    
    for product in products:
        response = requests.post(
            "http://localhost:8000/upload/products",
            headers=headers,
            json=product
        )
        
        if response.status_code == 201:
            print(f"Uploaded: {product['name']}")
        else:
            print(f"Failed to upload {product['name']}: {response.text}")

if __name__ == "__main__":
    upload_products_as_testuser1()