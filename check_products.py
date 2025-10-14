#!/usr/bin/env python3
"""
Script to check what products are stored in MongoDB and Qdrant
"""

from database import MongoDB
from qdrant_utils import qdrant_manager

def check_products():
    """Check products in both databases"""
    
    # Connect to MongoDB
    print("=== CONNECTING TO MONGODB ===")
    mongo = MongoDB()
    mongo.connect()
    
    # Check products in MongoDB
    print("\n=== MONGODB PRODUCTS ===")
    products_collection = mongo.get_collection("products")
    products = list(products_collection.find().limit(20))
    
    if not products:
        print("No products found in MongoDB!")
    else:
        for i, product in enumerate(products):
            print(f"\nProduct {i+1}:")
            print(f"  ID: {product['_id']}")
            print(f"  Name: {product.get('name', 'N/A')}")
            print(f"  Category: {product.get('category', 'N/A')}")
            print(f"  Price: {product.get('price', 'N/A')}")
            print(f"  Description: {product.get('description', 'N/A')[:100]}...")
            print(f"  Image URL: {product.get('image_url', 'N/A')}")
            print(f"  Created by: {product.get('created_by', 'N/A')}")
    
    # Check products in Qdrant
    print(f"\n=== QDRANT COLLECTION ===")
    try:
        collection_info = qdrant_manager.client.get_collection(qdrant_manager.collection_name)
        print(f"Collection name: {qdrant_manager.collection_name}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Points count: {collection_info.points_count}")
        
        # Sample some Qdrant points
        print(f"\n=== QDRANT SAMPLE PRODUCTS ===")
        sample_results = qdrant_manager.client.scroll(
            collection_name=qdrant_manager.collection_name,
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        
        if not sample_results[0]:
            print("No products found in Qdrant!")
        else:
            for i, point in enumerate(sample_results[0]):
                print(f"\nQdrant Point {i+1}:")
                print(f"  ID: {point.id}")
                print(f"  Payload: {point.payload}")
                
        # Check total count
        total_count = qdrant_manager.client.count(qdrant_manager.collection_name)
        print(f"\nTotal Qdrant points: {total_count.count}")
        
    except Exception as e:
        print(f"Error accessing Qdrant: {e}")

if __name__ == "__main__":
    check_products()