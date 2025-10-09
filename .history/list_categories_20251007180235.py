#!/usr/bin/env python3
"""List all unique categories in the Qdrant database."""

import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

def main():
    # Initialize Qdrant client
    client = QdrantClient(
        url="https://fbaa9def-f06b-4625-82dd-546493e5c559.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="your-api-key-here"  # Replace with your actual API key
    )
    
    collection_name = "eccomerce"
    
    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection: {collection_name}")
        print(f"Points count: {collection_info.points_count}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print("\n" + "="*50 + "\n")
        
        # Scroll through all points to extract categories
        categories = set()
        offset = None
        
        while True:
            # Scroll through points
            scroll_result = client.scroll(
                collection_name=collection_name,
                limit=1000,
                offset=offset,
                with_payload=["category"]
            )
            
            points, next_offset = scroll_result
            
            # Extract categories from current batch
            for point in points:
                if point.payload and 'category' in point.payload:
                    categories.add(point.payload['category'])
            
            # Check if we've reached the end
            if next_offset is None:
                break
                
            offset = next_offset
            
            print(f"Processed {len(categories)} unique categories so far...")
        
        print(f"\nTotal unique categories found: {len(categories)}")
        print("\nCategories:")
        for category in sorted(categories):
            print(f"  - {category}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()