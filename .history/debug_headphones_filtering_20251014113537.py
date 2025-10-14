#!/usr/bin/env python3
"""
Detailed debug test to understand headphones filtering issues.
"""

import sys
import os
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def debug_headphones_filtering():
    """Debug the headphones filtering process step by step."""
    
    print("🔍 DEBUGGING HEADPHONES FILTERING")
    print("=" * 60)
    
    try:
        # Initialize handlers
        product_handler = ProductHandler()
        enhanced_handler = EnhancedProductHandler(product_handler)
        
        # Step 1: Get raw search results without filtering
        print("\n1️⃣ Getting raw search results...")
        raw_result = await product_handler.search_products(
            query="Show me headphones",
            user_id=None,
            category=None,
            limit=50
        )
        
        if raw_result['status'] != 'success':
            print(f"❌ Raw search failed: {raw_result}")
            return False
        
        raw_products = raw_result.get('results', [])
        print(f"Found {len(raw_products)} raw products")
        
        # Analyze raw results
        print("\n📋 Raw Products Analysis:")
        headphones_in_raw = 0
        for i, product in enumerate(raw_products[:10]):  # Show first 10
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            score = product.get('similarity_score', 0)
            
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                headphones_in_raw += 1
            
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Category: {product.get('category', 'unknown')}, Score: {score:.3f}")
            print(f"     Headphones: {'✅' if is_headphones else '❌'}")
        
        print(f"\nRaw results: {headphones_in_raw}/{len(raw_products)} are headphones-related")
        
        # Step 2: Test semantic relevance calculation
        print("\n2️⃣ Testing semantic relevance calculation...")
        test_products = [
            {
                'name': 'Wireless Earbuds Pro',
                'description': 'True wireless earbuds with active noise cancellation and 30-hour battery.',
                'category': 'Electronics',
                'price': '179.99'
            },
            {
                'name': 'Smartphone X1',
                'description': 'Latest smartphone with advanced camera and 5G connectivity.',
                'category': 'Electronics', 
                'price': '899.99'
            },
            {
                'name': 'Noise Cancelling Headphones',
                'description': 'Premium over-ear headphones with active noise cancellation.',
                'category': 'Electronics',
                'price': '299.99'
            }
        ]
        
        query = "Show me headphones"
        print(f"\nTesting semantic relevance for query: '{query}'")
        for product in test_products:
            relevance = enhanced_handler.calculate_semantic_relevance(query, product)
            print(f"  {product['name']}: {relevance:.3f}")
        
        # Step 3: Test filtering with known products
        print("\n3️⃣ Testing filtering logic with known products...")
        filtered_results = enhanced_handler.filter_irrelevant_results(
            query="Show me headphones", 
            products=test_products, 
            min_semantic_score=None
        )
        
        print(f"Filtered from {len(test_products)} to {len(filtered_results)} products")
        for product in filtered_results:
            print(f"  ✅ {product['name']} (enhanced_score: {product.get('enhanced_score', 0):.3f})")
        
        # Step 4: Apply filtering to real results
        print("\n4️⃣ Applying filtering to real search results...")
        filtered_result = enhanced_handler.filter_irrelevant_results(
            query="Show me headphones",
            products=raw_products,
            min_semantic_score=None
        )
        
        print(f"Filtered from {len(raw_products)} to {len(filtered_result)} products")
        
        # Analyze filtered results
        print("\n📊 Filtered Products Analysis:")
        headphones_in_filtered = 0
        for i, product in enumerate(filtered_result):
            name = product.get('name', '').lower()
            description = product.get('description', '').lower()
            semantic_score = product.get('semantic_relevance', 0)
            vector_score = product.get('similarity_score', 0)
            enhanced_score = product.get('enhanced_score', 0)
            
            headphones_keywords = ['headphones', 'headphone', 'earbuds', 'earphone']
            is_headphones = any(keyword in name or keyword in description for keyword in headphones_keywords)
            
            if is_headphones:
                headphones_in_filtered += 1
            
            print(f"  {i+1}. {product['name']} (${product['price']})")
            print(f"     Category: {product.get('category', 'unknown')}")
            print(f"     Scores: semantic={semantic_score:.3f}, vector={vector_score:.3f}, enhanced={enhanced_score:.3f}")
            print(f"     Headphones: {'✅' if is_headphones else '❌'}")
        
        # Final analysis
        print(f"\n📈 FINAL ANALYSIS:")
        print(f"   Raw results: {len(raw_products)} products, {headphones_in_raw} headphones-related")
        print(f"   Filtered results: {len(filtered_result)} products, {headphones_in_filtered} headphones-related")
        
        if len(raw_products) > 0:
            raw_ratio = headphones_in_raw / len(raw_products)
            filtered_ratio = headphones_in_filtered / len(filtered_result) if len(filtered_result) > 0 else 0
            
            print(f"   Raw relevance ratio: {raw_ratio:.1%}")
            print(f"   Filtered relevance ratio: {filtered_ratio:.1%}")
            print(f"   Filtering improvement: {filtered_ratio - raw_ratio:.1%}")
        
        # Success if filtering improved relevance
        success = len(filtered_result) > 0 and (filtered_ratio > raw_ratio or filtered_ratio >= 0.7)
        
        if success:
            print("✅ SUCCESS: Filtering is working and improving relevance!")
        else:
            print("❌ ISSUE: Filtering needs adjustment")
            
        return success
            
    except Exception as e:
        print(f"❌ Error in debug test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(debug_headphones_filtering())
    sys.exit(0 if result else 1)