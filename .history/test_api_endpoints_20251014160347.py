#!/usr/bin/env python3
"""
Test API endpoints with enhanced search functionality
"""

import requests
import json
import base64
from pathlib import Path

def test_text_search():
    """Test text search endpoint"""
    print("🔍 Testing text search for 'necklace'...")
    
    url = "http://localhost:8000/products/search"
    data = {
        "query": "necklace",
        "limit": 5
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            print(f"Found {len(products)} products")
            
            # Count necklaces
            necklace_count = sum(1 for p in products if "necklace" in p.get("name", "").lower())
            print(f"Necklaces: {necklace_count}/{len(products)}")
            
            for i, product in enumerate(products, 1):
                status = "✅" if "necklace" in product.get("name", "").lower() else "❌"
                print(f"  {i}. {status} {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
            
            return necklace_count > 0
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def test_image_search():
    """Test image search endpoint"""
    print("\n📸 Testing image search for 'necklace'...")
    
    # Create a simple test image (1x1 pixel)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd4c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    url = "http://localhost:8000/chat/image-query"
    files = {
        'image': ('test.png', test_image_data, 'image/png')
    }
    data = {
        'text_query': 'necklace',
        'limit': 5
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            print(f"Found {len(products)} products")
            
            # Count necklaces
            necklace_count = sum(1 for p in products if "necklace" in p.get("name", "").lower())
            print(f"Necklaces: {necklace_count}/{len(products)}")
            
            for i, product in enumerate(products, 1):
                status = "✅" if "necklace" in product.get("name", "").lower() else "❌"
                print(f"  {i}. {status} {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
            
            return necklace_count > 0
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def main():
    print("🧪 Testing Enhanced Search API Endpoints")
    print("=" * 50)
    
    # Test text search
    text_success = test_text_search()
    
    # Test image search
    image_success = test_image_search()
    
    print("\n📊 Test Results:")
    print("=" * 50)
    print(f"Text search: {'✅ PASS' if text_success else '❌ FAIL'}")
    print(f"Image search: {'✅ PASS' if image_success else '❌ FAIL'}")
    
    if text_success and image_success:
        print("\n🎉 All tests passed! Enhanced search is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()