#!/usr/bin/env python3

import sys
import asyncio
sys.path.append('.')

from chatbot import ChatbotManager
from auth import create_new_session
from database import MongoDB
import json

async def debug_session():
    """Debug session creation and verification"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a proper session
    user_id = "test_user_123"
    session_id = await create_new_session(user_id)
    print(f"Created session: {session_id}")
    
    # Check if session exists in database
    db = MongoDB.get_db()
    session = db.sessions.find_one({"session_id": session_id})
    print(f"Session in database: {session}")
    
    # Test verification
    print(f"Verifying session {session_id}...")
    result = chatbot_manager._verify_session(session_id)
    print(f"Verification result: {result}")
    
    # Test user retrieval
    print(f"Getting user from session...")
    user = chatbot_manager._get_user_from_session(session_id)
    print(f"User from session: {user}")

if __name__ == "__main__":
    asyncio.run(debug_session())