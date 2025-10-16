#!/usr/bin/env python3

from enhanced_product_handler import EnhancedProductHandler
import asyncio

async def test_search():
    handler = EnhancedProductHandler()
    print("Testing jewelry search...")
    result = await handler.search_products_enhanced('earrings', user_id='test', category='jewelry')
    print(f'Found {result["count"]} products')
    for product in result['results']:
        print(f'- {product["name"]}: {product["category"]}')

asyncio.run(test_search())