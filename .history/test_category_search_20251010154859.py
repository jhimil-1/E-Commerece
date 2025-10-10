#!/usr/bin/env python3

import requests

def test_category_search():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMDJmZjgxY2QiLCJ1c2VyX2lkIjoiOWJhN2Q0MzgtMjA2Ni00NDY2LTk5MWQtZTRmNzhlNzI4YTc4IiwiZXhwIjoxNzYwMDkyNjg1fQ.R4w_0Ipd1XUnYtWaD5kG8nJ1rtNj8nVp_ALs2dwidrI'
    
    # Test the mapped categories from app.js
    category_mappings = {
        'electronics': 'Smartphones',
        'clothing': 'clothing',
        'home': 'Smart Speakers',
        'books': 'Tablets',
        'sports': 'Smartwatches'
    }
    
    for frontend_cat, backend_cat in category_mappings.items():
        print(f"\n🔄 Testing category mapping: {frontend_cat} -> {backend_cat}")
        
        response = requests.post(
            'http://localhost:8000/products/search',
            data={'query': 'products', 'category': backend_cat, 'limit': 3},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"Found {len(results)} results:")
            
            for i, product in enumerate(results[:2]):
                print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 0)} - Category: {product.get('category', 'Unknown')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_category_search()