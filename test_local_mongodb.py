#!/usr/bin/env python3
"""
Test script for local MongoDB connection
"""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_local_mongodb():
    """Test connection to local MongoDB"""
    try:
        logger.info("🔄 Testing local MongoDB connection...")
        
        # Test basic connection
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        logger.info("✅ Local MongoDB connection successful!")
        
        # Get server info
        server_info = client.server_info()
        logger.info(f"📊 MongoDB version: {server_info.get('version', 'Unknown')}")
        
        # List databases
        databases = client.list_database_names()
        logger.info(f"📁 Available databases: {databases}")
        
        client.close()
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ Local MongoDB connection failed: {e}")
        logger.error("💡 Please ensure MongoDB is installed and running:")
        logger.error("   - Install MongoDB Community Edition")
        logger.error("   - Start MongoDB service: 'net start MongoDB' (Windows)")
        logger.error("   - Or run: 'mongod' in a terminal")
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def test_local_qdrant():
    """Test connection to local Qdrant"""
    try:
        logger.info("🔄 Testing local Qdrant connection...")
        from qdrant_client import QdrantClient
        
        client = QdrantClient(url="http://localhost:6333")
        collections = client.get_collections()
        
        logger.info("✅ Local Qdrant connection successful!")
        logger.info(f"📊 Collections: {len(collections.collections)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Local Qdrant connection failed: {e}")
        logger.error("💡 Please ensure Qdrant is installed and running:")
        logger.error("   - Install Qdrant: 'pip install qdrant-client'")
        logger.error("   - Start Qdrant: 'docker run -p 6333:6333 qdrant/qdrant'")
        logger.error("   - Or download and run Qdrant locally")
        return False

if __name__ == "__main__":
    logger.info("🚀 Testing Local Database Connections")
    logger.info("=" * 50)
    
    # Test MongoDB
    mongodb_success = test_local_mongodb()
    
    # Test Qdrant
    qdrant_success = test_local_qdrant()
    
    logger.info("\n📊 SUMMARY:")
    logger.info(f"Local MongoDB: {'✅ WORKING' if mongodb_success else '❌ FAILED'}")
    logger.info(f"Local Qdrant: {'✅ WORKING' if qdrant_success else '❌ FAILED'}")
    
    if mongodb_success and qdrant_success:
        logger.info("\n🎉 All local databases are working! You can start your application.")
    else:
        logger.info("\n⚠️  Some databases are not available. Please install/start the missing services.")
        logger.info("The application will still work but with limited features.")