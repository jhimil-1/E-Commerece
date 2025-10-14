#!/usr/bin/env python3

import sys
import asyncio
sys.path.append('.')

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def debug_similar_search():
    """Debug the similar product search issue"""
    
    # Initialize handlers
    product_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    print("Debugging similar product search...")
    print("=" * 60)
    
    # Test what happens when we search for "Men's Chronograph Watch"
    query = "Men's Chronograph Watch"
    print(f"\nTesting query: '{query}'")
    print("-" * 40)
    
    try:
        result = await enhanced_handler.search_products_enhanced(query)
        
        print(f"Search status: {result.get('status')}")
        print(f"Original count: {result.get('metadata', {}).get('original_count', 0)}")
        print(f"Filtered count: {result.get('metadata', {}).get('filtered_count', 0)}")
        
        products = result.get('results', [])
        print(f"Final products: {len(products)}")
        
        if products:
            print("\nFirst few products:")
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')}")
                print(f"     Category: {product.get('category', 'unknown')}")
                print(f"     Price: ${product.get('price', 'N/A')}")
                print(f"     Vector score: {product.get('similarity_score', 'N/A')}")
                print(f"     Semantic relevance: {product.get('semantic_relevance', 'N/A')}")
                print(f"     Enhanced score: {product.get('enhanced_score', 'N/A')}")
        else:
            print("No products found!")
            
            # Let's also test the original product handler to see what it finds
            print("\nTesting original product handler...")
            original_result = await product_handler.search_products(query)
            original_products = original_result.get('results', [])
            print(f"Original handler found: {len(original_products)} products")
            
            if original_products:
                print("\nFirst few from original:")
                for i, product in enumerate(original_products[:3], 1):
                    print(f"  {i}. {product.get('name', 'Unknown')}")
                    print(f"     Category: {product.get('category', 'unknown')}")
                    print(f"     Price: ${product.get('price', 'N/A')}")
                    print(f"     Vector score: {product.get('similarity_score', 'N/A')}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_similar_search())