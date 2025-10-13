import ssl
import certifi
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Test MongoDB connection with different SSL configurations
def test_connection():
    mongodb_url = "mongodb+srv://jhilmiljain128:Gungun%4028@cluster0.mrqgflo.mongodb.net/"
    
    # Try different SSL configurations
    configs = [
        {
            "name": "Default SSL",
            "params": {}
        },
        {
            "name": "SSL with certifi",
            "params": {
                "tlsCAFile": certifi.where(),
                "tlsAllowInvalidCertificates": False
            }
        },
        {
            "name": "SSL allow invalid certificates",
            "params": {
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True
            }
        },
        {
            "name": "No SSL",
            "params": {
                "tls": False
            }
        }
    ]
    
    for config in configs:
        print(f"\nTesting: {config['name']}")
        try:
            client = MongoClient(
                mongodb_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                **config["params"]
            )
            client.admin.command('ping')
            print(f"✓ Success with {config['name']}")
            client.close()
            return True
        except Exception as e:
            print(f"✗ Failed with {config['name']}: {e}")
    
    return False

if __name__ == "__main__":
    print("Python SSL version:", ssl.OPENSSL_VERSION)
    print("Certifi path:", certifi.where())
    success = test_connection()
    if not success:
        print("\nAll connection attempts failed. This might be a network or certificate issue.")