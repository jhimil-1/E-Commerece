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
        result = await enhanced_handler.search_products_enhanced("Show me headphones")
        
        if not result or result.get('status') != 'success':
            print(f"❌ Search failed: {result}")
            return False
        
        products = result.get('results', [])
        
        if not products:
            print("❌ No products found")
            return False
        
        print(f"Found {len(products)} products:")
            
        # Show what should have been filtered
        print("\nDebugging info:")
        print(f"Expected: semantic >= 0.8, vector >= 0.7")
        for product in products:
            semantic_score = product.get('semantic_relevance', 0)
            vector_score = product.get('similarity_score', 0)
            should_pass = semantic_score >= 0.8 and vector_score >= 0.7
            print(f"  {product['name']}: semantic={semantic_score:.3f}, vector={vector_score:.3f}, pass={should_pass}")
        
        relevant_count = 0
        total_count = len(products)
        
        for i, product in enumerate(products):
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            
            # Check if product is headphones-related
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                relevant_count += 1
            
            semantic_score = product.get('semantic_relevance', 0)
            vector_score = product.get('similarity_score', 0)
            enhanced_score = product.get('enhanced_score', 0)
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Relevant: {'✅' if is_headphones else '❌'} - semantic: {semantic_score:.3f}, vector: {vector_score:.3f}, enhanced: {enhanced_score:.3f}")
        
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

async def test_electronics_search():
    """Test that broad electronics search still works."""
    
    print("\n2. Testing broad electronics search...")
    
    try:
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)

        result = await enhanced_handler.search_products_enhanced("Show me electronics")

        if not result or result.get('status') != 'success':
            print(f"❌ Search failed: {result}")
            return False

        products = result.get('results', [])

        if not products:
            print("❌ No products found")
            return False

        print(f"Found {len(products)} electronics products")
        for i, product in enumerate(products[:5]):  # Show first 5
            print(f"  {i+1}. {product['name']} (${product['price']})")

        print("✅ PASS: Broad electronics search is working")
        return True
            
    except Exception as e:
        print(f"❌ Error testing electronics search: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🎧 Enhanced Product Handler - Headphones Filtering Test")
    print("=" * 60)
    
    # Test headphones search
    headphones_pass = await test_headphones_filtering()
    
    # Test that we didn't break broad electronics search
    electronics_pass = await test_electronics_search()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Headphones filtering: {'✅ PASS' if headphones_pass else '❌ FAIL'}")
    print(f"Electronics search: {'✅ PASS' if electronics_pass else '❌ FAIL'}")
    
    if headphones_pass and electronics_pass:
        print("\n🎉 All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)