#!/usr/bin/env python3
"""
Check what's actually stored in Qdrant for product descriptions
"""

import requests
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "eccomerce")

def check_qdrant_descriptions():
    """Check what descriptions are stored in Qdrant"""
    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        
        collection_name = QDRANT_COLLECTION_NAME
        
        # Get some sample points
        print("🔍 Checking Qdrant payload structure:")
        points = client.scroll(
            collection_name=collection_name,
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        
        for i, point in enumerate(points[0]):
            print(f"\n--- Point {i+1} ---")
            print(f"ID: {point.id}")
            print(f"Payload keys: {list(point.payload.keys())}")
            
            # Check for description in payload
            if 'description' in point.payload:
                print(f"✅ Description found: {repr(point.payload['description'])}")
            else:
                print("❌ No 'description' field in payload")
                
            # Check for other fields
            for key in ['name', 'category', 'price', 'image_url', 'image_path', 'image']:
                if key in point.payload:
                    print(f"  - {key}: {repr(point.payload[key])}")
                else:
                    print(f"  - {key}: MISSING")
                    
            # Check if there are any other description-like fields
            desc_like_fields = [k for k in point.payload.keys() if 'desc' in k.lower() or 'detail' in k.lower()]
            if desc_like_fields:
                print(f"  - Description-like fields: {desc_like_fields}")
            
            print()
            
    except Exception as e:
        print(f"❌ Error checking Qdrant: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_qdrant_descriptions()