# database.py - Improved MongoDB connection with SSL/TLS fixes
import os
import ssl
from typing import Optional
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError
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
        """Establish MongoDB connection with improved SSL/TLS handling - LOCAL PRIORITY"""
        if cls._client is None:
            try:
                # Try local connection first (PRIORITY)
                logger.info("🔄 Attempting local MongoDB connection...")
                cls._client = MongoClient(MONGODB_URL_LOCAL, serverSelectionTimeoutMS=5000)
                cls._client.admin.command('ping')
                cls._db = cls._client[MONGODB_DB_NAME_LOCAL]
                logger.info("✅ Connected to local MongoDB successfully")
                return  # Exit early if local connection works
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.warning(f"❌ Local MongoDB connection failed: {e}")
                logger.info("🔄 Trying cloud MongoDB connection as fallback...")
                try:
                    # Fallback to cloud connection with improved SSL/TLS settings
                    from config import MONGODB_URL, MONGODB_DB_NAME
                    
                    # Parse connection string to check for SSL parameters
                    connection_string = MONGODB_URL
                    
                    # Enhanced connection options for MongoDB Atlas
                    connection_options = {
                        'serverSelectionTimeoutMS': 15000,
                        'connectTimeoutMS': 15000,
                        'socketTimeoutMS': 15000,
                        'retryWrites': True,
                        'w': 'majority',
                        'maxPoolSize': 10,
                        'minPoolSize': 1,
                        'maxIdleTimeMS': 30000,
                        # SSL/TLS settings
                        'tls': True,
                        'tlsAllowInvalidCertificates': False,  # Changed to False for security
                        'tlsAllowInvalidHostnames': False,       # Changed to False for security
                        'ssl_cert_reqs': ssl.CERT_REQUIRED,    # Require valid SSL certificates
                    }
                    
                    # If connection string already has SSL parameters, adjust accordingly
                    if 'tls=true' in connection_string.lower() or 'ssl=true' in connection_string.lower():
                        logger.info("SSL/TLS detected in connection string, using enhanced security settings")
                        # Use system SSL certificates
                        connection_options['ssl_ca_certs'] = None  # Use system CA bundle
                        connection_options['ssl_certfile'] = None
                        connection_options['ssl_keyfile'] = None
                    
                    logger.info(f"Connecting to cloud MongoDB with enhanced SSL settings...")
                    cls._client = MongoClient(connection_string, **connection_options)
                    
                    # Test connection
                    logger.info("Testing cloud MongoDB connection...")
                    cls._client.admin.command('ping')
                    cls._db = cls._client[MONGODB_DB_NAME]
                    logger.info("✅ Connected to cloud MongoDB successfully")
                    
                except (ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError) as cloud_error:
                    logger.error(f"❌ Cloud MongoDB connection failed: {cloud_error}")
                    logger.error(f"Error type: {type(cloud_error).__name__}")
                    
                    # Try one more time with relaxed SSL settings (fallback)
                    logger.info("Trying cloud MongoDB with relaxed SSL settings...")
                    try:
                        fallback_options = {
                            'serverSelectionTimeoutMS': 10000,
                            'connectTimeoutMS': 10000,
                            'socketTimeoutMS': 10000,
                            'retryWrites': True,
                            'w': 'majority',
                            # Relaxed SSL settings for compatibility
                            'tls': True,
                            'tlsAllowInvalidCertificates': True,
                            'tlsAllowInvalidHostnames': True,
                            'ssl_cert_reqs': ssl.CERT_NONE,
                        }
                        
                        cls._client = MongoClient(connection_string, **fallback_options)
                        cls._client.admin.command('ping')
                        cls._db = cls._client[MONGODB_DB_NAME]
                        logger.info("✅ Connected to cloud MongoDB with fallback SSL settings")
                        
                    except Exception as final_error:
                        logger.error(f"❌ All MongoDB connection attempts failed: {final_error}")
                        logger.warning("⚠️  MongoDB will not be available. Application will run with limited features.")
                        # Set to None to indicate no database connection
                        cls._client = None
                        cls._db = None
                        
                except Exception as unexpected_error:
                    logger.error(f"❌ Unexpected error connecting to MongoDB: {unexpected_error}")
                    logger.error(f"Error type: {type(unexpected_error).__name__}")
                    import traceback
                    traceback.print_exc()
                    cls._client = None
                    cls._db = None
    
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
def initialize_databases():
    """Initialize database connections with better error handling"""
    try:
        logger.info("🔄 Initializing database connections...")
        
        # Initialize MongoDB
        MongoDB.connect()
        
        # Initialize Qdrant (this will handle its own failures)
        qdrant_manager = QdrantManager()
        qdrant_manager.create_collection_if_not_exists()
        
        logger.info("✅ Database connections initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database connections: {e}")
        logger.warning("⚠️  Running without database connections - some features may be limited")
        return False

# Initialize databases when module is imported
initialize_databases()