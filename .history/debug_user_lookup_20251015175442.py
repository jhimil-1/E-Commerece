#!/usr/bin/env python3
"""
Debug script to understand user lookup issues
"""

import sys
sys.path.append('.')

from database import MongoDB
from bson import ObjectId

def debug_user_lookup():
    """Debug user lookup process"""
    print("=== DEBUG USER LOOKUP ===")
    
    # Get database
    db = MongoDB.get_db()
    
    # Test user ID
    test_user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    
    print(f"Testing user ID: {test_user_id}")
    
    # Check if it's a valid ObjectId
    try:
        ObjectId(test_user_id)
        print("Valid ObjectId format")
    except:
        print("Not a valid ObjectId format")
    
    # Try different lookup methods
    print("\n1. Trying ObjectId lookup...")
    try:
        user = db.users.find_one({"_id": ObjectId(test_user_id)})
        print(f"ObjectId lookup result: {user is not None}")
        if user:
            print(f"Username: {user.get('username')}")
            print(f"User ID: {user.get('user_id')}")
    except Exception as e:
        print(f"ObjectId lookup error: {e}")
    
    print("\n2. Trying UUID lookup...")
    try:
        user = db.users.find_one({"user_id": test_user_id})
        print(f"UUID lookup result: {user is not None}")
        if user:
            print(f"Username: {user.get('username')}")
            print(f"User ID: {user.get('user_id')}")
    except Exception as e:
        print(f"UUID lookup error: {e}")
    
    print("\n3. Trying username lookup...")
    try:
        user = db.users.find_one({"username": test_user_id})
        print(f"Username lookup result: {user is not None}")
        if user:
            print(f"Username: {user.get('username')}")
            print(f"User ID: {user.get('user_id')}")
    except Exception as e:
        print(f"Username lookup error: {e}")
    
    print("\n4. Check all users...")
    try:
        users = list(db.users.find().limit(10))
        print(f"Found {len(users)} users")
        for user in users:
            print(f"- Username: {user.get('username')}, User ID: {user.get('user_id')}, _id: {user.get('_id')}")
    except Exception as e:
        print(f"Error listing users: {e}")

if __name__ == "__main__":
    debug_user_lookup()