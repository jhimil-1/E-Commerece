#!/usr/bin/env python3

import requests
import json

def debug_dress_search():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMDJmZjgxY2QiLCJ1c2VyX2lkIjoiOWJhN2Q0MzgtMjA2Ni00NDY2LTk5MWQtZTRmNzhlNzI4YTc4IiwiZXhwIjoxNzYwMDkyNjg1fQ.R4w_0Ipd1XUnYtWaD5kG8nJ1rtNj8nVp_ALs2dwidrI'
    
    print("🔍 Debugging dress search with different parameters...")
    
    # Test 1: Search with explicit category filter
    print("\n1. Testing with explicit category='clothing':")
    response = requests.post(
        'http://localhost:8000/products/search',
        data={'query': 'dress', 'category': 'clothing', 'limit': 5},
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        print(f"Found {len(results)} results:")
        for i, product in enumerate(results):
            print(f"  {i+1}. {product.get('name')} - ${product.get('price')} - Category: {product.get('category')} - Score: {product.get('similarity_score', 0):.3f}")
    
    # Test 2: Search without category filter
    print("\n2. Testing without category filter:")
    response = requests.post(
        'http://localhost:8000/products/search',
        data={'query': 'dress', 'limit': 5},
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        print(f"Found {len(results)} results:")
        for i, product in enumerate(results):
            print(f"  {i+1}. {product.get('name')} - ${product.get('price')} - Category: {product.get('category')} - Score: {product.get('similarity_score', 0):.3f}")

if __name__ == "__main__":
    debug_dress_search()