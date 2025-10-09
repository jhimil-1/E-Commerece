from database import MongoDB

db = MongoDB.get_db()

# Check what products testuser1 has
results = list(db.products.find({'created_by': '2560e47c-dde4-4cbd-872f-d02042b58f50'}, {'category': 1, 'name': 1}))
print(f'Found {len(results)} products for testuser1')

categories = {}
for p in results:
    cat = p.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

print('Categories:')
for cat, count in categories.items():
    print(f'  {cat}: {count}')