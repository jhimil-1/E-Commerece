#!/usr/bin/env python3

import asyncio
import logging
from product_handler import ProductHandler
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_multi_user_filtering():
    """Test user filtering with different users"""
    
    product_handler = ProductHandler()
    
    # Test with testuser (should find products)
    user_id1 = "68da3c90a8de50211f8d9f67"  # testuser's ObjectId
    print(f"=== Testing with testuser (user_id: {user_id1}) ===")
    
    try:
        results1 = await product_handler.search_products(
            query="necklace",
            user_id=user_id1,
            limit=5
        )
        
        print(f"Found {len(results1.get('results', []))} products for testuser")
        for i, product in enumerate(results1.get('results', [])):
            print(f"  {i+1}. {product.get('name')} (score: {product.get('similarity_score')})")
            
    except Exception as e:
        print(f"Error with testuser: {e}")
    
    # Test with different user (should not find testuser's products)
    user_id2 = "507f1f77bcf86cd799439011"  # Different user ID
    print(f"\n=== Testing with different user (user_id: {user_id2}) ===")
    
    try:
        results2 = await product_handler.search_products(
            query="necklace",
            user_id=user_id2,
            limit=5
        )
        
        print(f"Found {len(results2.get('results', []))} products for different user")
        for i, product in enumerate(results2.get('results', [])):
            print(f"  {i+1}. {product.get('name')} (score: {product.get('similarity_score')})")
            
    except Exception as e:
        print(f"Error with different user: {e}")
    
    # Test without user filter (should find all products)
    print(f"\n=== Testing without user filter ===")
    
    try:
        results3 = await product_handler.search_products(
            query="necklace",
            limit=5
        )
        
        print(f"Found {len(results3.get('results', []))} products without user filter")
        for i, product in enumerate(results3.get('results', [])):
            print(f"  {i+1}. {product.get('name')} (score: {product.get('similarity_score')}) - Created by: {product.get('created_by')}")
            
    except Exception as e:
        print(f"Error without user filter: {e}")

if __name__ == "__main__":
    asyncio.run(test_multi_user_filtering())