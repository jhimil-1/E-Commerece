from database import MongoDB

db = MongoDB.get_db()

# Find test_user2
user = db.users.find_one({'username': 'test_user2'})
if user:
    user_id = user.get('user_id', str(user['_id']))
    print(f'User ID: {user_id}')
    
    # Check products
    results = list(db.products.find({'created_by': user_id}, {'category': 1, 'name': 1}))
    print(f'Found {len(results)} products for test_user2')
    for p in results:
        print(f'- {p.get("name", "Unknown")} (category: {p.get("category", "none")})')
else:
    print('test_user2 not found')