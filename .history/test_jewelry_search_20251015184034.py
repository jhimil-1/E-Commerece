#!/usr/bin/env python3

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler
import asyncio

async def test_search():
    # Initialize the base product handler
    base_handler = ProductHandler()
    
    # Initialize the enhanced handler with the base handler
    handler = EnhancedProductHandler(base_handler)
    
    print("Testing jewelry search...")
    result = await handler.search_products_enhanced('earrings', user_id=None, category='jewelry')
    print(f'Found {result.get("count", 0)} products')
    products = result.get('products', [])
    for product in products:
        print(f'- {product["name"]}: {product["category"]}')

asyncio.run(test_search())