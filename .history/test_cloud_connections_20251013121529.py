#!/usr/bin/env python3
"""Test cloud database connections"""

import logging
import sys
from database import MongoDBManager, QdrantManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    """Test MongoDB connection"""
    logger.info("🔄 Testing MongoDB connection...")
    try:
        db_manager = MongoDBManager()
        db_manager.connect()
        
        # Test basic operations
        db = db_manager.get_database()
        
        # List collections
        collections = db.list_collection_names()
        logger.info(f"📊 Available collections: {collections}")
        
        # Test a simple query
        if 'users' in collections:
            user_count = db.users.count_documents({})
            logger.info(f"👥 Found {user_count} users in database")
        
        logger.info("✅ MongoDB connection successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return False

def test_qdrant_connection():
    """Test Qdrant connection"""
    logger.info("🔄 Testing Qdrant connection...")
    try:
        qdrant_manager = QdrantManager()
        client = qdrant_manager.client
        
        if client is None:
            logger.error("❌ Qdrant client is None")
            return False
            
        # Test connection
        collections = client.get_collections()
        logger.info(f"📦 Available Qdrant collections: {collections.collections}")
        
        # Check if our collection exists
        collection_name = "jewellery_products"
        collection_exists = False
        for collection in collections.collections:
            if collection.name == collection_name:
                collection_exists = True
                break
                
        if collection_exists:
            # Get collection info
            collection_info = client.get_collection(collection_name)
            logger.info(f"💎 Collection '{collection_name}' found with {collection_info.points_count} points")
        else:
            logger.info(f"📋 Collection '{collection_name}' not found (this is OK if no products have been added)")
        
        logger.info("✅ Qdrant connection successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Qdrant connection failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🚀 Starting cloud database connection tests...")
    
    # Test MongoDB
    mongodb_success = test_mongodb_connection()
    
    # Test Qdrant
    qdrant_success = test_qdrant_connection()
    
    # Summary
    logger.info("\n📊 Connection Test Results:")
    logger.info(f"   MongoDB: {'✅ Connected' if mongodb_success else '❌ Failed'}")
    logger.info(f"   Qdrant:  {'✅ Connected' if qdrant_success else '❌ Failed'}")
    
    if mongodb_success and qdrant_success:
        logger.info("\n🎉 All cloud database connections successful!")
        return 0
    else:
        logger.error("\n⚠️  Some connections failed. Check logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())