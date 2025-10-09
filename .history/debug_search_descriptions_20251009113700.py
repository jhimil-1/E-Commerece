#!/usr/bin/env python3
"""
Debug the search process to understand why descriptions aren't being retrieved
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler
from database import MongoDB

def test_search_with_descriptions():
    """Test search to see what's happening with descriptions"""
    
    print("🧪 Testing search with detailed debugging...")
    
    # Initialize product handler
    handler = ProductHandler()
    
    # Test search
    query = "laptop"
    
    print(f"🔍 Searching for: {query}")
    
    # Run the search
    result = asyncio.run(handler.search_products(
        query=query,
        user_id="68da75b494c9b5dbe3bb5790",  # Use existing user ID
        limit=3
    ))
    
    print(f"\n📊 Search result status: {result.get('status')}")
    print(f"📊 Result count: {result.get('count')}")
    
    if result.get('results'):
        print(f"\n🔍 Detailed analysis of first result:")
        product = result['results'][0]
        
        print(f"Name: {product['name']}")
        print(f"Description: {repr(product['description'])}")
        print(f"Description length: {len(product['description'])}")
        print(f"Image URL: {repr(product['image_url'])}")
        print(f"Similarity Score: {product['similarity_score']}")
        
        # Now let's manually check MongoDB for this product
        print(f"\n🔍 Manual MongoDB check for product ID: {product['id']}")
        db = MongoDB.get_db()
        
        try:
            from bson import ObjectId
            mongo_product = db.products.find_one({"_id": ObjectId(product['id'])})
            if mongo_product:
                print(f"MongoDB Product Name: {mongo_product.get('name')}")
                print(f"MongoDB Product Description: {repr(mongo_product.get('description', 'MISSING'))}")
                print(f"MongoDB Product Image URL: {repr(mongo_product.get('image_url', 'MISSING'))}")
            else:
                print("❌ Product not found in MongoDB")
        except Exception as e:
            print(f"❌ Error checking MongoDB: {e}")
    else:
        print("❌ No results found")

if __name__ == "__main__":
    test_search_with_descriptions()