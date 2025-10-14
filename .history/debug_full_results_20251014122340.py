#!/usr/bin/env python3
"""
Debug test to see exactly what products are being returned
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def debug_full_results():
    """Show all products returned for headphones query"""
    
    # Initialize handlers fresh
    product_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    # Test headphones query
    print("🔍 Testing 'Show me headphones' query...")
    result = await enhanced_handler.search_products_enhanced("Show me headphones")
    
    if not result or result.get('status') != 'success':
        print(f"❌ Search failed: {result}")
        return
    
    products = result.get('results', [])
    print(f"📊 Found {len(products)} products total")
    print(f"🎯 Original count: {result.get('metadata', {}).get('original_count', 'N/A')}")
    print(f"🎯 Filtered count: {result.get('metadata', {}).get('filtered_count', 'N/A')}")
    
    print("\n📋 ALL PRODUCTS RETURNED:")
    print("=" * 80)
    
    headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
    headphones_count = 0
    
    for i, product in enumerate(products):
        name = product.get('name', '')
        description = product.get('description', '')
        category = product.get('category', 'unknown')
        semantic_score = product.get('semantic_relevance', 0)
        vector_score = product.get('similarity_score', 0)
        enhanced_score = product.get('enhanced_score', 0)
        
        # Check if headphones-related
        name_lower = name.lower()
        desc_lower = description.lower()
        is_headphones = any(keyword in name_lower or keyword in desc_lower for keyword in headphones_keywords)
        
        if is_headphones:
            headphones_count += 1
        
        print(f"\n{i+1}. {name}")
        print(f"   💰 Price: ${product.get('price', 'N/A')}")
        print(f"   🏷️  Category: {category}")
        print(f"   📖 Description: {description[:100]}...")
        print(f"   🎯 Relevant: {'✅ YES' if is_headphones else '❌ NO'}")
        print(f"   📊 Scores: semantic={semantic_score:.3f}, vector={vector_score:.3f}, enhanced={enhanced_score:.3f}")
    
    print(f"\n📈 SUMMARY:")
    print(f"   Total products: {len(products)}")
    print(f"   Headphones products: {headphones_count}")
    print(f"   Relevance ratio: {headphones_count/len(products):.1%}")
    
    # Show what the original search returned before filtering
    print(f"\n🔍 BEFORE FILTERING (from metadata):")
    print(f"   Original count: {result.get('metadata', {}).get('original_count', 'N/A')}")
    print(f"   Filtered count: {result.get('metadata', {}).get('filtered_count', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(debug_full_results())