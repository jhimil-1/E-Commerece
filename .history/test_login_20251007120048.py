#!/usr/bin/env python3

import requests
import json

def test_login():
    url = 'http://localhost:8000/auth/login'
    headers = {'Content-Type': 'application/json'}
    
    # Test with testuser1 (has user_id field)
    data = {'username': 'testuser1', 'password': 'test123'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f'Test 1 - testuser1 with test123:')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
    print()
    
    # Test with testuser1 and different passwords
    passwords = ['testuser1', 'test123456', 'password123']
    for pwd in passwords:
        data = {'username': 'testuser1', 'password': pwd}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(f'Test - testuser1 with {pwd}:')
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            print('SUCCESS: Login worked!')
            result = response.json()
            print(f'Access token: {result.get("access_token", "none")[:50]}...')
            print(f'User ID: {result.get("user_id", "none")}')
            break
        else:
            print(f'Response: {response.text}')
        print()

if __name__ == "__main__":
    test_login()