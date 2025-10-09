#!/usr/bin/env python3
"""
Debug script to investigate session and user ID issues
"""

import asyncio
import requests
import json
from datetime import datetime

def test_session_creation_and_query():
    """Test the complete flow from login to chat query"""
    
    base_url = "http://localhost:8000"
    
    # Step 1: Login to get token
    print("=== Step 1: Login ===")
    login_data = {
        "username": "testuser1",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.text}")
            return
            
        login_result = login_response.json()
        print(f"Login result: {json.dumps(login_result, indent=2)}")
        
        # Extract token
        token = login_result.get("access_token")
        if not token:
            print("No access token found in login response")
            return
            
        headers = {"Authorization": f"Bearer {token}"}
        
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # Step 2: Create session
    print("\n=== Step 2: Create Session ===")
    try:
        session_response = requests.post(f"{base_url}/chat/sessions", headers=headers)
        print(f"Session creation status: {session_response.status_code}")
        
        if session_response.status_code != 201:
            print(f"Session creation failed: {session_response.text}")
            return
            
        session_result = session_response.json()
        print(f"Session result: {json.dumps(session_result, indent=2)}")
        
        session_id = session_result.get("session_id")
        if not session_id:
            print("No session ID found in response")
            return
            
    except Exception as e:
        print(f"Session creation error: {e}")
        return
    
    # Step 3: Check session in database
    print("\n=== Step 3: Check Session in Database ===")
    try:
        from database import MongoDB
        MongoDB.connect()
        db = MongoDB.get_db()
        
        # Check sessions collection
        sessions_collection = db["sessions"]
        session_doc = sessions_collection.find_one({"session_id": session_id})
        
        if session_doc:
            print(f"Session document: {json.dumps(session_doc, indent=2, default=str)}")
            print(f"User ID in session: {session_doc.get('user_id')}")
        else:
            print(f"No session found with ID: {session_id}")
            
        # Check all recent sessions
        print("\nAll recent sessions:")
        recent_sessions = list(sessions_collection.find().sort("created_at", -1).limit(5))
        for session in recent_sessions:
            print(f"Session ID: {session.get('session_id')}, User ID: {session.get('user_id')}")
            
    except Exception as e:
        print(f"Database check error: {e}")
    
    # Step 4: Test chat query
    print("\n=== Step 4: Test Chat Query ===")
    try:
        query_data = {
            "query": "laptop",
            "session_id": session_id
        }
        
        query_response = requests.post(f"{base_url}/chat/query", 
                                     json=query_data, headers=headers)
        print(f"Chat query status: {query_response.status_code}")
        
        if query_response.status_code != 200:
            print(f"Chat query failed: {query_response.text}")
        else:
            query_result = query_response.json()
            print(f"Chat query result: {json.dumps(query_result, indent=2)}")
            
            # Check if products were found
            products = query_result.get("products", [])
            print(f"Number of products found: {len(products)}")
            
            if products:
                print("First product:")
                print(json.dumps(products[0], indent=2))
            else:
                print("No products found in response")
                
    except Exception as e:
        print(f"Chat query error: {e}")

if __name__ == "__main__":
    test_session_creation_and_query()