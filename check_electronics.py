#!/usr/bin/env python3
"""Check what electronics products are available"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler

async def check_electronics():
    handler = ProductHandler()
    
    print("=== CHECKING ELECTRONICS PRODUCTS ===\n")
    
    # Test different electronics searches
    queries = ["electronics", "smartphone", "phone", "camera"]
    
    for query in queries:
        print(f"Query: '{query}'")
        print("-" * 50)
        
        try:
            results = await handler.search_products(query, category='electronics', limit=10)
            
            print(f"Total results: {results.get('count', 0)}")
            
            if results.get('results'):
                for i, product in enumerate(results['results'], 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    score = product.get('similarity_score', 0)
                    desc = product.get('description', 'No description')
                    print(f"  {i}. {name} ({category}) - Score: {score:.3f}")
                    print(f"     Description: {desc}")
            else:
                print("  No products found")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
        
        print()

if __name__ == "__main__":
    asyncio.run(check_electronics())