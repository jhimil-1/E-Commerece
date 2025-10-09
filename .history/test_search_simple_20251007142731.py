#!/usr/bin/env python3
"""Simple test to verify search functionality works."""

import requests
import json

def test_search():
    print("Testing search functionality...")
    
    # Login first
    login_data = {'username': 'testuser', 'password': 'testpass123'}
    login_response = requests.post('http://localhost:8000/auth/login', data=login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token = login_response.json()['access_token']
    print("✅ Login successful")
    
    # Test search for electronics
    headers = {'Authorization': f'Bearer {token}'}
    search_data = {'query': 'electronics', 'limit': 5}
    search_response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
    
    print(f"Search response: {search_response.status_code}")
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"Found {results.get('count', 0)} results for electronics")
        for i, result in enumerate(results.get('results', [])):
            print(f"{i+1}. {result.get('name', 'N/A')} - {result.get('category', 'N/A')}")
    else:
        print(f"Error: {search_response.text}")

if __name__ == "__main__":
    test_search()