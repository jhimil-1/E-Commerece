#!/usr/bin/env python3
"""Test script to verify frontend signup functionality"""

import requests
import json

def test_signup():
    """Test the signup endpoint directly"""
    url = "http://localhost:8000/auth/signup"
    
    # Test data
    test_user = {
        "username": "frontend_test_user",
        "email": "frontend_test@example.com", 
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=test_user)
        print(f"Signup status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Signup successful: {result}")
            return True
        else:
            result = response.json()
            print(f"❌ Signup failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_login():
    """Test login with the new user"""
    url = "http://localhost:8000/auth/login"
    
    login_data = {
        "username": "frontend_test_user",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=login_data)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login successful: {result}")
            return result.get("access_token")
        else:
            result = response.json()
            print(f"❌ Login failed: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing frontend signup functionality...")
    
    # Test signup
    signup_success = test_signup()
    
    if signup_success:
        # Test login
        token = test_login()
        if token:
            print(f"🎉 Frontend API test successful! Token: {token[:20]}...")
        else:
            print("❌ Login test failed")
    else:
        print("❌ Signup test failed - checking if user already exists...")
        
        # Try login with existing user
        token = test_login()
        if token:
            print(f"✅ User already exists, login successful! Token: {token[:20]}...")
        else:
            print("❌ Both signup and login failed")