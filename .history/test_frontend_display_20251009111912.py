#!/usr/bin/env python3
"""
Test script to verify the frontend is displaying products correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_frontend_display():
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
    
    # Make a chat query to get products
    print("\n💬 Making chat query for 'laptop'...")
    query_data = {
        "query": "laptop",
        "session_id": "test-session-123",
        "limit": 3
    }
    
    query_response = requests.post(f"{BASE_URL}/chat/query", json=query_data, headers=headers)
    
    if query_response.status_code != 200:
        print(f"❌ Query failed: {query_response.status_code}")
        print(f"Error: {query_response.text}")
        return
    
    result = query_response.json()
    products = result.get('products', [])
    
    print(f"✅ Found {len(products)} products")
    
    # Display what the frontend should show
    for i, product in enumerate(products):
        print(f"\n📦 Product {i+1}: {product['name']}")
        print(f"   - Category: {product['category']}")
        print(f"   - Price: ${product['price']}")
        print(f"   - Description: '{product['description']}' (empty: {not product['description'].strip()})")
        print(f"   - Similarity Score: {product['score']:.1%}")
        print(f"   - Image URL: {product.get('image_url', 'N/A')}")
    
    print("\n✅ Frontend should now display:")
    print("   - Description: 'No description available' (for empty descriptions)")
    print("   - Similarity: percentage (e.g., 73.0%)")

if __name__ == "__main__":
    test_frontend_display()