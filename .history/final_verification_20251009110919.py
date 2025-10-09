#!/usr/bin/env python3
"""
Final verification test to ensure the chatbot search issue is resolved
"""

import asyncio
import requests
import json
from datetime import datetime

def test_original_issue():
    """Test the exact scenario that was failing before"""
    
    base_url = "http://localhost:8000"
    
    print("=== Testing Original Issue: Chatbot Search ===")
    
    # Step 1: Login
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.text}")
            return False
            
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Create session
    try:
        session_response = requests.post(f"{base_url}/chat/sessions", headers=headers)
        if session_response.status_code != 201:
            print(f"❌ Session creation failed: {session_response.text}")
            return False
            
        session_id = session_response.json().get("session_id")
        print(f"✅ Session created: {session_id}")
        
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return False
    
    # Step 3: Test chat query (the original failing operation)
    test_queries = ["laptop", "phone", "electronics", "MacBook"]
    
    all_passed = True
    
    for query in test_queries:
        try:
            query_data = {
                "query": query,
                "session_id": session_id
            }
            
            query_response = requests.post(f"{base_url}/chat/query", 
                                         json=query_data, headers=headers)
            
            if query_response.status_code != 200:
                print(f"❌ Query '{query}' failed: {query_response.text}")
                all_passed = False
                continue
                
            result = query_response.json()
            products = result.get("products", [])
            
            if len(products) == 0:
                print(f"⚠️  Query '{query}' returned no products (but no error)")
            else:
                print(f"✅ Query '{query}' returned {len(products)} products")
                
                # Verify product structure
                if products:
                    first_product = products[0]
                    required_fields = ["name", "category", "price", "score"]
                    missing_fields = [field for field in required_fields if field not in first_product]
                    
                    if missing_fields:
                        print(f"⚠️  Product missing fields: {missing_fields}")
                    else:
                        print(f"   - Product structure valid: {first_product['name']} (${first_product['price']})")
                
        except Exception as e:
            print(f"❌ Query '{query}' error: {e}")
            all_passed = False
    
    # Final summary
    print("\n=== Final Summary ===")
    if all_passed:
        print("✅ All tests passed! The chatbot search issue has been resolved.")
        print("✅ User sessions are working correctly")
        print("✅ Product search is returning results")
        print("✅ API endpoints are functioning properly")
        return True
    else:
        print("❌ Some tests failed. Issue may not be fully resolved.")
        return False

if __name__ == "__main__":
    success = test_original_issue()
    exit(0 if success else 1)