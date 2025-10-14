#!/usr/bin/env python3
"""
Script to debug user lookup logic
"""

import asyncio
from database import MongoDB
from bson import ObjectId
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_user_lookup():
    """Debug user lookup logic"""
    
    # Get database instance
    db = MongoDB.get_db()
    
    # Test different user lookup scenarios
    test_user_ids = ["test_user", "test_user_123"]
    
    for user_id in test_user_ids:
        logger.info(f"\n=== Testing user lookup for: {user_id} ===")
        
        # Try to find user by ObjectId
        try:
            user_by_objectid = db.users.find_one({"_id": ObjectId(user_id)})
            logger.info(f"Find by ObjectId: {user_by_objectid is not None}")
            if user_by_objectid:
                logger.info(f"  User ID field: {user_by_objectid.get('user_id')}")
                logger.info(f"  Username field: {user_by_objectid.get('username')}")
        except Exception as e:
            logger.info(f"  ObjectId conversion failed: {e}")
        
        # Try to find user by user_id field
        user_by_userid = db.users.find_one({"user_id": user_id})
        logger.info(f"Find by user_id field: {user_by_userid is not None}")
        if user_by_userid:
            logger.info(f"  User ID field: {user_by_userid.get('user_id')}")
            logger.info(f"  Username field: {user_by_userid.get('username')}")
            logger.info(f"  MongoDB _id: {user_by_userid.get('_id')}")
        
        # Try to find user by username field
        user_by_username = db.users.find_one({"username": user_id})
        logger.info(f"Find by username field: {user_by_username is not None}")
        if user_by_username:
            logger.info(f"  User ID field: {user_by_username.get('user_id')}")
            logger.info(f"  Username field: {user_by_username.get('username')}")
            logger.info(f"  MongoDB _id: {user_by_username.get('_id')}")
    
    # Also check what users exist in the database
    logger.info("\n=== All users in database ===")
    users = list(db.users.find({}).limit(5))
    for user in users:
        logger.info(f"User:")
        logger.info(f"  _id: {user.get('_id')}")
        logger.info(f"  user_id: {user.get('user_id')}")
        logger.info(f"  username: {user.get('username')}")
        logger.info(f"  email: {user.get('email')}")

if __name__ == "__main__":
    asyncio.run(debug_user_lookup())