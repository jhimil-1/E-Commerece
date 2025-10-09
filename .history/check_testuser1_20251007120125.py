#!/usr/bin/env python3

from database import MongoDB
from auth import verify_password

db = MongoDB.get_db()
user = db.users.find_one({'username': 'testuser1'})
if user:
    print(f'Username: {user["username"]}')
    print(f'Hashed password: {user["hashed_password"]}')
    print(f'User ID: {user.get("user_id", "none")}')
    
    # Test common passwords
    passwords = ['test123', 'testuser1', 'test123456', 'password123', '123456', 'test']
    for pwd in passwords:
        result = verify_password(pwd, user["hashed_password"])
        print(f'Testing {pwd}: {result}')
        if result:
            print(f'*** FOUND CORRECT PASSWORD: {pwd} ***')
            break
else:
    print('User not found')