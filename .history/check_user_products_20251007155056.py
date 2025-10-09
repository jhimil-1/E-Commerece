from database import MongoDB

db = MongoDB.get_db()

# Check what electronics products testuser1 has
products = list(db.products.find({'category': 'electronics', 'created_by': '2560e47c-dde4-4cbd-872f-d02042b58f50'}))
print(f'Electronics products for testuser1: {len(products)}')
for p in products:
    print(f'- {p["name"]} (category: {p["category"]})')

print()

# Check what laptop products testuser1 has  
laptop_products = list(db.products.find({'category': 'laptops', 'created_by': '2560e47c-dde4-4cbd-872f-d02042b58f50'}))
print(f'Laptop products for testuser1: {len(laptop_products)}')
for p in laptop_products:
    print(f'- {p["name"]} (category: {p["category"]})')

print()

# Check all categories testuser1 has
pipeline = [
    {'$match': {'created_by': '2560e47c-dde4-4cbd-872f-d02042b58f50'}},
    {'$group': {'_id': '$category', 'count': {'$sum': 1}}}
]
categories = list(db.products.aggregate(pipeline))
print('All categories for testuser1:')
for cat in categories:
    print(f'- {cat["_id"]}: {cat["count"]} products')