#!/usr/bin/env python3

import asyncio
import logging
from database import MongoDB
from product_handler import product_handler
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

# Set up logging
logging.basicConfig(level=logging.DEBUG)

async def debug_product_handler():
    """Debug the product handler search functionality"""
    
    # Get user ID for testuser1
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser1'})
    if not user:
        print("testuser1 not found")
        return
    
    user_id = user['user_id']
    print(f"testuser1 user_id: {user_id}")
    
    # Test direct Qdrant search first
    print("\n=== Testing direct Qdrant search ===")
    test_embedding = clip_manager.get_text_embedding("rings")
    print(f"Generated embedding: {len(test_embedding)} dimensions")
    
    qdrant_results = qdrant_manager.search_similar_products(
        query_embedding=test_embedding,
        user_id=user_id,
        limit=5
    )
    print(f"Direct Qdrant results: {len(qdrant_results)}")
    for r in qdrant_results:
        print(f"  - {r['name']} (score: {r['score']:.3f})")
    
    # Test product handler search
    print("\n=== Testing product_handler.search_products ===")
    
    try:
        results = await product_handler.search_products(
            query="rings",
            user_id=user_id,
            limit=5,
            min_score=0.1
        )
        
        print(f"Product handler results: {results}")
        
    except Exception as e:
        print(f"Error in product handler search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_product_handler())