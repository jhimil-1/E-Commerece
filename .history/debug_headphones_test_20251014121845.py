#!/usr/bin/env python3
"""
Simple debug test for headphones detection
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def debug_headphones():
    """Test headphones detection with simple queries"""
    # Create the base product handler first
    base_handler = ProductHandler()
    handler = EnhancedProductHandler(base_handler)
    
    test_queries = [
        "headphones",
        "Show me headphones", 
        "headphone",
        "earbuds",
        "earphone"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: '{query}'")
        print(f"{'='*60}")
        
        # Test the filtering method directly
        test_products = [
            {
                'name': 'Noise Cancelling Headphones',
                'description': 'Premium noise cancelling headphones with superior sound quality',
                'category': 'electronics',
                'similarity_score': 0.8
            },
            {
                'name': 'Wireless Earbuds Pro',
                'description': 'True wireless earbuds with active noise cancellation',
                'category': 'electronics', 
                'similarity_score': 0.7
            },
            {
                'name': 'Smart Home Hub',
                'description': 'Control your smart home devices with voice commands',
                'category': 'electronics',
                'similarity_score': 0.6
            }
        ]
        
        print(f"Testing filter_irrelevant_results directly...")
        filtered = handler.filter_irrelevant_results(query, test_products, min_semantic_score=None)
        print(f"Filtered results: {len(filtered)} products")
        
        for product in filtered:
            print(f"  - {product['name']}: semantic_relevance={product.get('semantic_relevance', 'N/A')}, enhanced_score={product.get('enhanced_score', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(debug_headphones())