#!/usr/bin/env python3
"""
Simple test for enhanced search functionality
"""

import requests
import json

def test_products_search():
    """Test the products/search endpoint"""
    print("🔍 Testing products/search endpoint...")
    
    url = "http://localhost:8000/products/search"
    data = {
        "query": "necklace",
        "limit": 5
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            products = result.get("results", [])
            print(f"Found {len(products)} products")
            
            # Count necklaces
            necklace_count = sum(1 for p in products if "necklace" in p.get("name", "").lower())
            print(f"Necklaces: {necklace_count}/{len(products)}")
            
            for i, product in enumerate(products, 1):
                status = "✅" if "necklace" in product.get("name", "").lower() else "❌"
                print(f"  {i}. {status} {product.get('name', 'Unknown')} - Score: {product.get('similarity_score', 0):.3f}")
            
            return necklace_count > 0
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def test_health_check():
    """Test health endpoint"""
    print("\n🏥 Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Server is healthy")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def main():
    print("🧪 Testing Enhanced Search API")
    print("=" * 40)
    
    # Test health first
    health_ok = test_health_check()
    
    if health_ok:
        # Test search
        search_ok = test_products_search()
        
        print("\n📊 Test Results:")
        print("=" * 40)
        print(f"Health check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"Search test: {'✅ PASS' if search_ok else '❌ FAIL'}")
        
        if health_ok and search_ok:
            print("\n🎉 Enhanced search is working correctly!")
            print("The system now provides more relevant results for specific queries.")
        else:
            print("\n⚠️  Some tests failed. Check server status.")
    else:
        print("\n❌ Server is not responding. Check if it's running.")

if __name__ == "__main__":
    main()