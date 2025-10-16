#!/usr/bin/env python3
"""
Simple script to clear all data from MongoDB and Qdrant databases
"""

import asyncio
import logging
from pymongo import MongoClient
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def clear_all_data():
    """Clear all data from both databases"""
    
    # MongoDB connection
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    mongo_client = MongoClient(mongo_uri)
    db_name = os.getenv("DATABASE_NAME", "jewellery_db")
    mongo_db = mongo_client[db_name]
    
    # Qdrant connection
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if qdrant_api_key:
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    else:
        qdrant_client = QdrantClient(url=qdrant_url)
    
    try:
        print("🧹 Starting database cleanup...")
        
        # Clear MongoDB collections
        print("\n📊 MongoDB Collections:")
        collections = mongo_db.list_collection_names()
        print(f"Found {len(collections)} collections: {collections}")
        
        if collections:
            for collection_name in collections:
                mongo_db.drop_collection(collection_name)
                print(f"✅ Dropped collection: {collection_name}")
        
        # Clear Qdrant collections
        print("\n🔍 Qdrant Collections:")
        qdrant_collections = qdrant_client.get_collections()
        collection_names = [col.name for col in qdrant_collections.collections]
        print(f"Found {len(collection_names)} collections: {collection_names}")
        
        if collection_names:
            for collection_name in collection_names:
                qdrant_client.delete_collection(collection_name)
                print(f"✅ Deleted Qdrant collection: {collection_name}")
        
        print("\n🎉 Database cleanup completed successfully!")
        print("✅ All data has been cleared from MongoDB and Qdrant")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
    
    finally:
        mongo_client.close()

if __name__ == "__main__":
    print("🚀 Starting complete database cleanup...")
    asyncio.run(clear_all_data())