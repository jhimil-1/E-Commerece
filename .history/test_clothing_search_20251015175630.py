#!/usr/bin/env python3
"""
Test search with clothing-related query since the user has clothing products
"""

import sys
sys.path.append('.')

from product_handler import ProductHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_clothing_search():
    """Test search with clothing-related query"""
    print("=== TEST CLOTHING SEARCH ===")
    
    # Initialize product handler
    product_handler = ProductHandler()
    
    # Test parameters
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    
    # Test different queries
    test_queries = [
        "jacket",
        "leather jacket", 
        "chinos",
        "sweater",
        "dress",
        "jeans"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        
        # Test with category filter
        result = product_handler.search_products(
            query=query,
            user_id=user_id,
            category="Clothing",
            limit=5,
            min_score=0.0
        )
        
        print(f"With 'Clothing' category: {len(result.get('results', []))} products")
        if result.get('results'):
            for product in result['results']:
                print(f"  - {product.get('name')} (score: {product.get('relevance_score', 0):.2f})")
        
        # Test without category filter
        result = product_handler.search_products(
            query=query,
            user_id=user_id,
            limit=5,
            min_score=0.0
        )
        
        print(f"Without category: {len(result.get('results', []))} products")
        if result.get('results'):
            for product in result['results']:
                print(f"  - {product.get('name')} (score: {product.get('relevance_score', 0):.2f})")

if __name__ == "__main__":
    test_clothing_search()