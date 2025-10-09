#!/usr/bin/env python3
"""
Debug script to examine the complete product structure including payload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def debug_complete_product_structure():
    # Login
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    print("🔑 Logging in...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    login_data = login_response.json()
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Login successful")
    
    # Create session
    print("\n📝 Creating session...")
    session_response = requests.post(f"{BASE_URL}/chat/sessions", headers=headers)
    
    if session_response.status_code not in [200, 201]:
        print(f"❌ Session creation failed: {session_response.status_code}")
        print(session_response.text)
        return
    
    session_data = session_response.json()
    session_id = session_data["session_id"]
    
    print(f"✅ Session created: {session_id}")
    
    # Make a chat query
    print("\n💬 Making chat query...")
    query_data = {
        "query": "laptop",
        "session_id": session_id,
        "limit": 2
    }
    
    query_response = requests.post(f"{BASE_URL}/chat/query", json=query_data, headers=headers)
    
    if query_response.status_code != 200:
        print(f"❌ Query failed: {query_response.status_code}")
        print(query_response.text)
        return
    
    query_result = query_response.json()
    
    print("✅ Query successful")
    
    # Examine the products structure in detail
    products = query_result.get('products', [])
    if products:
        print(f"\n🔍 Detailed product analysis:")
        for i, product in enumerate(products):
            print(f"\n--- Product {i+1}: {product['name']} ---")
            print(f"Top-level fields:")
            for key, value in product.items():
                if key != 'payload':  # Skip payload for now
                    print(f"  - {key}: {repr(value)}")
            
            print(f"\nPayload content:")
            if 'payload' in product:
                for key, value in product['payload'].items():
                    print(f"  - {key}: {repr(value)}")
            
            # Check for description in different places
            print(f"\nDescription analysis:")
            print(f"  - product['description']: {repr(product.get('description', 'MISSING'))}")
            print(f"  - product['payload']['description']: {repr(product.get('payload', {}).get('description', 'MISSING'))}")
            
            # Check for image in different places
            print(f"\nImage analysis:")
            print(f"  - product['image_url']: {repr(product.get('image_url', 'MISSING'))}")
            print(f"  - product['image_path']: {repr(product.get('image_path', 'MISSING'))}")
            print(f"  - product['image']: {repr(product.get('image', 'MISSING'))}")
            print(f"  - product['payload']['image_url']: {repr(product.get('payload', {}).get('image_url', 'MISSING'))}")

if __name__ == "__main__":
    debug_complete_product_structure()