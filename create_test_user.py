#!/usr/bin/env python3

import requests
import json
import uuid

def create_test_user():
    # Create a new user
    url = 'http://localhost:8000/auth/signup'
    headers = {'Content-Type': 'application/json'}
    
    username = f'test_user_{uuid.uuid4().hex[:8]}'
    password = 'test123456'
    
    data = {
        'username': username,
        'password': password,
        'email': f'{username}@test.com'
    }
    
    print(f'Creating user: {username}')
    print(f'Password: {password}')
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(f'Signup Status: {response.status_code}')
        print(f'Signup Response: {response.text}')
        
        if response.status_code == 200:
            # Now test login
            login_data = {'username': username, 'password': password}
            login_response = requests.post('http://localhost:8000/auth/login', 
                                         data=json.dumps(login_data), 
                                         headers=headers)
            print(f'Login Status: {login_response.status_code}')
            print(f'Login Response: {login_response.text}')
            
            if login_response.status_code == 200:
                result = login_response.json()
                print(f'*** SUCCESS! Access token: {result.get("access_token", "none")[:50]}...')
                print(f'User ID: {result.get("user_id", "none")}')
                return username, password, result.get('access_token')
        
    except Exception as e:
        print(f'Error: {e}')
        return None, None, None

if __name__ == "__main__":
    create_test_user()