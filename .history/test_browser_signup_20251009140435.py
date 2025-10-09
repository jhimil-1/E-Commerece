#!/usr/bin/env python3
"""
Test script to verify the frontend signup functionality is working correctly
by testing the API endpoints that the frontend uses.
"""

import requests
import json
import random
import string
import time

def generate_test_user():
    """Generate random test user data"""
    username = f"test_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
    email = f"{username}@example.com"
    password = "TestPassword123!"
    return username, email, password

def test_frontend_signup_flow():
    """Test the complete frontend signup flow"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing frontend signup flow...")
    
    # Generate test user
    username, email, password = generate_test_user()
    print(f"Generated test user: {username} ({email})")
    
    try:
        # Test signup endpoint (what frontend calls)
        signup_data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        print(f"Testing signup with data: {json.dumps(signup_data, indent=2)}")
        
        response = requests.post(
            f"{base_url}/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Signup response status: {response.status_code}")
        print(f"Signup response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Signup successful! User ID: {result.get('user_id')}")
            
            # Test login endpoint (what frontend calls)
            login_data = {
                "username": username,  # Frontend uses username for login
                "password": password
            }
            
            print(f"Testing login with data: {json.dumps(login_data, indent=2)}")
            
            login_response = requests.post(
                f"{base_url}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Login response status: {login_response.status_code}")
            print(f"Login response: {login_response.text}")
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"✅ Login successful! Access token: {login_result.get('access_token')[:20]}...")
                
                # Test authenticated endpoint
                auth_headers = {
                    "Authorization": f"Bearer {login_result.get('access_token')}"
                }
                
                # Test search endpoint
                search_response = requests.get(
                    f"{base_url}/jewelry/search",
                    params={"query": "gold ring"},
                    headers=auth_headers
                )
                
                print(f"Search response status: {search_response.status_code}")
                if search_response.status_code == 200:
                    print("✅ Authenticated search endpoint is working!")
                    return True
                else:
                    print(f"❌ Search endpoint failed: {search_response.text}")
                    return False
            else:
                print(f"❌ Login failed: {login_response.text}")
                return False
        else:
            print(f"❌ Signup failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_signup_flow()
    if success:
        print("\n🎉 Frontend signup functionality is working correctly!")
    else:
        print("\n❌ Frontend signup functionality has issues.")
    exit(0 if success else 1)