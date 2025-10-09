#!/usr/bin/env python3

from database import MongoDB
import requests
import json

def debug_session():
    # Create a session as testuser1
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    login_response = requests.post(
        "http://localhost:8000/auth/login",
        json=login_data
    )
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token_data = login_response.json()
    token = token_data["access_token"]
    user_id = token_data["user_id"]
    
    print(f"Logged in as testuser1")
    print(f"User ID from token: {user_id}")
    
    # Create session
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    session_response = requests.post(
        "http://localhost:8000/chat/sessions",
        headers=headers
    )
    
    if session_response.status_code != 201:
        print(f"Session creation failed: {session_response.text}")
        return
    
    session_data = session_response.json()
    session_id = session_data["session_id"]
    
    print(f"Created session: {session_id}")
    
    # Check session in database
    db = MongoDB.get_db()
    session_doc = db.sessions.find_one({"session_id": session_id})
    
    if session_doc:
        print(f"Session user_id: {session_doc.get('user_id')}")
        print(f"Session data: {session_doc}")
    else:
        print("Session not found in database")
    
    # Check what products exist for different users
    print("\n=== Product ownership ===")
    products = list(db.products.find({}).limit(10))
    for product in products:
        print(f"Product: {product.get('name')} - Created by: {product.get('created_by')}")
    
    # Check user mapping
    print("\n=== User mapping ===")
    users = list(db.users.find({"username": {"$in": ["testuser", "testuser1"]}}))
    for user in users:
        print(f"Username: {user['username']} - ID: {str(user['_id'])}")

if __name__ == "__main__":
    debug_session()