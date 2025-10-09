#!/usr/bin/env python3
"""
Test script to verify the search functionality and see what products are being returned
"""

import requests
import json
import random
import string

def generate_test_user():
    """Generate random test user data"""
    username = f"test_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
    email = f"{username}@example.com"
    password = "TestPassword123!"
    return username, email, password

def test_search_functionality():
    """Test the complete search functionality"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing search functionality...")
    
    # Generate test user
    username, email, password = generate_test_user()
    print(f"Generated test user: {username} ({email})")
    
    try:
        # Sign up and login first
        signup_data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        print("Creating user...")
        signup_response = requests.post(
            f"{base_url}/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        
        if signup_response.status_code != 200:
            print(f"Signup failed: {signup_response.text}")
            return False
            
        # Login
        login_data = {
            "username": username,
            "password": password
        }
        
        print("Logging in...")
        login_response = requests.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.text}")
            return False
            
        login_result = login_response.json()
        access_token = login_result.get('access_token')
        
        # Create a chat session
        print("Creating chat session...")
        session_response = requests.post(
            f"{base_url}/chat/sessions",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if session_response.status_code != 201:
            print(f"Session creation failed: {session_response.text}")
            return False
            
        session_data = session_response.json()
        session_id = session_data.get('session_id')
        print(f"Created session: {session_id}")
        
        # Test search query
        search_query = {
            "query": "smartphone",
            "session_id": session_id
        }
        
        print(f"Testing search with query: {search_query}")
        search_response = requests.post(
            f"{base_url}/chat/query",
            json=search_query,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"Search response status: {search_response.status_code}")
        print(f"Search response: {search_response.text}")
        
        if search_response.status_code == 200:
            result = search_response.json()
            print(f"✅ Search successful!")
            print(f"Response structure: {json.dumps(result, indent=2)}")
            
            # Check what products are returned
            if 'results' in result:
                products = result['results']
                print(f"Found {len(products)} products")
                for i, product in enumerate(products[:3]):  # Show first 3 products
                    print(f"Product {i+1}: {product}")
            elif 'products' in result:
                products = result['products']
                print(f"Found {len(products)} products")
                for i, product in enumerate(products[:3]):  # Show first 3 products
                    print(f"Product {i+1}: {product}")
            else:
                print("No products found in response")
                
            return True
        else:
            print(f"❌ Search failed: {search_response.text}")
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
    success = test_search_functionality()
    if success:
        print("\n🎉 Search functionality is working correctly!")
    else:
        print("\n❌ Search functionality has issues.")
    exit(0 if success else 1)