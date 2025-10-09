#!/usr/bin/env python3

from database import MongoDB

def check_users():
    db = MongoDB.get_db()
    users = list(db.users.find({}))
    
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"  - {user['username']} (ID: {str(user['_id'])})")
    
    # Check if testuser exists
    testuser = db.users.find_one({"username": "testuser"})
    if testuser:
        print(f"\n✓ testuser exists with ID: {str(testuser['_id'])}")
    else:
        print(f"\n✗ testuser not found")
    
    # Check if testuser1 exists
    testuser1 = db.users.find_one({"username": "testuser1"})
    if testuser1:
        print(f"✓ testuser1 exists with ID: {str(testuser1['_id'])}")
    else:
        print(f"✗ testuser1 not found")

if __name__ == "__main__":
    check_users()