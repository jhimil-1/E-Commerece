#!/usr/bin/env python3
"""
MongoDB SSL/TLS Connection Fix
This script provides solutions for common MongoDB SSL/TLS connection issues
"""
import os
import ssl
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mongodb_connection_with_ssl_fix(connection_string, db_name="test"):
    """Test MongoDB connection with various SSL/TLS configurations"""
    
    logger.info(f"Testing MongoDB connection with SSL fixes...")
    logger.info(f"Connection string: {connection_string[:50]}...")
    
    # Test configurations for different SSL/TLS scenarios
    test_configs = [
        {
            "name": "Standard SSL (recommended)",
            "config": {
                'serverSelectionTimeoutMS': 10000,
                'connectTimeoutMS': 10000,
                'socketTimeoutMS': 10000,
                'tls': True,
                'tlsAllowInvalidCertificates': False,
                'tlsAllowInvalidHostnames': False,
                'ssl_cert_reqs': ssl.CERT_REQUIRED,
                'retryWrites': True,
                'w': 'majority'
            }
        },
        {
            "name": "Relaxed SSL (compatibility)",
            "config": {
                'serverSelectionTimeoutMS': 10000,
                'connectTimeoutMS': 10000,
                'socketTimeoutMS': 10000,
                'tls': True,
                'tlsAllowInvalidCertificates': True,
                'tlsAllowInvalidHostnames': True,
                'ssl_cert_reqs': ssl.CERT_NONE,
                'retryWrites': True,
                'w': 'majority'
            }
        },
        {
            "name": "No SSL (local only)",
            "config": {
                'serverSelectionTimeoutMS': 5000,
                'connectTimeoutMS': 5000,
                'socketTimeoutMS': 5000,
                'tls': False,
                'retryWrites': False
            }
        }
    ]
    
    for test_config in test_configs:
        logger.info(f"\n--- Testing: {test_config['name']} ---")
        try:
            client = MongoClient(connection_string, **test_config['config'])
            client.admin.command('ping')
            
            # Test database access
            db = client[db_name]
            collections = db.list_collection_names()
            
            logger.info(f"✅ SUCCESS: {test_config['name']}")
            logger.info(f"   - Collections found: {len(collections)}")
            logger.info(f"   - Server info: {client.server_info().get('version', 'Unknown')}")
            
            client.close()
            return True, test_config['config']
            
        except Exception as e:
            logger.error(f"❌ FAILED: {test_config['name']}")
            logger.error(f"   Error: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            
            try:
                client.close()
            except:
                pass
    
    return False, None

def create_fixed_connection_string(original_url):
    """Create a fixed connection string with proper SSL parameters"""
    
    # Parse and fix common issues in connection strings
    fixed_url = original_url
    
    # Ensure proper URL encoding
    if '@' in fixed_url:
        # URL might need encoding fixes
        parts = fixed_url.split('@')
        if len(parts) == 2:
            credentials_part = parts[0]
            server_part = parts[1]
            
            # Fix common encoding issues
            if ':' in credentials_part:
                cred_parts = credentials_part.split('://')
                if len(cred_parts) == 2:
                    protocol = cred_parts[0]
                    user_pass = cred_parts[1]
                    
                    # Properly encode username and password
                    if ':' in user_pass:
                        username, password = user_pass.split(':', 1)
                        username = quote_plus(username)
                        password = quote_plus(password)
                        
                        fixed_url = f"{protocol}://{username}:{password}@{server_part}"
    
    # Add SSL parameters if not present
    if 'tls=' not in fixed_url.lower() and 'ssl=' not in fixed_url.lower():
        separator = '&' if '?' in fixed_url else '?'
        fixed_url += f"{separator}tls=true&retryWrites=true&w=majority"
    
    return fixed_url

def main():
    """Main function to test and fix MongoDB connections"""
    
    logger.info("🔧 MongoDB SSL/TLS Connection Fix Tool")
    logger.info("=" * 50)
    
    # Load connection string from .env or use a test one
    try:
        from dotenv import load_dotenv
        load_dotenv()
        mongodb_url = os.getenv('MONGODB_URL', '')
        
        if not mongodb_url:
            logger.error("❌ MONGODB_URL not found in .env file")
            return False
            
    except ImportError:
        logger.warning("python-dotenv not installed, trying to read .env manually")
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('MONGODB_URL='):
                        mongodb_url = line.split('=', 1)[1].strip()
                        break
                else:
                    logger.error("❌ MONGODB_URL not found in .env file")
                    return False
        except Exception as e:
            logger.error(f"❌ Failed to read .env file: {e}")
            return False
    
    logger.info(f"Original connection string: {mongodb_url[:50]}...")
    
    # Fix connection string
    fixed_url = create_fixed_connection_string(mongodb_url)
    logger.info(f"Fixed connection string: {fixed_url[:50]}...")
    
    # Test the connection
    success, working_config = test_mongodb_connection_with_ssl_fix(fixed_url)
    
    if success:
        logger.info("\n✅ MongoDB connection successful!")
        logger.info("You can now update your database.py with the working configuration")
        
        # Save working configuration
        with open('mongodb_working_config.py', 'w') as f:
            f.write("# Working MongoDB configuration\n")
            f.write(f"MONGODB_URL = '{fixed_url}'\n")
            f.write("CONNECTION_OPTIONS = {\n")
            for key, value in working_config.items():
                f.write(f"    '{key}': {repr(value)},\n")
            f.write("}\n")
        
        logger.info("Working configuration saved to 'mongodb_working_config.py'")
        return True
        
    else:
        logger.error("\n❌ All MongoDB connection attempts failed")
        logger.error("Please check:")
        logger.error("1. MongoDB Atlas cluster is running")
        logger.error("2. Your IP address is whitelisted in Atlas")
        logger.error("3. Connection string credentials are correct")
        logger.error("4. Network connectivity to MongoDB Atlas")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)