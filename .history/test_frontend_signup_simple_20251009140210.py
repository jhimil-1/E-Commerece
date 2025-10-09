#!/usr/bin/env python3
"""
Simple test to verify frontend signup functionality is working
"""
import requests
import json
import random
import string

def test_signup():
    """Test the signup endpoint directly"""
    base_url = "http://localhost:8000"
    
    # Generate a random username to avoid conflicts
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    username = f"test_user_{random_suffix}"
    email = f"{username}@example.com"
    password = "testpassword123"
    
    print(f"🧪 Testing signup with username: {username}")
    
    # Test signup
    signup_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{base_url}/auth/signup", json=signup_data)
        print(f"Signup response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Signup successful: {result}")
            
            # Test login with the new user
            login_data = {
                "username": email,  # Frontend uses email as username
                "password": password
            }
            
            login_response = requests.post(f"{base_url}/auth/login", json=login_data)
            print(f"Login response status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"✅ Login successful: {login_result}")
                return True
            else:
                print(f"❌ Login failed: {login_response.text}")
                return False
                
        elif response.status_code == 400:
            result = response.json()
            print(f"❌ Signup failed: {result}")
            return False
        else:
            print(f"❌ Unexpected response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("Testing frontend signup functionality...")
    success = test_signup()
    if success:
        print("\n🎉 Frontend signup functionality is working correctly!")
    else:
        print("\n❌ Frontend signup functionality has issues.")