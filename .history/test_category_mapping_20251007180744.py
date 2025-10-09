#!/usr/bin/env python3
"""Test the category mapping fix."""

import requests
import json

def test_category_search(category, user_id="68da75b494c9b5dbe3bb5790"):
    """Test searching with a specific category."""
    
    # Test credentials from the working tests
    username = "test_user2"
    password = "test123"
    
    # Login first
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        # Login
        login_response = requests.post("http://localhost:8000/auth/login", json=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            return None
            
        login_result = login_response.json()
        access_token = login_result["access_token"]
        
        # Search with category
        search_data = {
            "query": "",
            "category": category,
            "limit": 10
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        search_response = requests.post("http://localhost:8000/products/search", data=search_data, headers=headers)
        
        if search_response.status_code == 200:
            result = search_response.json()
            results = result.get("results", [])
            print(f"Category '{category}': {len(results)} results")
            if results:
                print(f"  First result: {results[0].get('name')} - {results[0].get('category')}")
            return len(results)
        else:
            print(f"Search failed for category '{category}': {search_response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error testing category '{category}': {e}")
        return None

def main():
    """Test the category mapping."""
    
    # Test frontend categories
    frontend_categories = [
        'electronics',
        'clothing', 
        'home',
        'books',
        'sports'
    ]
    
    # Test backend categories
    backend_categories = [
        'Smartphones',
        'Smartwatches',
        'Smart Speakers',
        'Tablets',
        'Laptops',
        'Headphones'
    ]
    
    print("Testing frontend category mapping...")
    print("=" * 50)
    
    for category in frontend_categories:
        test_category_search(category)
        
    print("\nTesting backend categories...")
    print("=" * 50)
    
    for category in backend_categories:
        test_category_search(category)

if __name__ == "__main__":
    main()