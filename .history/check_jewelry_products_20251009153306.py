#!/usr/bin/env python3
"""
Script to check jewelry products in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_utils import QdrantManager
from clip_utils import clip_manager

def main():
    # Initialize managers
    qdrant_manager = QdrantManager()
    
    # Generate embedding for jewelry query
    query_embedding = clip_manager.get_text_embedding('gold diamond jewelry ring necklace bracelet')
    
    print("🔍 Searching for jewelry products...")
    
    # Search for similar products
    results = qdrant_manager.search_similar_products(
        query_embedding=query_embedding,
        limit=10,
        min_score=0.1
    )
    
    if not results:
        print("❌ No products found in database")
        return
    
    print(f"\n✅ Found {len(results)} products:\n")
    
    # Display results
    jewelry_count = 0
    for i, product in enumerate(results, 1):
        name = product.get('name', 'Unknown')
        price = product.get('price', 'N/A')
        category = product.get('category', 'Unknown')
        description = product.get('description', 'No description')
        image_url = product.get('image_url', '')
        score = product.get('score', 0)
        
        # Check if it's a jewelry product
        jewelry_categories = ['Rings', 'Necklaces', 'Bracelets', 'Earrings', 'Jewelry']
        is_jewelry = category in jewelry_categories or any(keyword in name.lower() for keyword in ['gold', 'diamond', 'silver', 'pearl', 'emerald'])
        
        if is_jewelry:
            jewelry_count += 1
            print(f"💎 JEWELRY PRODUCT {jewelry_count}:")
        else:
            print(f"📦 Product {i}:")
            
        print(f"   Name: {name}")
        print(f"   Price: ${price}")
        print(f"   Category: {category}")
        print(f"   Description: {description}")
        print(f"   Image: {image_url}")
        print(f"   Similarity Score: {score:.1%}")
        print()
    
    print(f"📊 Summary: Found {jewelry_count} jewelry products out of {len(results)} total products")

if __name__ == "__main__":
    main()