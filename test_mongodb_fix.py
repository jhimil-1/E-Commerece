#!/usr/bin/env python3
"""
Comprehensive MongoDB connection test to diagnose and fix connection issues
"""
import os
import sys
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mongodb_connection(connection_string, description=""):
    """Test MongoDB connection with detailed diagnostics"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing MongoDB connection: {description}")
    logger.info(f"Connection string: {connection_string}")
    logger.info(f"{'='*60}")
    
    try:
        # Test connection with different configurations
        configurations = [
            {"name": "Basic connection", "config": {}},
            {"name": "With TLS settings", "config": {
                "tls": True,
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True,
                "serverSelectionTimeoutMS": 10000,
                "connectTimeoutMS": 10000,
                "socketTimeoutMS": 10000
            }},
            {"name": "With retry settings", "config": {
                "retryWrites": True,
                "w": "majority",
                "serverSelectionTimeoutMS": 15000,
                "connectTimeoutMS": 15000,
                "socketTimeoutMS": 15000
            }},
            {"name": "Full configuration", "config": {
                "tls": True,
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True,
                "retryWrites": True,
                "w": "majority",
                "serverSelectionTimeoutMS": 20000,
                "connectTimeoutMS": 20000,
                "socketTimeoutMS": 20000,
                "maxPoolSize": 10,
                "minPoolSize": 1,
                "maxIdleTimeMS": 30000
            }}
        ]
        
        for config_test in configurations:
            logger.info(f"\n--- Testing: {config_test['name']} ---")
            try:
                client = MongoClient(connection_string, **config_test['config'])
                
                # Test basic connection
                logger.info("Attempting to ping server...")
                client.admin.command('ping')
                logger.info("✅ Ping successful!")
                
                # Test database access
                logger.info("Testing database access...")
                db = client.get_database()
                collections = db.list_collection_names()
                logger.info(f"✅ Database accessible. Collections: {len(collections)}")
                
                # Test server info
                logger.info("Getting server info...")
                server_info = client.server_info()
                logger.info(f"✅ Server version: {server_info.get('version', 'Unknown')}")
                
                client.close()
                logger.info("✅ Connection test PASSED")
                return True
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"❌ Connection failed: {e}")
                logger.error(f"Error type: {type(e).__name__}")
                if hasattr(e, 'details'):
                    logger.error(f"Error details: {e.details}")
                    
            except ConfigurationError as e:
                logger.error(f"❌ Configuration error: {e}")
                logger.error(f"Error type: {type(e).__name__}")
                
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                logger.error(f"Error type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
                
            finally:
                try:
                    client.close()
                except:
                    pass
    
    except Exception as e:
        logger.error(f"❌ Critical error during connection test: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def test_local_mongodb():
    """Test local MongoDB connection"""
    logger.info("\n🔄 Testing LOCAL MongoDB connection...")
    return test_mongodb_connection("mongodb://localhost:27017/", "Local MongoDB")

def test_cloud_mongodb():
    """Test cloud MongoDB connection with current .env settings"""
    logger.info("\n🔄 Testing CLOUD MongoDB connection...")
    
    # Load from current .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        mongodb_url = os.getenv('MONGODB_URL', '')
        
        if not mongodb_url:
            logger.error("❌ MONGODB_URL not found in .env file")
            return False
            
        return test_mongodb_connection(mongodb_url, "Cloud MongoDB from .env")
        
    except ImportError:
        logger.error("❌ python-dotenv not installed, trying direct URL from .env")
        # Try to read .env file directly
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('MONGODB_URL='):
                        url = line.split('=', 1)[1].strip()
                        return test_mongodb_connection(url, "Cloud MongoDB from .env (manual read)")
        except Exception as e:
            logger.error(f"❌ Failed to read .env file: {e}")
            return False

def suggest_mongodb_fix():
    """Suggest fixes based on common MongoDB issues"""
    logger.info("\n🔧 SUGGESTED FIXES:")
    logger.info("1. Check MongoDB Atlas whitelist - ensure your IP is allowed")
    logger.info("2. Verify MongoDB Atlas cluster is running")
    logger.info("3. Check network connectivity to MongoDB Atlas")
    logger.info("4. Try different TLS/SSL configurations")
    logger.info("5. Check if MongoDB Atlas requires specific connection options")
    logger.info("6. Verify username/password in connection string")
    logger.info("7. Check if MongoDB Atlas has connection limits")
    logger.info("8. Try connecting from MongoDB Compass to verify credentials")

def main():
    """Main test function"""
    logger.info("🚀 Starting MongoDB Connection Diagnostics")
    
    # Test local MongoDB first
    local_success = test_local_mongodb()
    
    # Test cloud MongoDB
    cloud_success = test_cloud_mongodb()
    
    # Provide suggestions
    suggest_mongodb_fix()
    
    # Summary
    logger.info("\n📊 SUMMARY:")
    logger.info(f"Local MongoDB: {'✅ WORKING' if local_success else '❌ FAILED'}")
    logger.info(f"Cloud MongoDB: {'✅ WORKING' if cloud_success else '❌ FAILED'}")
    
    if not cloud_success:
        logger.warning("\n⚠️  Cloud MongoDB is not working. Application will run with limited features.")
        logger.info("The application is designed to work without databases, but some features will be limited.")
    
    return cloud_success or local_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)