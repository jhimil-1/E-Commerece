#!/usr/bin/env python3
"""
Check if any products in the database have descriptions
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def check_product_descriptions():
    # Login
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    print("🔑 Logging in...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    login_data = login_response.json()
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try different search terms to see if any products have descriptions
    search_terms = ["laptop", "phone", "electronics", "MacBook", "iPhone", "Samsung"]
    
    for term in search_terms:
        print(f"\n🔍 Searching for '{term}'...")
        
        # Create session
        session_response = requests.post(f"{BASE_URL}/chat/sessions", headers=headers)
        if session_response.status_code not in [200, 201]:
            continue
            
        session_id = session_response.json()["session_id"]
        
        # Make chat query
        query_data = {
            "query": term,
            "session_id": session_id,
            "limit": 5
        }
        
        query_response = requests.post(f"{BASE_URL}/chat/query", json=query_data, headers=headers)
        
        if query_response.status_code == 200:
            result = query_response.json()
            products = result.get('products', [])
            
            # Check if any product has a description
            products_with_descriptions = [p for p in products if p.get('description', '').strip()]
            
            if products_with_descriptions:
                print(f"✅ Found {len(products_with_descriptions)} products with descriptions!")
                for p in products_with_descriptions:
                    print(f"   - {p['name']}: '{p['description']}'")
                break
            else:
                print(f"   All {len(products)} products have empty descriptions")
        else:
            print(f"   Query failed: {query_response.status_code}")

if __name__ == "__main__":
    check_product_descriptions()