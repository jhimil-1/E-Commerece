#!/usr/bin/env python3
"""
Debug script to examine the exact structure of products returned by the chatbot
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def debug_product_structure():
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
    print(f"\n📊 Response structure:")
    print(f"- session_id: {query_result.get('session_id')}")
    print(f"- query: {query_result.get('query')}")
    print(f"- response: {query_result.get('response')}")
    print(f"- products count: {len(query_result.get('products', []))}")
    
    # Examine the products structure
    products = query_result.get('products', [])
    if products:
        print(f"\n🔍 First product structure:")
        first_product = products[0]
        print(f"Product keys: {list(first_product.keys())}")
        
        for key, value in first_product.items():
            print(f"- {key}: {type(value).__name__} = {repr(value)}")
    
    # Check if similarity_score is present
    if products:
        print(f"\n🎯 Similarity scores:")
        for i, product in enumerate(products):
            score = product.get('score', product.get('similarity_score', 'N/A'))
            print(f"Product {i+1} ({product.get('name', 'Unknown')}): score = {score}")

if __name__ == "__main__":
    debug_product_structure()