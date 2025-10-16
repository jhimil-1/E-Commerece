#!/usr/bin/env python3
"""
Integration test to verify the enhanced search works through the API endpoints
"""

import requests
import json
import base64
from PIL import Image
import io

def test_api_search():
    """Test the API endpoints for enhanced search"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Integration with Enhanced Search")
    print("=" * 60)
    
    # Test 1: Text search for necklace
    print("\n🔍 Test 1: Text search for 'necklace'")
    print("-" * 40)
    
    try:
        response = requests.post(
            f"{base_url}/products/search",
            json={
                "query": "necklace",
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            print(f"Status: ✅ Success")
            print(f"Found {len(products)} products")
            
            if products:
                # Check relevance
                necklace_products = [p for p in products if 'necklace' in p.get('name', '').lower()]
                print(f"Products with 'necklace' in name: {len(necklace_products)}/{len(products)}")
                
                for i, product in enumerate(products[:3], 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    score = product.get('similarity_score', 0)
                    has_necklace = 'necklace' in name.lower()
                    status = "✅" if has_necklace else "❌"
                    print(f"  {i}. {status} {name} - {category} (Score: {score:.3f})")
                    
                if len(necklace_products) == len(products):
                    print("✅ PERFECT: All products are necklaces!")
                elif len(necklace_products) >= len(products) * 0.8:
                    print("✅ VERY GOOD: 80%+ products are necklaces")
                else:
                    print("⚠️  NEEDS IMPROVEMENT: Less than 80% are necklaces")
            else:
                print("❌ No products found")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
    
    # Test 2: Chatbot text query
    print("\n💬 Test 2: Chatbot query for 'necklace'")
    print("-" * 40)
    
    try:
        # First create a session
        session_response = requests.post(f"{base_url}/chat/session")
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data.get('session_id')
            print(f"Created session: {session_id}")
            
            # Now test chat query
            chat_response = requests.post(
                f"{base_url}/chat/message",
                json={
                    "session_id": session_id,
                    "query": "necklace"
                }
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                products = chat_data.get('products', [])
                
                print(f"Status: ✅ Success")
                print(f"Found {len(products)} products")
                print(f"Response: {chat_data.get('response', 'No response')}")
                
                if products:
                    necklace_products = [p for p in products if 'necklace' in p.get('name', '').lower()]
                    print(f"Products with 'necklace' in name: {len(necklace_products)}/{len(products)}")
                    
                    for i, product in enumerate(products[:3], 1):
                        name = product.get('name', 'Unknown')
                        category = product.get('category', 'Unknown')
                        has_necklace = 'necklace' in name.lower()
                        status = "✅" if has_necklace else "❌"
                        print(f"  {i}. {status} {name} - {category}")
                        
                    if len(necklace_products) == len(products):
                        print("✅ PERFECT: All products are necklaces!")
                    elif len(necklace_products) >= len(products) * 0.8:
                        print("✅ VERY GOOD: 80%+ products are necklaces")
                    else:
                        print("⚠️  NEEDS IMPROVEMENT: Less than 80% are necklaces")
                else:
                    print("❌ No products found in chat response")
            else:
                print(f"❌ Chat API Error: {chat_response.status_code} - {chat_response.text}")
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            
    except Exception as e:
        print(f"❌ Chat test failed: {str(e)}")
    
    print("\n📊 Integration Test Summary:")
    print("=" * 60)
    print("Enhanced search has been integrated into the API endpoints.")
    print("The system should now return more relevant products for specific queries.")

if __name__ == "__main__":
    test_api_search()