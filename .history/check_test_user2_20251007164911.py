from database import MongoDB

db = MongoDB.get_db()

# Find test_user2
user = db.users.find_one({'username': 'test_user2'})
if user:
    user_id = user.get('user_id', str(user['_id']))
    print(f'User ID: {user_id}')
    
    # Check products with exact user_id
    count = db.products.count_documents({'created_by': user_id})
    print(f'Found {count} products with exact user_id')
    
    # Check products with database ID
    db_id = str(user['_id'])
    count2 = db.products.count_documents({'created_by': db_id})
    print(f'Found {count2} products with database ID')
    
    # Show sample products
    print('\nSample products:')
    results = list(db.products.find({'created_by': user_id}, {'category': 1, 'name': 1}).limit(5))
    for p in results:
        print(f'- {p.get("name", "Unknown")} (category: {p.get("category", "none")})')
        
    # Show all categories for this user
    print('\nAll categories:')
    categories = db.products.distinct('category', {'created_by': user_id})
    print(categories)
else:
    print('test_user2 not found')