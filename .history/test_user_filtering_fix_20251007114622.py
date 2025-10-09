#!/usr/bin/env python3

import asyncio
import logging
from product_handler import ProductHandler
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_user_filtering_fix():
    """Test that user filtering now works correctly with the fix"""
    
    product_handler = ProductHandler()
    
    # Test user - testuser (MongoDB ObjectId)
    user_id = "68da3c90a8de50211f8d9f67"  # testuser's ObjectId
    
    print(f"Testing search with user_id: {user_id}")
    
    # Test search query
    query = "necklace"
    
    try:
        # Search products
        results = await product_handler.search_products(
            query=query,
            user_id=user_id,
            limit=5
        )
        
        print(f"Search results status: {results.get('status', 'unknown')}")
        print(f"Number of results: {len(results.get('results', []))}")
        
        if results.get('results'):
            for i, product in enumerate(results['results']):
                print(f"\nResult {i+1}:")
                print(f"  Name: {product.get('name')}")
                print(f"  Category: {product.get('category')}")
                print(f"  Created by: {product.get('created_by')}")
                print(f"  Similarity score: {product.get('similarity_score')}")
                
                # Check if the product belongs to the user
                if product.get('similarity_score', 0) > 0:
                    print(f"  ✓ Product belongs to user")
                else:
                    print(f"  ✗ Product hidden (score = 0)")
        else:
            print("No products found")
            
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_user_filtering_fix())