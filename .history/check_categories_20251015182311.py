#!/usr/bin/env python3

from database import get_database
from bson import ObjectId

db = get_database()
product_ids = ['68ef7aeb4c29fbc709bc3487', '68ef7aeb4c29fbc709bc348b', '68ef7aeb4c29fbc709bc349a', '68ef7aeb4c29fbc709bc3490', '68ef7aeb4c29fbc709bc347c']

print("Checking product categories:")
for pid in product_ids:
    product = db.products.find_one({'_id': ObjectId(pid)})
    if product:
        print(f"{product.get('name', 'Unknown')} - Category: {product.get('category', 'No category')}")
    else:
        print(f"Product {pid} not found")