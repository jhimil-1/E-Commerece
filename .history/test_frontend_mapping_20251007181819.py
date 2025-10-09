#!/usr/bin/env python3
"""Test the frontend category mapping fix."""

import requests
import json

def test_frontend_category_mapping():
    """Test that frontend categories are properly mapped to backend categories."""
    
    # Test credentials
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
            return False
            
        login_result = login_response.json()
        access_token = login_result["access_token"]
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Test frontend categories that should be mapped
        frontend_backend_mapping = {
            'electronics': 'Smartphones',
            'clothing': 'Smartwatches',  # Assuming this mapping
            'home': 'Smart Speakers',    # Assuming this mapping
            'books': 'Tablets',            # Assuming this mapping
            'sports': 'Headphones'         # Assuming this mapping
        }
        
        print("Testing frontend category mapping...")
        print("=" * 50)
        
        all_passed = True
        
        for frontend_cat, backend_cat in frontend_backend_mapping.items():
            # Test frontend category
            search_data = {
                "query": "products",
                "category": frontend_cat,
                "limit": 5
            }
            
            frontend_response = requests.post("http://localhost:8000/products/search", data=search_data, headers=headers)
            
            # Test backend category
            search_data["category"] = backend_cat
            backend_response = requests.post("http://localhost:8000/products/search", data=search_data, headers=headers)
            
            if frontend_response.status_code == 200 and backend_response.status_code == 200:
                frontend_results = len(frontend_response.json().get("results", []))
                backend_results = len(backend_response.json().get("results", []))
                
                print(f"Frontend '{frontend_cat}': {frontend_results} results")
                print(f"Backend '{backend_cat}': {backend_results} results")
                
                if frontend_results == 0 and backend_results > 0:
                    print(f"  ❌ MAPPING ISSUE: Frontend returns 0 but backend has {backend_results} results")
                    all_passed = False
                elif frontend_results > 0:
                    print(f"  ✅ Frontend mapping appears to work")
                else:
                    print(f"  ⚠️  Both return 0 results")
            else:
                print(f"  ❌ Request failed for {frontend_cat}/{backend_cat}")
                all_passed = False
                
            print()
        
        return all_passed
        
    except Exception as e:
        print(f"Error testing category mapping: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_category_mapping()
    if success:
        print("✅ All category mapping tests passed!")
    else:
        print("❌ Some category mapping tests failed!")