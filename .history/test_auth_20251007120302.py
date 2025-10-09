#!/usr/bin/env python3

import requests
import json

def test_auth():
    # Use the credentials from the successful login
    username = 'test_user_92aeb317'
    password = 'test123456'
    
    # Login to get token
    login_data = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    
    login_response = requests.post('http://localhost:8000/auth/login', 
                                 data=json.dumps(login_data), 
                                 headers=headers)
    
    if login_response.status_code == 200:
        result = login_response.json()
        access_token = result.get('access_token')
        user_id = result.get('user_id')
        
        print(f'Login successful!')
        print(f'User ID: {user_id}')
        print(f'Access token: {access_token[:50]}...')
        
        # Test authenticated endpoint
        auth_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test search with user authentication
        search_data = {'query': 'gold necklace', 'user_id': user_id}
        search_response = requests.post('http://localhost:8000/search', 
                                        data=json.dumps(search_data), 
                                        headers=auth_headers)
        
        print(f'Search with auth status: {search_response.status_code}')
        if search_response.status_code == 200:
            search_result = search_response.json()
            print(f'Search returned {len(search_result.get(\"results\", []))} results')
            for i, result in enumerate(search_result.get('results', [])[:3]):
                print(f'  {i+1}. {result.get(\"name\", \"Unknown\")}')
        else:
            print(f'Search error: {search_response.text}')
            
    else:
        print(f'Login failed: {login_response.text}')

if __name__ == "__main__":
    test_auth()