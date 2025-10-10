#!/usr/bin/env python3

import requests
import json

def test_search():
    # Use the token we created earlier
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMDJmZjgxY2QiLCJ1c2VyX2lkIjoiOWJhN2Q0MzgtMjA2Ni00NDY2LTk5MWQtZTRmNzhlNzI4YTc4IiwiZXhwIjoxNzYwMDkyNjg1fQ.R4w_0Ipd1XUnYtWaD5kG8nJ1rtNj8nVp_ALs2dwidrI'
    
    # Test different search queries
    test_queries = ["dress", "clothing", "summer dress", "evening dress"]
    
    for query in test_queries:
        print(f"\n🔍 Testing search for: '{query}'")
        
        # Use the products search endpoint (POST method with form data)
        response = requests.post(
            'http://localhost:8000/products/search',
            data={'query': query, 'limit': 5},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"Found {len(results)} results:")
            
            for i, product in enumerate(results[:3]):  # Show first 3 results
                print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 0)} - Category: {product.get('category', 'Unknown')}")
                print(f"     Description: {product.get('description', 'No description')[:80]}...")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_search()