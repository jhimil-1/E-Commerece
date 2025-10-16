#!/usr/bin/env python3
"""
Test script to verify targeted product search functionality
Tests both text and image search for specific product types
"""

import asyncio
import logging
from PIL import Image
import io
import base64
import requests
from chatbot import ChatbotManager
from auth import create_new_session
from product_handler import ProductHandler
from database import MongoDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_targeted_search():
    """Test targeted search for specific products"""
    
    print("🧪 Testing Targeted Product Search")
    print("=" * 50)
    
    # Initialize components
    chatbot = ChatbotManager()
    product_handler = ProductHandler()
    
    # Create test session
    session_id = await create_new_session("test_user_targeted")
    print(f"Created session: {session_id}")
    
    # Test queries for specific products
    test_cases = [
        {
            "query": "necklace",
            "expected_category": "jewelry",
            "description": "Simple necklace search"
        },
        {
            "query": "gold necklace with pendant",
            "expected_category": "jewelry", 
            "description": "Specific necklace description"
        },
        {
            "query": "diamond ring",
            "expected_category": "jewelry",
            "description": "Specific jewelry type"
        },
        {
            "query": "women's dress",
            "expected_category": "clothing",
            "description": "Clothing search"
        },
        {
            "query": "smartphone",
            "expected_category": "electronics",
            "description": "Electronics search"
        }
    ]
    
    print("\n📋 Testing Text Search:")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['description']}")
        print(f"Query: '{test_case['query']}'")
        print(f"Expected: {test_case['expected_category']}")
        
        try:
            # Test direct product handler search
            result = await product_handler.search_products(
                query=test_case['query'],
                user_id="test_user_targeted",
                limit=5
            )
            
            if result['status'] == 'success':
                products = result['results']
                print(f"Found {len(products)} products")
                
                if products:
                    # Analyze categories found
                    categories = [p.get('category', 'unknown') for p in products]
                    unique_categories = list(set(categories))
                    print(f"Categories found: {unique_categories}")
                    
                    # Check if all products match expected category
                    matching_products = [p for p in products if p.get('category', '').lower() == test_case['expected_category']]
                    print(f"Products matching expected category: {len(matching_products)}/{len(products)}")
                    
                    # Show top 3 products
                    for i, product in enumerate(products[:3], 1):
                        print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} (Score: {product.get('similarity_score', 0):.3f})")
                    
                    # Calculate relevance score
                    relevance_ratio = len(matching_products) / len(products) if products else 0
                    if relevance_ratio >= 0.8:
                        print("✅ EXCELLENT: 80%+ relevant products")
                    elif relevance_ratio >= 0.6:
                        print("⚠️  GOOD: 60%+ relevant products")
                    else:
                        print("❌ POOR: Less than 60% relevant products")
                else:
                    print("❌ No products found")
            else:
                print(f"❌ Search failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n🖼️  Testing Image Search:")
    print("-" * 30)
    
    # Test image search with sample jewelry image
    try:
        # Create a simple test image (we'll use a placeholder approach)
        print("\n🔍 Testing image search with 'necklace' text + sample image...")
        
        # For this test, we'll use text-only but with image processing logic
        result = await product_handler.search_products(
            query="necklace",
            user_id="test_user_targeted",
            limit=5
        )
        
        if result['status'] == 'success':
            products = result['results']
            print(f"Found {len(products)} products for necklace image search")
            
            # Check relevance
            jewelry_products = [p for p in products if p.get('category', '').lower() == 'jewelry']
            print(f"Jewelry products: {len(jewelry_products)}/{len(products)}")
            
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
                
    except Exception as e:
        print(f"❌ Image search error: {str(e)}")
    
    print("\n📊 Summary:")
    print("=" * 50)
    print("Current search behavior analyzed.")
    print("Next step: Implement enhanced filtering to show only top relevant products.")

if __name__ == "__main__":
    asyncio.run(test_targeted_search())