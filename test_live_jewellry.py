#!/usr/bin/env python3
"""
Test the live server with jewellry spelling fix
"""

import requests
import json
import uuid

def test_live_jewellry_search():
    """Test the live server with jewellry spelling"""
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    health_resp = requests.get(f"{base_url}/health")
    print(f"Health check: {health_resp.status_code}")
    
    if health_resp.status_code != 200:
        print("❌ Server not healthy")
        return False
    
    # Login data
    login_data = {
        "username": "test_user_02ff81cd",
        "password": "test123"
    }
    
    try:
        login_resp = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login response: {login_resp.status_code}")
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.text}")
            return False
        
        token_data = login_resp.json()
        token = token_data.get('access_token')
        print(f"Got token: {token[:20]}...")
        
        # Create session
        session_resp = requests.post(
            f"{base_url}/chat/sessions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if session_resp.status_code != 201:
            print(f"❌ Session creation failed: {session_resp.text}")
            return False
        
        session_data = session_resp.json()
        session_id = session_data.get('session_id')
        print(f"Created session: {session_id}")
        
        # Test jewellry search
        query_data = {
            "session_id": session_id,
            "query": "show me jewellry"
        }
        
        query_resp = requests.post(
            f"{base_url}/chat/query",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=query_data
        )
        
        print(f"Query response: {query_resp.status_code}")
        
        if query_resp.status_code != 200:
            print(f"❌ Query failed: {query_resp.text}")
            return False
        
        result = query_resp.json()
        print(f"Response: {result.get('response', 'No response')}")
        print(f"Products found: {len(result.get('products', []))}")
        
        products = result.get('products', [])
        if products:
            print("First few products:")
            for i, product in enumerate(products[:3]):
                name = product.get('name', 'Unknown')
                category = product.get('category', 'Unknown')
                price = product.get('price', 'Unknown')
                print(f"  {i+1}. {name} - {category} (${price})")
            
            # Check if they're jewelry products
            jewelry_count = sum(1 for p in products if p.get('category', '').lower() == 'jewelry')
            print(f"Jewelry products: {jewelry_count}/{len(products)}")
            
            if jewelry_count > 0:
                print("✅ SUCCESS: Found jewelry products with 'jewellry' spelling!")
                return True
            else:
                print("❌ FAILED: No jewelry products found")
                return False
        else:
            print("❌ FAILED: No products found")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_live_jewellry_search()
    if success:
        print("\n🎉 Live server test PASSED!")
    else:
        print("\n❌ Live server test FAILED!")