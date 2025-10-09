#!/usr/bin/env python3

import asyncio
from database import MongoDB
from product_handler import product_handler
from auth import get_current_user
from fastapi import Depends

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
    
    # Test product handler search
    print("\n=== Testing product_handler.search_products ===")
    
    try:
        results = await product_handler.search_products(
            query="rings",
            user_id=user_id,
            limit=5,
            min_score=0.1
        )
        
        print(f"Search results: {results}")
        print(f"Search keys: {results.keys()}")
        
        if 'results' in results:
            for i, product in enumerate(results['results']):
                print(f"  {i+1}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} - Score: {product.get('similarity_score', 0)}")
        else:
            print("No results key found")
            
    except Exception as e:
        print(f"Error in product handler search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_product_handler())