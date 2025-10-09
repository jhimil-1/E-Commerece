#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
from qdrant_client import models

async def debug_user_id_issue():
    """Debug the user_id vs username issue"""
    
    # Get user ID for testuser
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser'})
    if not user:
        print("testuser not found")
        return
    
    user_id = str(user['_id'])
    username = user['username']
    
    print(f"testuser details:")
    print(f"  user_id (MongoDB ObjectId): {user_id}")
    print(f"  username: {username}")
    
    # Check what products have in their created_by field
    product = db.products.find_one({"created_by": "testuser"})
    if product:
        print(f"Product created_by field: {product['created_by']}")
    
    # Now let's see what the product_handler is doing
    from product_handler import ProductHandler
    
    handler = ProductHandler()
    
    print(f"\n=== Testing product_handler.search_products ===")
    print(f"Calling with user_id: {user_id}")
    
    # This is what product_handler does internally
    query_embedding = clip_manager.get_text_embedding("rings")
    print(f"Generated embedding for 'rings'")
    
    # This is the call that fails
    search_results = qdrant_manager.search_similar_products(
        query_embedding=query_embedding,
        user_id=user_id,  # This is the problem - it's passing user_id instead of username
        category_filter=None,
        limit=5,
        min_score=0.0
    )
    
    print(f"Results from search_similar_products with user_id: {len(search_results)}")
    
    # Now try with username
    search_results = qdrant_manager.search_similar_products(
        query_embedding=query_embedding,
        user_id=username,  # Use username instead
        category_filter=None,
        limit=5,
        min_score=0.0
    )
    
    print(f"Results from search_similar_products with username: {len(search_results)}")
    for result in search_results:
        print(f"  Score: {result['score']}, Name: {result['name']}, Category: {result['category']}")

if __name__ == "__main__":
    asyncio.run(debug_user_id_issue())