#!/usr/bin/env python3
"""Test script to verify similar products context handling"""

import asyncio
import sys
import os
import uuid
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from database import MongoDB

def create_test_session(user_id="test_user"):
    """Create a test session directly in MongoDB"""
    try:
        db = MongoDB.get_db()
        sessions_collection = db["sessions"]
        
        session_id = str(uuid.uuid4())
        new_session = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }
        sessions_collection.insert_one(new_session)
        return session_id
    except Exception as e:
        print(f"Failed to create test session: {str(e)}")
        return None

async def test_similar_products_with_context():
    """Test similar products query with previous context"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a test session
    session_id = create_test_session("test_user")
    
    # First, ask about phones to establish context
    print("=== Step 1: Ask about phones ===")
    response1 = await chatbot_manager.handle_text_query(
        session_id=session_id,
        query="Do you have any smartphones?"
    )
    print(f"User: Do you have any smartphones?")
    print(f"Assistant: {response1.response}")
    print(f"Products found: {len(response1.products)}")
    print()
    
    # Now ask for similar products
    print("=== Step 2: Ask for similar products ===")
    response2 = await chatbot_manager.handle_text_query(
        session_id=session_id,
        query="Show me similar products"
    )
    print(f"User: Show me similar products")
    print(f"Assistant: {response2.response}")
    print(f"Products found: {len(response2.products)}")
    print()
    
    # Check chat history
    print("=== Chat History ===")
    history = chatbot_manager.get_session_history(session_id)
    for i, msg in enumerate(history.messages):
        print(f"{i+1}. {msg.role}: {msg.content}")
        if msg.products:
            print(f"   Products: {len(msg.products)} items")
    
if __name__ == "__main__":
    asyncio.run(test_similar_products_with_context())