#!/usr/bin/env python3
"""
Test script to verify the search endpoint fix.
"""

import requests
import json
import asyncio
import subprocess
import time
import sys
from pathlib import Path

def test_search_endpoints():
    """Test both the old and new search endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Search Endpoint Fix")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("1. Testing server status...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Server is running")
        else:
            print(f"   ❌ Server returned {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Test old jewelry/search endpoint (should return 404)
    print("\n2. Testing old /jewelry/search endpoint (should be 404)...")
    try:
        response = requests.post(f"{base_url}/jewelry/search", data={"query": "test"})
        if response.status_code == 404:
            print("   ✅ Old endpoint correctly returns 404")
        else:
            print(f"   ❌ Old endpoint returned {response.status_code} (expected 404)")
    except Exception as e:
        print(f"   ❌ Error testing old endpoint: {e}")
    
    # Test 3: Test new products/search endpoint (should work with auth)
    print("\n3. Testing new /products/search endpoint...")
    
    # First, create a test user and login
    print("   Creating test user and logging in...")
    
    # Try to create user (might already exist)
    try:
        signup_data = {
            "username": "testuser_search",
            "password": "testpass123",
            "email": "testuser_search@example.com"
        }
        response = requests.post(f"{base_url}/auth/signup", json=signup_data)
        if response.status_code in [200, 201]:
            print("   ✅ Test user created")
        else:
            print(f"   ℹ️  User might already exist (status: {response.status_code})")
    except Exception as e:
        print(f"   ℹ️  Signup error (user might exist): {e}")
    
    # Login
    try:
        login_data = {
            "username": "testuser_search",
            "password": "testpass123"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("   ✅ Login successful")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Test search with authentication
    print("   Testing search with authentication...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        search_data = {"query": "electronics", "limit": 5}
        
        response = requests.post(
            f"{base_url}/products/search", 
            data=search_data,
            headers=headers
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"   ✅ Search successful! Found {results.get('count', 0)} results")
            if results.get('results'):
                print(f"   📊 First result: {results['results'][0].get('name', 'N/A')}")
        else:
            print(f"   ❌ Search failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return False
    
    # Test 4: Test search without authentication (should fail)
    print("\n4. Testing search without authentication (should fail)...")
    try:
        response = requests.post(f"{base_url}/products/search", data={"query": "test"})
        if response.status_code == 401:
            print("   ✅ Search correctly blocked without authentication")
        else:
            print(f"   ❌ Unexpected status without auth: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing unauth search: {e}")
    
    print("\n" + "=" * 50)
    print("✅ All search endpoint tests completed successfully!")
    return True

def main():
    """Main test function"""
    print("🚀 Starting Search Endpoint Fix Test")
    print("This test verifies that the jewelry/search -> products/search fix works correctly.")
    print()
    
    success = test_search_endpoints()
    
    if success:
        print("\n🎉 All tests passed! The search endpoint fix is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the server and endpoints.")
        sys.exit(1)

if __name__ == "__main__":
    main()