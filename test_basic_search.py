#!/usr/bin/env python3

from product_handler import ProductHandler
import asyncio

async def test_basic_search():
    handler = ProductHandler()
    result = await handler.search_products('earrings', user_id=None, category=None, min_score=0.0, limit=10)
    print(f'Basic search found {len(result.get("products", []))} products')
    if result.get('products'):
        for product in result['products'][:3]:
            print(f'- {product["name"]} (category: {product.get("category", "N/A")})')

asyncio.run(test_basic_search())