#!/usr/bin/env python3
"""
Simple test to verify headphones search filtering is working.
Tests the enhanced product handler directly.
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def test_headphones_filtering():
    """Test that headphones search returns only relevant products."""
    
    print("Testing headphones search filtering...")
    
    try:
        # Initialize handlers
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)
        
        # Test headphones search
        print("\n1. Testing 'headphones' search...")
        results = await enhanced_handler.search_products_enhanced("Show me headphones")
        
        if not results:
            print("❌ No results found")
            return False
        
        print(f"Found {len(results)} products:")
        
        relevant_count = 0
        total_count = len(results)
        
        for i, product in enumerate(results):
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            
            # Check if product is headphones-related
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                relevant_count += 1
            
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Relevant: {'✅' if is_headphones else '❌'}")
        
        relevance_ratio = relevant_count / total_count
        print(f"\nRelevance Summary:")
        print(f"  Total products: {total_count}")
        print(f"  Relevant products: {relevant_count}")
        print(f"  Relevance ratio: {relevance_ratio:.1%}")
        
        # Test criteria: At least 70% of results should be headphones-related
        if relevance_ratio >= 0.7:
            print("✅ PASS: Headphones search filtering is working correctly!")
            return True
        else:
            print("❌ FAIL: Too many irrelevant products returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing headphones search: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_electronics_search():
    """Test that broad electronics search still works."""
    
    print("\n2. Testing broad electronics search...")
    
    try:
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)
        
        results = enhanced_handler.search_products_enhanced("Show me electronics")
        
        if results:
            print(f"Found {len(results)} electronics products")
            for i, product in enumerate(results[:5]):  # Show first 5
                print(f"  {i+1}. {product['name']} (${product['price']})")
            
            print("✅ PASS: Broad electronics search is working")
            return True
        else:
            print("❌ No electronics products found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing electronics search: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎧 Enhanced Product Handler - Headphones Filtering Test")
    print("=" * 60)
    
    # Test headphones search
    headphones_pass = test_headphones_filtering()
    
    # Test that we didn't break broad electronics search
    electronics_pass = test_electronics_search()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Headphones filtering: {'✅ PASS' if headphones_pass else '❌ FAIL'}")
    print(f"Electronics search: {'✅ PASS' if electronics_pass else '❌ FAIL'}")
    
    if headphones_pass and electronics_pass:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)