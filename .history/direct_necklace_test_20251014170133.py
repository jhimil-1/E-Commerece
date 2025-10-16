#!/usr/bin/env python3
"""
Direct test script for necklace image search functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler
from enhanced_product_handler import EnhancedProductHandler

async def test_necklace_search():
    """Test the necklace search functionality directly"""
    print("Initializing ProductHandler...")
    base_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(base_handler)
    
    # Test necklace search
    test_query = "show me necklaces"
    
    print(f"\nTesting query: '{test_query}'")
    response = await enhanced_handler.search_jewelry_by_image_and_category(
        text_query=test_query,
        category="necklaces",
        limit=5
    )
    
    print("\nResponse status:", response.get('status', 'No status'))
    
    if 'results' in response and response['results']:
        print(f"\nFound {len(response['results'])} products:")
        for i, product in enumerate(response['results']):
            print(f"{i+1}. {product.get('name')} - ${product.get('price')}")
            print(f"   {product.get('description')}")
    else:
        print("No products found")

if __name__ == "__main__":
    asyncio.run(test_necklace_search())