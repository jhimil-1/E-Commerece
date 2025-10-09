#!/usr/bin/env python3

from database import MongoDB

def check_users():
    db = MongoDB.get_db()
    users = list(db.users.find({}, {'_id': 1, 'username': 1, 'user_id': 1, 'hashed_password': 1}))
    
    print("Current users in database:")
    for user in users:
        print(f"Username: {user.get('username', 'unknown')}")
        print(f"  _id: {user.get('_id', 'none')}")
        print(f"  user_id: {user.get('user_id', 'none')}")
        print(f"  has password: {'yes' if 'hashed_password' in user else 'no'}")
        print()

if __name__ == "__main__":
    check_users()