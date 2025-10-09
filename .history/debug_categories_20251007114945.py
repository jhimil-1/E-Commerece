#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager

async def debug_categories():
    """Debug what categories are stored in Qdrant vs MongoDB"""
    
    db = MongoDB.get_db()
    
    print("=== Category Analysis ===\n")
    
    # Check categories in MongoDB
    print("1. Categories in MongoDB:")
    mongo_categories = db.products.distinct("category")
    print(f"   Found {len(mongo_categories)} unique categories:")
    for cat in sorted(mongo_categories):
        count = db.products.count_documents({"category": cat})
        print(f"   - '{cat}' ({count} products)")
    
    # Check categories in Qdrant
    print("\n2. Categories in Qdrant (sample of 10 points):")
    try:
        # Get some sample points from Qdrant
        from qdrant_client import models
        
        result = qdrant_manager.client.scroll(
            collection_name="ecommerce",
            limit=10,
            with_payload=True
        )
        
        qdrant_categories = set()
        for point in result[0]:
            category = point.payload.get("category", "NO_CATEGORY")
            qdrant_categories.add(category)
            print(f"   - '{category}' (from product: {point.payload.get('name', 'Unknown')})")
            
        print(f"\n   Found {len(qdrant_categories)} unique categories in Qdrant sample")
        
    except Exception as e:
        print(f"   Error accessing Qdrant: {e}")
    
    # Test category case sensitivity
    print("\n3. Testing category case sensitivity:")
    test_categories = ["necklaces", "Necklaces", "NECKLACES"]
    
    for test_cat in test_categories:
        try:
            count = db.products.count_documents({"category": test_cat})
            print(f"   '{test_cat}': {count} products in MongoDB")
        except Exception as e:
            print(f"   '{test_cat}': Error - {e}")

if __name__ == "__main__":
    asyncio.run(debug_categories())