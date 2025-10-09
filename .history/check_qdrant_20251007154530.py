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

def check_qdrant_collection():
    """Check what's in the Qdrant collection"""
    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        
        collection_name = "eccomerce"
        
        # Check collection info
        collection_info = client.get_collection(collection_name)
        print(f"📊 Collection: {collection_name}")
        print(f"🎯 Points count: {collection_info.points_count}")
        print(f"🎯 Vectors count: {collection_info.vectors_count}")
        print(f"📏 Vector size: {collection_info.config.params.vectors.size}")
        print()
        
        if collection_info.points_count == 0:
            print("❌ No points found in Qdrant collection!")
            return
        
        # Get some sample points
        print("🔍 Sample points from Qdrant:")
        points = client.scroll(
            collection_name=collection_name,
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        
        for i, point in enumerate(points[0]):
            print(f"{i+1}. ID: {point.id}")
            print(f"   Payload: {point.payload}")
            print()
        
        # Try a simple search
        print("🔍 Testing simple search:")
        test_embedding = [0.1] * 512  # Simple test embedding
        search_results = client.search(
            collection_name=collection_name,
            query_vector=test_embedding,
            limit=5
        )
        
        print(f"Search returned {len(search_results)} results")
        for i, result in enumerate(search_results):
            print(f"{i+1}. ID: {result.id}, Score: {result.score}")
            print(f"   Payload: {result.payload}")
            print()
            
    except Exception as e:
        print(f"❌ Error checking Qdrant: {str(e)}")

if __name__ == "__main__":
    check_qdrant_collection()