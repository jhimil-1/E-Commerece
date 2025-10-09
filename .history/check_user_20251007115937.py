#!/usr/bin/env python3

from database import MongoDB
from auth import verify_password

db = MongoDB.get_db()
user = db.users.find_one({'username': 'testuser'})
if user:
    print(f'Username: {user["username"]}')
    print(f'Hashed password: {user["hashed_password"]}')
    print(f'Testing with password test123: {verify_password("test123", user["hashed_password"])}')
else:
    print('User not found')