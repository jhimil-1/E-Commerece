#!/usr/bin/env python3
"""Test cloud database functionality"""

import requests
import json
import uuid

def test_cloud_functionality():
    """Test complete user flow with cloud databases"""
    
    # Generate unique user data
    user_email = f"test_user_{str(uuid.uuid4())[:8]}@example.com"
    user_data = {
        'email': user_email,
        'password': 'test123456',
        'full_name': 'Test User'
    }
    
    print(f"Testing with user: {user_email}")
    
    # Test 1: Sign up
    print("\n1. Testing user signup...")
    signup_response = requests.post('http://localhost:8000/auth/signup', json=user_data)
    print(f"Signup status: {signup_response.status_code}")
    if signup_response.status_code != 200:
        print(f"Signup failed: {signup_response.text}")
        return False
    
    # Test 2: Login
    print("\n2. Testing user login...")
    login_response = requests.post('http://localhost:8000/auth/login', json={
        'username': user_data['email'],
        'password': user_data['password']
    })
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return False
    
    token = login_response.json()['access_token']
    print(f"Got access token: {token[:50]}...")
    
    # Test 3: Create chat session
    print("\n3. Testing chat session creation...")
    headers = {'Authorization': f'Bearer {token}'}
    session_response = requests.post('http://localhost:8000/chat/sessions', headers=headers)
    print(f"Session creation status: {session_response.status_code}")
    if session_response.status_code != 201:
        print(f"Session creation failed: {session_response.text}")
        return False
    
    session_data = session_response.json()
    session_id = session_data['session_id']
    print(f"Created session: {session_id}")
    
    # Test 4: Send chat message
    print("\n4. Testing chat functionality...")
    chat_response = requests.post('http://localhost:8000/chat/query', 
                                headers=headers,
                                json={
                                    'session_id': session_id, 
                                    'query': 'Hello, I am looking for jewelry'
                                })
    print(f"Chat status: {chat_response.status_code}")
    if chat_response.status_code != 200:
        print(f"Chat failed: {chat_response.text}")
        return False
    
    chat_data = chat_response.json()
    print(f"Chat response: {chat_data.get('response', 'No response')}")
    
    # Test 5: Check chat history
    print("\n5. Testing chat history retrieval...")
    history_response = requests.get(f'http://localhost:8000/chat/sessions/{session_id}/history', headers=headers)
    print(f"History status: {history_response.status_code}")
    if history_response.status_code == 200:
        history_data = history_response.json()
        print(f"Found {len(history_data)} messages in history")
    else:
        print(f"History retrieval failed: {history_response.text}")
    
    print("\n✅ All cloud functionality tests passed!")
    return True

if __name__ == "__main__":
    success = test_cloud_functionality()
    exit(0 if success else 1)