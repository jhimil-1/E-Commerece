#!/usr/bin/env python3
"""
Test script to compare original vs enhanced search results
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler
from enhanced_product_handler import EnhancedProductHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def compare_search_results():
    """Compare original vs enhanced search results"""
    
    # Initialize handlers
    original_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(original_handler)
    
    # Test queries that were problematic
    test_queries = [
        "pant",
        "pants", 
        "business professional dress",
        "dress",
        "shirt"
    ]
    
    print("=== SEARCH ALGORITHM COMPARISON ===\n")
    
    for query in test_queries:
        print(f"Testing query: '{query}'")
        print("=" * 60)
        
        try:
            # Original search
            print("ORIGINAL SEARCH:")
            print("-" * 30)
            original_result = await original_handler.search_products(
                query=query,
                user_id=None,
                category=None,
                limit=5
            )
            
            if original_result['status'] == 'success':
                original_products = original_result['results']
                print(f"Found {len(original_products)} products")
                
                for i, product in enumerate(original_products, 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    score = product.get('similarity_score', 0)
                    match_pct = product.get('match_percentage', 0)
                    print(f"  {i}. {name} ({category}) - Score: {score:.3f} ({match_pct}%)")
                    
                # Calculate relevance score
                relevant_count = count_relevant_results(query, original_products)
                print(f"Relevance: {relevant_count}/{len(original_products)} relevant")
            else:
                print(f"Search failed: {original_result['message']}")
            
            print("\nENHANCED SEARCH:")
            print("-" * 30)
            enhanced_result = await enhanced_handler.search_products_enhanced(
                query=query,
                user_id=None,
                category=None,
                limit=5
            )
            
            if enhanced_result['status'] == 'success':
                enhanced_products = enhanced_result['results']
                print(f"Found {len(enhanced_products)} products")
                
                for i, product in enumerate(enhanced_products, 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    score = product.get('similarity_score', 0)
                    enhanced_score = product.get('enhanced_score', 0)
                    semantic_score = product.get('semantic_relevance', 0)
                    print(f"  {i}. {name} ({category}) - Vector: {score:.3f}, "
                          f"Semantic: {semantic_score:.3f}, Combined: {enhanced_score:.3f}")
                    
                # Calculate relevance score
                relevant_count = count_relevant_results(query, enhanced_products)
                print(f"Relevance: {relevant_count}/{len(enhanced_products)} relevant")
                print(f"Filtering: {enhanced_result['metadata']['original_count']} -> "
                      f"{enhanced_result['metadata']['filtered_count']} products")
            else:
                print(f"Search failed: {enhanced_result['message']}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*60 + "\n")

def count_relevant_results(query: str, products: list) -> int:
    """Count how many products are relevant to the query"""
    query_lower = query.lower()
    relevant_count = 0
    
    for product in products:
        name_lower = product.get('name', '').lower()
        category_lower = product.get('category', '').lower()
        desc_lower = product.get('description', '').lower()
        
        # Simple relevance check
        if (query_lower in name_lower or 
            query_lower in category_lower or
            any(word in name_lower for word in query_lower.split()) or
            any(word in desc_lower for word in query_lower.split())):
            relevant_count += 1
    
    return relevant_count

if __name__ == "__main__":
    print("Starting search algorithm comparison...")
    asyncio.run(compare_search_results())
    print("Comparison complete!")