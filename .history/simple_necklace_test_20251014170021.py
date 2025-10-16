#!/usr/bin/env python3
"""
Simple test script for necklace search functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler

async def test_necklace_search():
    """Test the necklace search functionality"""
    print("Initializing EnhancedProductHandler...")
    handler = EnhancedProductHandler()
    
    # Test queries
    test_query = "show me necklaces"
    
    print(f"\nTesting query: '{test_query}'")
    response = await handler.search_products_enhanced(
        query=test_query,
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