#!/usr/bin/env python3

import requests
import json

def test_backend_response():
    """Test what the backend actually returns"""
    
    # Try to login first
    login_data = {
        "username": "testuser_new_123",
        "password": "test123"
    }
    
    try:
        # Try login
        login_response = requests.post("http://localhost:8000/auth/login", json=login_data)
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code != 200:
            print(f"Login error: {login_response.text}")
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print(f"Got token: {token[:20]}...")
        else:
            # Try signup
            signup_data = {
                "username": "testuser_new_123",
                "password": "test123",
                "email": "testuser_new_123@example.com"
            }
            signup_response = requests.post("http://localhost:8000/auth/signup", json=signup_data)
            print(f"Signup status: {signup_response.status_code}")
            if signup_response.status_code != 200:
                print(f"Signup error: {signup_response.text}")
            
            if signup_response.status_code == 200:
                result = signup_response.json()
                print(f"Signup result: {result}")
                token = result.get("access_token")
                if token:
                    headers = {"Authorization": f"Bearer {token}"}
                    print(f"Got token from signup: {token[:20]}...")
                else:
                    print("No token in signup response")
                    return
            else:
                print("Failed to get token")
                return
        
        # Test search
        search_data = {
            "query": "gold ring",
            "session_id": "test-session-123"
        }
        
        search_response = requests.post("http://localhost:8000/chat/query", 
                                      json=search_data, headers=headers)
        
        print(f"\nSearch status: {search_response.status_code}")
        print(f"Search response headers: {dict(search_response.headers)}")
        
        if search_response.status_code == 200:
            result = search_response.json()
            print(f"\nResponse structure:")
            print(f"Type: {type(result)}")
            print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            if isinstance(result, dict):
                if 'products' in result:
                    print(f"Products count: {len(result['products'])}")
                    if result['products']:
                        print(f"First product keys: {list(result['products'][0].keys())}")
                        print(f"First product: {json.dumps(result['products'][0], indent=2)}")
                elif 'data' in result:
                    print(f"Data structure: {type(result['data'])}")
                    if isinstance(result['data'], dict) and 'results' in result['data']:
                        print(f"Results count: {len(result['data']['results'])}")
                        if result['data']['results']:
                            print(f"First result: {json.dumps(result['data']['results'][0], indent=2)}")
                else:
                    print(f"Full response: {json.dumps(result, indent=2)}")
            else:
                print(f"Raw response: {result}")
        else:
            print(f"Search error: {search_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_backend_response()