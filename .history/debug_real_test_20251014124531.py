#!/usr/bin/env python3
"""
Debug the real test environment to see exact scores
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler
from database import MongoDB
from auth import Auth

async def debug_real_test():
    """Debug the actual test environment"""
    
    # Initialize handlers
    db = Database()
    auth = Auth(db)
    product_handler = ProductHandler(db, auth)
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    # Test the actual query from the test
    query = "Show me headphones"
    
    print(f"Testing query: '{query}'")
    print("=" * 50)
    
    # Run the enhanced search
    result = await enhanced_handler.search_products_enhanced(query)
    
    if result['status'] == 'success':
        products = result['results']
        print(f"Found {len(products)} products after filtering")
        print()
        
        headphones_count = 0
        for i, product in enumerate(products, 1):
            name = product.get('name', 'Unknown')
            category = product.get('category', 'Unknown')
            semantic_score = product.get('semantic_relevance', 0)
            vector_score = product.get('similarity_score', 0)
            enhanced_score = product.get('enhanced_score', 0)
            
            is_headphones = any(word in name.lower() for word in ['headphones', 'headphone', 'earbuds', 'earphone'])
            if is_headphones:
                headphones_count += 1
            
            print(f"{i}. {name}")
            print(f"   Category: {category}")
            print(f"   Semantic: {semantic_score:.3f}")
            print(f"   Vector: {vector_score:.3f}")
            print(f"   Enhanced: {enhanced_score:.3f}")
            print(f"   Is Headphones: {is_headphones}")
            print()
        
        relevance_ratio = (headphones_count / len(products)) * 100 if products else 0
        print(f"Headphones relevance ratio: {relevance_ratio:.1f}%")
        print(f"Headphones products: {headphones_count} / {len(products)}")
        
    else:
        print(f"Search failed: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(debug_real_test())