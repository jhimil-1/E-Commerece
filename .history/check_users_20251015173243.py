from database import MongoDB

db = MongoDB.get_db()
users = list(db.users.find({}, {'username': 1, 'user_id': 1}))
print(f'Users found: {len(users)}')
for user in users[:5]:
    username = user.get('username', 'unknown')
    user_id = user.get('user_id', str(user.get('_id')))
    print(f'User: {username} - ID: {user_id}')