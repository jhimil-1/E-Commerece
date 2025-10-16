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
    result = await handler.search_products_enhanced('earrings', user_id='test', category='jewelry')
    print(f'Found {result["count"]} products')
    for product in result['products']:
        print(f'- {product["name"]}: {product["category"]}')

asyncio.run(test_search())