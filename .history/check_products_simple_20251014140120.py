from database import MongoDB

mongo = MongoDB()
db = mongo.get_db()

# Check for watch-related products
watch_products = list(db.products.find({
    '$or': [
        {'name': {'$regex': 'watch', '$options': 'i'}},
        {'name': {'$regex': 'smartwatch', '$options': 'i'}},
        {'description': {'$regex': 'watch', '$options': 'i'}}
    ]
}))

print('Watch/Smartwatch products:')
for p in watch_products:
    print(f'  - {p["name"]} (${p["price"]}) - {p["category"]}')

# Check for clothing products
clothing_products = list(db.products.find({'category': {'$regex': 'clothing', '$options': 'i'}}))
print(f'\nClothing products ({len(clothing_products)}):')
for p in clothing_products[:10]:
    print(f'  - {p["name"]} (${p["price"]})')

if len(clothing_products) > 10:
    print(f'  ... and {len(clothing_products) - 10} more')

# Check for jewellery products
jewellery_products = list(db.products.find({'category': 'Jewelry'}))
print(f'\nJewellery products ({len(jewellery_products)}):')
for p in jewellery_products:
    print(f'  - {p["name"]} (${p["price"]})')

mongo.close()