from database import MongoDB

mongo = MongoDB()
db = mongo.get_db()
products = list(db.products.find({'category': 'electronics'}))
print(f'Total electronics: {len(products)}')
for i, p in enumerate(products):
    print(f'{i+1}. {p["name"]}')