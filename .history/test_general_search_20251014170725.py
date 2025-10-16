#!/usr/bin/env python3
"""
Test script for general image and text search functionality
"""

import asyncio
import base64
import requests
from pathlib import Path
from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler
from clip_utils import CLIPManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test queries for different product types
TEST_QUERIES = [
    # General product categories
    {"query": "red dress", "category": "clothing"},
    {"query": "smartphone", "category": "electronics"},
    {"query": "gold necklace", "category": "jewelry"},
    {"query": "coffee table", "category": "furniture"},
    # Mixed queries
    {"query": "wireless headphones", "category": None},
    {"query": "silver earrings", "category": None}
]

async def test_text_search():
    """Test text search for various product types"""
    print("\n🔍 Testing text search for various products...")
    
    # Initialize handlers
    product_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    for test_case in TEST_QUERIES:
        query = test_case["query"]
        category = test_case["category"]
        
        print(f"\nTesting query: '{query}' (Category: {category or 'auto-detect'})")
        
        # Perform search
        result = await enhanced_handler.search_products(
            query=query,
            category=category,
            limit=5
        )
        
        if result['status'] == 'success':
            products = result['results']
            print(f"Found {len(products)} products")
            
            # Print top results
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
                print(f"     {product.get('description', '')[:100]}...")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")

async def test_image_search():
    """Test image search with text queries"""
    print("\n📸 Testing image search with text queries...")
    
    # Initialize handlers
    product_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(product_handler)
    clip_manager = CLIPManager()
    
    # Generate a simple test embedding (simulating an image)
    test_embedding = clip_manager.get_text_embedding("sample product image")
    
    for test_case in TEST_QUERIES:
        query = test_case["query"]
        category = test_case["category"]
        
        print(f"\nTesting image search with query: '{query}' (Category: {category or 'auto-detect'})")
        
        # Perform search using the test embedding
        result = await enhanced_handler.search_products(
            query=query,
            image_embedding=test_embedding,
            category=category,
            limit=5
        )
        
        if result['status'] == 'success':
            products = result['results']
            print(f"Found {len(products)} products")
            
            # Print top results
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")

async def main():
    """Run all tests"""
    print("=" * 50)
    print("GENERAL PRODUCT SEARCH TEST")
    print("=" * 50)
    
    # Test text search
    await test_text_search()
    
    # Test image search
    await test_image_search()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())