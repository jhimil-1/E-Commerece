#!/usr/bin/env python3
"""
Test script to verify the search functionality with proper authentication
"""

import requests
import json

def test_search_with_auth():
    """Test the search functionality with authentication"""
    
    print("=== Testing Search with Authentication ===")
    
    # Test credentials
    username = "testuser123"
    password = "testpass123"
    
    # Base URL
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Login to get token
        print("\n1. Logging in...")
        login_response = requests.post(f"{base_url}/auth/login", json={
            "username": username,
            "password": password
        })
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
        token = login_response.json()["access_token"]
        print(f"✓ Login successful, token: {token[:20]}...")
        
        # Step 2: Create chat session
        print("\n2. Creating chat session...")
        session_response = requests.post(f"{base_url}/chat/sessions", 
                                         headers={"Authorization": f"Bearer {token}"})
        
        if session_response.status_code != 200:
            print(f"Session creation failed: {session_response.status_code} - {session_response.text}")
            return False
            
        session_id = session_response.json()["session_id"]
        print(f"✓ Session created: {session_id}")
        
        # Step 3: Test search
        print("\n3. Testing search for 'phone'...")
        search_response = requests.post(f"{base_url}/chat/query",
                                      headers={"Authorization": f"Bearer {token}"},
                                      json={
                                          "query": "phone",
                                          "session_id": session_id,
                                          "limit": 5
                                      })
        
        print(f"Search response status: {search_response.status_code}")
        
        if search_response.status_code != 200:
            print(f"Search failed: {search_response.status_code} - {search_response.text}")
            return False
            
        result = search_response.json()
        print(f"✓ Search successful!")
        print(f"Response structure:")
        print(f"  - session_id: {result.get('session_id', 'N/A')}")
        print(f"  - query: {result.get('query', 'N/A')}")
        print(f"  - response: {result.get('response', 'N/A')[:50]}...")
        print(f"  - products count: {len(result.get('products', []))}")
        print(f"  - timestamp: {result.get('timestamp', 'N/A')}")
        
        # Step 4: Examine products
        products = result.get('products', [])
        if products:
            print(f"\n4. First product details:")
            first_product = products[0]
            for key, value in first_product.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"  - {key}: {value[:100]}...")
                else:
                    print(f"  - {key}: {value}")
        else:
            print("\n4. No products found in response")
        
        return True
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_search_with_auth()
    print(f"\n=== Test {'PASSED' if success else 'FAILED'} ===")