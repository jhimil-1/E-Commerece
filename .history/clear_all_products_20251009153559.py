#!/usr/bin/env python3
"""
Script to clear all products from the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_utils import QdrantManager
from database import MongoDB
from pymongo import MongoClient

def clear_all_products():
    """Clear all products from both Qdrant and MongoDB"""
    try:
        # Initialize Qdrant manager
        qdrant_manager = QdrantManager()
        
        print("🗑️ Starting to clear all products...")
        
        # Clear from MongoDB
        print("📊 Clearing MongoDB products collection...")
        products_collection = MongoDB.get_collection("products")
        products_result = products_collection.delete_many({})
        print(f"✅ Deleted {products_result.deleted_count} products from MongoDB")
        
        # Clear from Qdrant
        print("🔍 Clearing Qdrant vector database...")
        try:
            # Get all points to delete
            from qdrant_client import models
            
            # Try to get all points first
            scroll_result = qdrant_manager.client.scroll(
                collection_name=qdrant_manager.collection_name,
                limit=1000,
                with_payload=False,
                with_vectors=False
            )
            
            if scroll_result and scroll_result[0]:
                point_ids = [point.id for point in scroll_result[0]]
                if point_ids:
                    qdrant_manager.client.delete(
                        collection_name=qdrant_manager.collection_name,
                        points_selector=models.PointIdsList(points=point_ids)
                    )
                    print(f"✅ Deleted {len(point_ids)} vectors from Qdrant")
                else:
                    print("ℹ️ No points found in Qdrant to delete")
            else:
                print("ℹ️ No points found in Qdrant to delete")
                
        except Exception as e:
            print(f"⚠️ Could not clear Qdrant (may be empty): {e}")
        
        print("\n✅ All products cleared successfully!")
        print("💡 You can now upload new products without conflicts.")
        
    except Exception as e:
        print(f"❌ Error clearing products: {str(e)}")
        return False
    
    return True

def verify_clear():
    """Verify that products are cleared"""
    try:
        # Check MongoDB
        products_collection = MongoDB.get_collection("products")
        mongo_count = products_collection.count_documents({})
        print(f"📊 MongoDB products count: {mongo_count}")
        
        # Check Qdrant
        qdrant_manager = QdrantManager()
        try:
            qdrant_count = qdrant_manager.client.count(
                collection_name=qdrant_manager.collection_name
            ).count
            print(f"🔍 Qdrant vectors count: {qdrant_count}")
        except:
            print("🔍 Qdrant appears to be empty")
            
        if mongo_count == 0:
            print("✅ Verification: Database is clean!")
            return True
        else:
            print("⚠️ Warning: Some products may still exist")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting complete product cleanup...\n")
    
    # Clear all products
    if clear_all_products():
        print("\n🔍 Verifying cleanup...")
        verify_clear()
        print("\n🎉 Cleanup completed successfully!")
    else:
        print("\n❌ Cleanup failed!")
        sys.exit(1)