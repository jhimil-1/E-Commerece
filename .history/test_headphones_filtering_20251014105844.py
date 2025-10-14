#!/usr/bin/env python3
"""
Test script to verify that headphones search filtering is working correctly.
This tests that searching for 'headphones' returns only relevant headphones products.
"""

import requests
import json
import sys

def test_headphones_search():
    """Test that headphones search returns only relevant products."""
    
    print("Testing headphones search filtering...")
    
    # First authenticate
    try:
        auth_response = requests.post(
            "http://localhost:8000/auth/login",
            json={
                "username": "test_user",
                "password": "test_pass123"
            }
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Authentication failed with status {auth_response.status_code}")
            return False
            
        auth_data = auth_response.json()
        token = auth_data.get("access_token")
        
        if not token:
            print("❌ No access token received")
            return False
            
        print("✅ Authentication successful")
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False
    
    # Test the enhanced search endpoint
    try:
        response = requests.post(
            "http://localhost:8000/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": "Show me headphones",
                "session_id": "test_headphones_session"
            }
        )
        
        if response.status_code != 200:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response text: {response.text}")
            return False
            
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Check if we got products
        if 'products' in result and result['products']:
            print(f"\nFound {len(result['products'])} products:")
            
            relevant_products = []
            irrelevant_products = []
            
            for product in result['products']:
                name = product.get('name', '').lower()
                description = product.get('description', '').lower()
                
                # Check if product is headphones-related
                headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
                is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
                
                if is_headphones:
                    relevant_products.append(product)
                else:
                    irrelevant_products.append(product)
                
                print(f"  - {product['name']} (${product['price']})")
                print(f"    Description: {product['description'][:100]}...")
                print(f"    Relevant: {'✅' if is_headphones else '❌'}")
                print()
            
            # Calculate relevance ratio
            total_products = len(result['products'])
            relevant_count = len(relevant_products)
            irrelevant_count = len(irrelevant_products)
            relevance_ratio = relevant_count / total_products if total_products > 0 else 0
            
            print(f"Results Summary:")
            print(f"  Total products: {total_products}")
            print(f"  Relevant (headphones): {relevant_count}")
            print(f"  Irrelevant: {irrelevant_count}")
            print(f"  Relevance ratio: {relevance_ratio:.1%}")
            
            # Test criteria: At least 80% of results should be headphones-related
            if relevance_ratio >= 0.8:
                print(f"✅ PASS: Headphones search filtering is working correctly!")
                return True
            else:
                print(f"❌ FAIL: Too many irrelevant products returned")
                return False
                
        else:
            print("❌ No products found in response")
            return False
            
    except Exception as e:
        print(f"❌ Error testing headphones search: {e}")
        return False

def test_regular_electronics_search():
    """Test that broad electronics search still works."""
    
    print("\nTesting broad electronics search...")
    
    # Authenticate first (reuse credentials from previous test)
    try:
        auth_response = requests.post(
            "http://localhost:8000/auth/login",
            json={
                "username": "test_user",
                "password": "test_pass123"
            }
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Authentication failed with status {auth_response.status_code}")
            return False
            
        auth_data = auth_response.json()
        token = auth_data.get("access_token")
        
        if not token:
            print("❌ No access token received")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False
    
    try:
        response = requests.post(
            "http://localhost:8000/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": "Show me electronics",
                "session_id": "test_electronics_session"
            }
        )
        
        if response.status_code != 200:
            print(f"❌ API request failed with status {response.status_code}")
            return False
            
        result = response.json()
        
        if 'products' in result and result['products']:
            print(f"Found {len(result['products'])} electronics products")
            for product in result['products']:
                print(f"  - {product['name']} (${product['price']})")
            
            print("✅ PASS: Broad electronics search is working")
            return True
        else:
            print("❌ No electronics products found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing electronics search: {e}")
        return False

if __name__ == "__main__":
    print("🎧 Headphones Search Filtering Test")
    print("=" * 40)
    
    # Test headphones search
    headphones_pass = test_headphones_search()
    
    # Test that we didn't break broad electronics search
    electronics_pass = test_regular_electronics_search()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Headphones filtering: {'✅ PASS' if headphones_pass else '❌ FAIL'}")
    print(f"Electronics search: {'✅ PASS' if electronics_pass else '❌ FAIL'}")
    
    if headphones_pass and electronics_pass:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)