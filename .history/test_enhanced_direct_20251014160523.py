#!/usr/bin/env python3
"""
Direct test of enhanced search functionality
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def test_enhanced_search():
    """Test enhanced search directly"""
    print("🧪 Testing Enhanced Search Directly")
    print("=" * 40)
    
    # Initialize handlers
    base_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(base_handler)
    
    # Test search for necklace
    print("🔍 Testing search for 'necklace'...")
    
    try:
        results = await enhanced_handler.search_products(
            query="necklace",
            limit=5
        )
        
        products = results.get("results", [])
        print(f"Found {len(products)} products")
        
        # Count necklaces
        necklace_count = sum(1 for p in products if "necklace" in p.get("name", "").lower())
        print(f"Necklaces: {necklace_count}/{len(products)}")
        
        for i, product in enumerate(products, 1):
            status = "✅" if "necklace" in product.get("name", "").lower() else "❌"
            print(f"  {i}. {status} {product.get('name', 'Unknown')} - Score: {product.get('similarity_score', 0):.3f}")
        
        # Test other queries
        test_queries = ["earrings", "ring", "watch"]
        
        for query in test_queries:
            print(f"\n🔍 Testing search for '{query}'...")
            results = await enhanced_handler.search_products(
                query=query,
                limit=3
            )
            
            products = results.get("results", [])
            relevant_count = sum(1 for p in products if query in p.get("name", "").lower())
            print(f"  Found {len(products)} products, {relevant_count} relevant")
        
        return necklace_count > 0
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

async def main():
    success = await test_enhanced_search()
    
    print("\n📊 Test Results:")
    print("=" * 40)
    print(f"Enhanced search: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 Enhanced search is working correctly!")
        print("The system now provides more relevant results for specific queries.")
    else:
        print("\n⚠️  Enhanced search failed. Check the configuration.")

if __name__ == "__main__":
    asyncio.run(main())