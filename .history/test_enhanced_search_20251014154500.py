#!/usr/bin/env python3
"""
Test script to verify enhanced product search functionality
Tests the EnhancedProductHandler for targeted product filtering
"""

import asyncio
import logging
from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler
from database import MongoDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_enhanced_search():
    """Test enhanced search for specific products"""
    
    print("🧪 Testing Enhanced Product Search")
    print("=" * 50)
    
    # Initialize components
    base_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(base_handler)
    
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
    
    print("\n📋 Testing Enhanced Text Search:")
    print("-" * 40)
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['description']}")
        print(f"Query: '{test_case['query']}'")
        print(f"Expected: {test_case['expected_category']}")
        
        try:
            # Test enhanced handler search
            result = await enhanced_handler.search_products(
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
                    
                    # Show top 3 products with relevance scores
                    for i, product in enumerate(products[:3], 1):
                        print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} (Score: {product.get('similarity_score', 0):.3f})")
                    
                    # Calculate relevance score
                    relevance_ratio = len(matching_products) / len(products) if products else 0
                    if relevance_ratio >= 0.9:
                        print("✅ EXCELLENT: 90%+ relevant products")
                    elif relevance_ratio >= 0.8:
                        print("✅ VERY GOOD: 80%+ relevant products")
                    elif relevance_ratio >= 0.6:
                        print("⚠️  GOOD: 60%+ relevant products")
                    else:
                        print("❌ POOR: Less than 60% relevant products")
                        
                    # Show relevance filtering info
                    print(f"Relevance filtering: {result.get('message', 'No message')}")
                else:
                    print("❌ No products found after filtering")
            else:
                print(f"❌ Search failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n🔍 Testing Specific Necklace Search:")
    print("-" * 40)
    
    # Test specific necklace search to see if we get only necklaces
    try:
        result = await enhanced_handler.search_products(
            query="necklace",
            user_id="test_user_targeted",
            limit=10
        )
        
        if result['status'] == 'success':
            products = result['results']
            print(f"Found {len(products)} products for 'necklace' search")
            
            # Check if products actually contain "necklace" in their names
            necklace_products = [p for p in products if 'necklace' in p.get('name', '').lower()]
            print(f"Products with 'necklace' in name: {len(necklace_products)}/{len(products)}")
            
            # Show all products
            for i, product in enumerate(products, 1):
                name = product.get('name', 'Unknown')
                category = product.get('category', 'Unknown')
                score = product.get('similarity_score', 0)
                has_necklace = 'necklace' in name.lower()
                status = "✅" if has_necklace else "❌"
                print(f"  {i}. {status} {name} - {category} (Score: {score:.3f})")
                
            if len(necklace_products) == len(products):
                print("✅ PERFECT: All products are necklaces!")
            elif len(necklace_products) >= len(products) * 0.8:
                print("✅ VERY GOOD: 80%+ products are necklaces")
            elif len(necklace_products) >= len(products) * 0.6:
                print("⚠️  GOOD: 60%+ products are necklaces")
            else:
                print("❌ NEEDS IMPROVEMENT: Less than 60% are necklaces")
                
    except Exception as e:
        print(f"❌ Error in specific necklace test: {str(e)}")
    
    print("\n📊 Summary:")
    print("=" * 50)
    print("Enhanced search functionality tested.")
    print("The enhanced handler should now provide more targeted results.")

if __name__ == "__main__":
    asyncio.run(test_enhanced_search())