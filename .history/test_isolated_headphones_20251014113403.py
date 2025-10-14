#!/usr/bin/env python3
"""
Isolated test to verify headphones search filtering works correctly.
This test completely isolates the enhanced product handler testing.
"""

import sys
import os
import asyncio
import logging

# Set up logging to see debug messages
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def test_isolated_headphones():
    """Test headphones search in complete isolation."""
    
    print("🎧 ISOLATED HEADPHONES TEST")
    print("=" * 50)
    
    try:
        # Initialize handlers fresh
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)
        
        # Test 1: Headphones query
        print("\n1. Testing 'Show me headphones' query...")
        headphones_query = "Show me headphones"
        print(f"DEBUG: Sending query: '{headphones_query}'")
        
        result = await enhanced_handler.search_products_enhanced(headphones_query)
        
        if not result or result.get('status') != 'success':
            print(f"❌ Search failed: {result}")
            return False
        
        products = result.get('results', [])
        print(f"DEBUG: Found {len(products)} products")
        
        # Analyze results
        headphones_count = 0
        for i, product in enumerate(products):
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            semantic_score = product.get('semantic_relevance', 0)
            vector_score = product.get('similarity_score', 0)
            
            # Check if headphones-related
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                headphones_count += 1
            
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Category: {product.get('category', 'unknown')}")
            print(f"     Relevant: {'✅' if is_headphones else '❌'}")
            print(f"     Scores: semantic={semantic_score:.3f}, vector={vector_score:.3f}")
        
        relevance_ratio = headphones_count / len(products) if products else 0
        print(f"\n📊 Results Summary:")
        print(f"   Total products: {len(products)}")
        print(f"   Headphones products: {headphones_count}")
        print(f"   Relevance ratio: {relevance_ratio:.1%}")
        
        # Test 2: Wait a moment and test electronics separately
        print("\n2. Testing 'Show me electronics' query...")
        electronics_query = "Show me electronics"
        print(f"DEBUG: Sending query: '{electronics_query}'")
        
        result2 = await enhanced_handler.search_products_enhanced(electronics_query)
        
        if not result2 or result2.get('status') != 'success':
            print(f"❌ Electronics search failed: {result2}")
            return False
        
        electronics_products = result2.get('results', [])
        print(f"DEBUG: Found {len(electronics_products)} electronics products")
        
        # Show first few electronics products
        for i, product in enumerate(electronics_products[:3]):
            print(f"  {i+1}. {product['name']} (${product['price']})")
        
        # Test 3: Test headphones again to ensure consistency
        print("\n3. Testing 'Show me headphones' query again...")
        headphones_query2 = "Show me headphones"
        print(f"DEBUG: Sending query: '{headphones_query2}'")
        
        result3 = await enhanced_handler.search_products_enhanced(headphones_query2)
        
        if not result3 or result3.get('status') != 'success':
            print(f"❌ Second headphones search failed: {result3}")
            return False
        
        products3 = result3.get('results', [])
        print(f"DEBUG: Found {len(products3)} products in second test")
        
        # Analyze second headphones test
        headphones_count2 = 0
        for product in products3:
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                headphones_count2 += 1
        
        relevance_ratio2 = headphones_count2 / len(products3) if products3 else 0
        print(f"   Second test relevance ratio: {relevance_ratio2:.1%}")
        
        # Final evaluation
        print(f"\n📈 FINAL EVALUATION:")
        print(f"   First headphones test: {relevance_ratio:.1%} relevant")
        print(f"   Second headphones test: {relevance_ratio2:.1%} relevant")
        print(f"   Electronics test: {len(electronics_products)} products found")
        
        # Success criteria: both headphones tests should have high relevance
        success = (relevance_ratio >= 0.7 and relevance_ratio2 >= 0.7 and 
                  len(products) > 0 and len(products3) > 0)
        
        if success:
            print("✅ SUCCESS: Headphones filtering is working correctly!")
            return True
        else:
            print("❌ FAILURE: Headphones filtering needs improvement")
            return False
            
    except Exception as e:
        print(f"❌ Error in isolated test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_isolated_headphones())
    sys.exit(0 if result else 1)