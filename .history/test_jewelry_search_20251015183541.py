#!/usr/bin/env python3

from enhanced_product_handler import search_products_enhanced

print("Testing jewelry search...")
result = search_products_enhanced('earrings', user_id='test', category='jewelry')
print(f'Found {result["count"]} products')
for product in result['results']:
    print(f'- {product["name"]}: {product["category"]}')