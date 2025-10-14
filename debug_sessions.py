#!/usr/bin/env python3
"""
Debug script to check sessions and their user associations
"""

import asyncio
import logging
from database import MongoDB
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_sessions():
    """Debug sessions and user associations"""
    try:
        # Get database connection
        db = MongoDB.get_db()
        
        if db is None:
            logger.error("Failed to get database connection")
            return
            
        logger.info("=== Checking sessions ===")
        
        # Get all sessions
        sessions = list(db.sessions.find({}).limit(10))
        logger.info(f"Found {len(sessions)} sessions")
        
        for session in sessions:
            session_id = session.get('session_id')
            user_id = session.get('user_id')
            created_at = session.get('created_at')
            
            logger.info(f"Session ID: {session_id}")
            logger.info(f"  User ID: {user_id}")
            logger.info(f"  Created at: {created_at}")
            
            # Look up the user details
            if user_id:
                user = db.users.find_one({"user_id": user_id})
                if user:
                    logger.info(f"  User details:")
                    logger.info(f"    Username: {user.get('username')}")
                    logger.info(f"    Email: {user.get('email')}")
                    logger.info(f"    MongoDB _id: {user.get('_id')}")
                else:
                    logger.info(f"  No user found with user_id: {user_id}")
            else:
                logger.info(f"  No user_id in session")
            
            logger.info("")
        
        # Test specific session ID from our debug script
        test_session_id = "test_session_123"
        logger.info(f"=== Testing session lookup for: {test_session_id} ===")
        
        session = db.sessions.find_one({"session_id": test_session_id})
        if session:
            logger.info(f"Found session: {session}")
        else:
            logger.info(f"No session found with ID: {test_session_id}")
            
    except Exception as e:
        logger.error(f"Error debugging sessions: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(debug_sessions())