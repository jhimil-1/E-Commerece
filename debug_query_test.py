#!/usr/bin/env python3
"""
Simple test to debug what query text is being passed to the filtering method.
"""

import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def debug_query_test():
    """Test to see what query text is being used."""
    
    print("🔍 DEBUG QUERY TEST")
    print("=" * 50)
    
    try:
        # Initialize handlers fresh
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)
        
        # Test with a simple headphones query
        query = "headphones"
        print(f"DEBUG: Testing query: '{query}'")
        
        result = await enhanced_handler.search_products_enhanced(query)
        
        if not result or result.get('status') != 'success':
            print(f"❌ Search failed: {result}")
            return False
        
        products = result.get('results', [])
        print(f"DEBUG: Found {len(products)} products")
        
        # Show first few products
        for i, product in enumerate(products[:3]):
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Category: {product.get('category', 'unknown')}")
            print(f"     Semantic score: {product.get('semantic_relevance', 'N/A')}")
            print(f"     Vector score: {product.get('similarity_score', 'N/A')}")
        
        return True
            
    except Exception as e:
        print(f"❌ Error in debug test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(debug_query_test())
    sys.exit(0 if result else 1)