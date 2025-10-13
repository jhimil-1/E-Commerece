# database_local.py - Local MongoDB connection for testing
import os
from typing import Optional
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

# Local MongoDB configuration for testing
MONGODB_URL_LOCAL = "mongodb://localhost:27017/"
MONGODB_DB_NAME_LOCAL = "product_chatbot_local"

logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB connection manager"""
    
    _client = None
    _db = None
    
    @classmethod
    def connect(cls):
        """Establish MongoDB connection"""
        if cls._client is None:
            try:
                # Try local connection first
                cls._client = MongoClient(MONGODB_URL_LOCAL, serverSelectionTimeoutMS=5000)
                cls._client.admin.command('ping')
                cls._db = cls._client[MONGODB_DB_NAME_LOCAL]
                logger.info("Connected to local MongoDB successfully")
            except ConnectionFailure:
                logger.warning("Local MongoDB connection failed, trying cloud...")
                try:
                    # Fallback to cloud connection
                    from config import MONGODB_URL, MONGODB_DB_NAME
                    cls._client = MongoClient(
                        MONGODB_URL,
                        tls=True,
                        tlsAllowInvalidCertificates=True,
                        serverSelectionTimeoutMS=30000,
                        connectTimeoutMS=30000,
                        socketTimeoutMS=30000
                    )
                    cls._client.admin.command('ping')
                    cls._db = cls._client[MONGODB_DB_NAME]
                    logger.info("Connected to cloud MongoDB successfully")
                except Exception as e:
                    logger.error(f"Failed to connect to MongoDB: {e}")
                    logger.warning("MongoDB will not be available. Some features may be limited.")
                    # Don't raise, just log the error
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls._db is None:
            cls.connect()
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a specific collection from the database"""
        db = cls.get_db()
        return db[collection_name]
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")

class QdrantManager:
    """Qdrant vector database manager"""
    
    _client = None
    
    @classmethod
    def get_client(cls):
        """Get Qdrant client instance"""
        if cls._client is None:
            try:
                cls._client = QdrantClient(
                    url="http://localhost:6333",  # Local Qdrant
                    api_key=None
                )
                logger.info("Connected to local Qdrant successfully")
            except Exception as e:
                logger.warning(f"Local Qdrant failed: {e}, trying cloud...")
                try:
                    from config import QDRANT_URL, QDRANT_API_KEY
                    cls._client = QdrantClient(
                        url=QDRANT_URL,
                        api_key=QDRANT_API_KEY
                    )
                    logger.info("Connected to cloud Qdrant successfully")
                except Exception as e2:
                    logger.error(f"Failed to connect to Qdrant: {e2}")
                    logger.warning("Qdrant will not be available. Vector search features may be limited.")
                    # Return None to indicate Qdrant is not available
                    return None
        return cls._client
    
    @classmethod
    def create_collection_if_not_exists(cls, collection_name: str = None, vector_size: int = 768):
        """Create collection if it doesn't exist"""
        collection_name = collection_name or "products_local"
        client = cls.get_client()
        
        # If Qdrant is not available, skip collection creation
        if client is None:
            logger.warning("Qdrant client not available, skipping collection creation")
            return
        
        try:
            collections = client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            
            if collection_name not in collection_names:
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {collection_name}")
            else:
                logger.info(f"Using existing collection: {collection_name}")
                
        except UnexpectedResponse as e:
            logger.error(f"Error creating Qdrant collection: {e}")
            logger.warning("Qdrant collection creation failed. Vector search features may be limited.")

# Initialize database connections when module is imported
try:
    MongoDB.connect()
    qdrant_manager = QdrantManager()
    qdrant_manager.create_collection_if_not_exists()
    logger.info("Database connections initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database connections: {e}")
    logger.warning("Running without database connections - some features may be limited")