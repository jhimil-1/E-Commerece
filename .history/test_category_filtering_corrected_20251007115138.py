#!/usr/bin/env python3

import asyncio
import logging
from product_handler import ProductHandler
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_category_filtering_corrected():
    """Test category filtering with correct case"""
    
    product_handler = ProductHandler()
    
    # testuser's ObjectId
    user_id = "68da3c90a8de50211f8d9f67"
    
    print("=== Testing Category Filtering (Corrected Case) ===\n")
    
    # Test 1: Search with correct case category filter
    print("1. Search with category='Necklaces' (correct case):")
    try:
        results = await product_handler.search_products(
            query="gold jewelry",
            user_id=user_id,
            category="Necklaces",
            limit=10
        )
        
        print(f"   Found {len(results.get('results', []))} products")
        for i, product in enumerate(results.get('results', [])[:5]):
            print(f"   {i+1}. {product.get('name')} (category: {product.get('category')}, score: {product.get('similarity_score')})")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Search with correct case for bracelets
    print("\n2. Search with category='Bracelets' (correct case):")
    try:
        results = await product_handler.search_products(
            query="gold jewelry",
            user_id=user_id,
            category="Bracelets",
            limit=10
        )
        
        print(f"   Found {len(results.get('results', []))} products")
        for i, product in enumerate(results.get('results', [])[:5]):
            print(f"   {i+1}. {product.get('name')} (category: {product.get('category')}, score: {product.get('similarity_score')})")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Search without category filter (should find all jewelry)
    print("\n3. Search without category filter:")
    try:
        results = await product_handler.search_products(
            query="gold jewelry",
            user_id=user_id,
            limit=10
        )
        
        print(f"   Found {len(results.get('results', []))} products")
        for i, product in enumerate(results.get('results', [])[:5]):
            print(f"   {i+1}. {product.get('name')} (category: {product.get('category')}, score: {product.get('similarity_score')})")
            
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_category_filtering_corrected())