#!/usr/bin/env python3
"""
Clear all data from both MongoDB and Qdrant databases
This script removes all products, chat history, sessions, and Qdrant vectors
"""

import logging
from database import MongoDB
from qdrant_utils import qdrant_manager
from config import QDRANT_COLLECTION_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_mongodb_data():
    """Clear all data from MongoDB collections"""
    try:
        logger.info("Starting MongoDB data cleanup...")
        
        # Get all collections
        products_collection = MongoDB.get_collection("products")
        chat_collection = MongoDB.get_collection("chat_history")
        sessions_collection = MongoDB.get_collection("sessions")
        users_collection = MongoDB.get_collection("users")
        
        # Count current documents
        products_count = products_collection.count_documents({})
        chat_count = chat_collection.count_documents({})
        sessions_count = sessions_collection.count_documents({})
        users_count = users_collection.count_documents({})
        
        logger.info(f"Current MongoDB data:")
        logger.info(f"  - Products: {products_count}")
        logger.info(f"  - Chat messages: {chat_count}")
        logger.info(f"  - Sessions: {sessions_count}")
        logger.info(f"  - Users: {users_count}")
        
        # Clear collections (keep users for authentication)
        logger.info("Clearing products collection...")
        products_result = products_collection.delete_many({})
        logger.info(f"Deleted {products_result.deleted_count} products")
        
        logger.info("Clearing chat history collection...")
        chat_result = chat_collection.delete_many({})
        logger.info(f"Deleted {chat_result.deleted_count} chat messages")
        
        logger.info("Clearing sessions collection...")
        sessions_result = sessions_collection.delete_many({})
        logger.info(f"Deleted {sessions_result.deleted_count} sessions")
        
        # Note: Keeping users collection for authentication purposes
        logger.info("Keeping users collection for authentication")
        
        logger.info("MongoDB cleanup completed!")
        
    except Exception as e:
        logger.error(f"Error clearing MongoDB data: {str(e)}")
        raise

def clear_qdrant_data():
    """Clear all vectors from Qdrant collection"""
    try:
        logger.info("Starting Qdrant data cleanup...")
        
        # Get collection info
        try:
            collection_info = qdrant_manager.client.get_collection(QDRANT_COLLECTION_NAME)
            vector_count = collection_info.points_count
            logger.info(f"Current Qdrant vectors: {vector_count}")
        except Exception as e:
            logger.warning(f"Could not get collection info: {str(e)}")
            vector_count = 0
        
        if vector_count > 0:
            logger.info(f"Deleting {vector_count} vectors from Qdrant...")
            
            # Delete all points from the collection using scroll and delete
            logger.info("Fetching all point IDs to delete...")
            
            # First, get all point IDs
            all_points = []
            offset = None
            
            while True:
                # Scroll through all points
                scroll_result = qdrant_manager.client.scroll(
                    collection_name=QDRANT_COLLECTION_NAME,
                    limit=100,
                    offset=offset
                )
                
                points, next_offset = scroll_result
                
                if points:
                    all_points.extend([point.id for point in points])
                
                if next_offset is None:
                    break
                
                offset = next_offset
            
            logger.info(f"Found {len(all_points)} points to delete")
            
            if all_points:
                # Delete points in batches
                batch_size = 100
                deleted_count = 0
                
                for i in range(0, len(all_points), batch_size):
                    batch = all_points[i:i + batch_size]
                    
                    delete_result = qdrant_manager.client.delete(
                        collection_name=QDRANT_COLLECTION_NAME,
                        points_selector=batch
                    )
                    
                    deleted_count += len(batch)
                    logger.info(f"Deleted {deleted_count}/{len(all_points)} points")
                
                logger.info(f"Total points deleted: {deleted_count}")
            else:
                logger.info("No points found to delete")
            
            logger.info(f"Qdrant deletion result: {delete_result}")
            
            # Verify deletion
            collection_info = qdrant_manager.client.get_collection(QDRANT_COLLECTION_NAME)
            remaining_vectors = collection_info.points_count
            logger.info(f"Remaining Qdrant vectors: {remaining_vectors}")
            
        else:
            logger.info("No vectors to delete from Qdrant")
        
        logger.info("Qdrant cleanup completed!")
        
    except Exception as e:
        logger.error(f"Error clearing Qdrant data: {str(e)}")
        raise

def main():
    """Main cleanup function"""
    try:
        logger.info("=" * 50)
        logger.info("STARTING COMPLETE DATABASE CLEANUP")
        logger.info("=" * 50)
        
        # Confirm with user
        print("\n⚠️  WARNING: This will delete ALL data from:")
        print("   - MongoDB: products, chat_history, sessions")
        print("   - Qdrant: all product vectors")
        print("   - Users collection will be preserved for authentication")
        
        confirmation = input("\nAre you sure you want to proceed? Type 'YES' to continue: ").strip().upper()
        
        if confirmation != 'YES':
            logger.info("Cleanup cancelled by user")
            return
        
        # Clear MongoDB data
        clear_mongodb_data()
        
        # Clear Qdrant data
        clear_qdrant_data()
        
        logger.info("=" * 50)
        logger.info("DATABASE CLEANUP COMPLETED SUCCESSFULLY!")
        logger.info("=" * 50)
        logger.info("You can now add new data without conflicts")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()