#!/usr/bin/env python3
"""
Comprehensive database cleanup script
Clears all data from both MongoDB and Qdrant databases
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

class DatabaseCleaner:
    def __init__(self):
        """Initialize database connections"""
        # MongoDB connection
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.mongo_client = MongoClient(self.mongo_uri)
        self.db_name = os.getenv("DATABASE_NAME", "jewellery_db")
        self.mongo_db = self.mongo_client[self.db_name]
        
        # Qdrant connection
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if self.qdrant_api_key:
            self.qdrant_client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key
            )
        else:
            self.qdrant_client = QdrantClient(url=self.qdrant_url)
        
        logger.info("Database connections initialized")
    
    async def clear_mongodb_collections(self):
        """Clear all collections from MongoDB"""
        try:
            logger.info("Starting MongoDB cleanup...")
            
            # Get all collection names
            collections = self.mongo_db.list_collection_names()
            logger.info(f"Found {len(collections)} collections: {collections}")
            
            if not collections:
                logger.info("No collections found in MongoDB")
                return
            
            # Drop each collection
            for collection_name in collections:
                try:
                    self.mongo_db.drop_collection(collection_name)
                    logger.info(f"✓ Dropped collection: {collection_name}")
                except Exception as e:
                    logger.error(f"✗ Failed to drop collection {collection_name}: {e}")
            
            # Verify cleanup
            remaining_collections = self.mongo_db.list_collection_names()
            logger.info(f"MongoDB cleanup complete. Remaining collections: {len(remaining_collections)}")
            
        except Exception as e:
            logger.error(f"MongoDB cleanup failed: {e}")
            raise
    
    async def clear_qdrant_collections(self):
        """Clear all collections from Qdrant"""
        try:
            logger.info("Starting Qdrant cleanup...")
            
            # Get all collection names
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            logger.info(f"Found {len(collection_names)} Qdrant collections: {collection_names}")
            
            if not collection_names:
                logger.info("No collections found in Qdrant")
                return
            
            # Delete each collection
            for collection_name in collection_names:
                try:
                    self.qdrant_client.delete_collection(collection_name)
                    logger.info(f"✓ Deleted Qdrant collection: {collection_name}")
                except Exception as e:
                    logger.error(f"✗ Failed to delete Qdrant collection {collection_name}: {e}")
            
            # Verify cleanup
            remaining_collections = self.qdrant_client.get_collections()
            remaining_names = [col.name for col in remaining_collections.collections]
            logger.info(f"Qdrant cleanup complete. Remaining collections: {len(remaining_names)}")
            
        except Exception as e:
            logger.error(f"Qdrant cleanup failed: {e}")
            raise
    
    async def clear_specific_collections(self):
        """Clear specific collections that are commonly used"""
        try:
            logger.info("Clearing specific collections...")
            
            # Common MongoDB collections
            mongo_collections = ['products', 'users', 'sessions', 'chat_history', 'uploaded_products']
            
            for collection_name in mongo_collections:
                if collection_name in self.mongo_db.list_collection_names():
                    try:
                        result = self.mongo_db[collection_name].delete_many({})
                        logger.info(f"✓ Cleared {result.deleted_count} documents from {collection_name}")
                    except Exception as e:
                        logger.error(f"✗ Failed to clear {collection_name}: {e}")
            
            # Common Qdrant collections
            qdrant_collections = ['products', 'products_local', 'jewelry_products']
            
            for collection_name in qdrant_collections:
                try:
                    # Check if collection exists
                    self.qdrant_client.get_collection(collection_name)
                    # Delete all points in the collection
                    self.qdrant_client.delete_collection(collection_name)
                    logger.info(f"✓ Deleted Qdrant collection: {collection_name}")
                except Exception as e:
                    logger.info(f"Collection {collection_name} not found or already deleted")
            
        except Exception as e:
            logger.error(f"Specific collections cleanup failed: {e}")
    
    async def show_database_stats(self):
        """Show current database statistics"""
        try:
            logger.info("=== DATABASE STATISTICS ===")
            
            # MongoDB stats
            collections = self.mongo_db.list_collection_names()
            logger.info(f"MongoDB Collections ({len(collections)}):")
            for collection_name in collections:
                count = self.mongo_db[collection_name].count_documents({})
                logger.info(f"  {collection_name}: {count} documents")
            
            # Qdrant stats
            collections = self.qdrant_client.get_collections()
            logger.info(f"Qdrant Collections ({len(collections.collections)}):")
            for collection in collections.collections:
                info = self.qdrant_client.get_collection(collection.name)
                logger.info(f"  {collection.name}: {info.points_count} points, {info.vectors_count} vectors")
            
            logger.info("=== END STATISTICS ===")
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
    
    def close_connections(self):
        """Close database connections"""
        try:
            self.mongo_client.close()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")

async def main():
    """Main cleanup function"""
    cleaner = DatabaseCleaner()
    
    try:
        print("\n" + "="*60)
        print("DATABASE CLEANUP UTILITY")
        print("="*60 + "\n")
        
        # Show current stats
        await cleaner.show_database_stats()
        
        print("\n" + "-"*40)
        print("CLEANUP OPTIONS:")
        print("1. Clear ALL data (complete wipe)")
        print("2. Clear specific collections only")
        print("3. Show statistics only")
        print("-"*40 + "\n")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n⚠️  WARNING: This will delete ALL data from both databases!")
            confirm = input("Type 'DELETE ALL' to confirm: ").strip()
            
            if confirm == "DELETE ALL":
                print("\nStarting complete database cleanup...")
                await cleaner.clear_mongodb_collections()
                await cleaner.clear_qdrant_collections()
                print("\n✅ Complete cleanup finished!")
            else:
                print("\n❌ Cleanup cancelled.")
        
        elif choice == "2":
            print("\nClearing specific collections...")
            await cleaner.clear_specific_collections()
            print("\n✅ Specific collections cleanup finished!")
        
        elif choice == "3":
            print("\nStatistics shown above.")
        
        else:
            print("\n❌ Invalid choice. Exiting.")
        
        # Show final stats
        print("\n" + "-"*40)
        print("FINAL DATABASE STATUS:")
        await cleaner.show_database_stats()
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        print(f"\n❌ Error during cleanup: {e}")
    
    finally:
        cleaner.close_connections()
        print("\n👋 Cleanup utility finished.")

if __name__ == "__main__":
    asyncio.run(main())