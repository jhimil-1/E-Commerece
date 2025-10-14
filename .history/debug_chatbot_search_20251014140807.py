#!/usr/bin/env python3

import sys
import asyncio
sys.path.append('.')

from chatbot import ChatbotManager
from auth import create_new_session
from database import MongoDB
import json

async def test_chatbot_search():
    """Test chatbot search functionality to understand why it's failing"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a proper session
    user_id = "test_user_123"
    session_id = await create_new_session(user_id)
    print(f"Created session: {session_id}")
    
    # Test queries that are failing
    test_queries = [
        "show me watch",
        "smartwatches", 
        "show me clothes",
        "show me jewellery"
    ]
    
    print("Testing chatbot search functionality...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 40)
        
        try:
            # Process the query
            response = await chatbot_manager.handle_text_query(query, session_id, user_id)
            print(f"Response: {response}")
            
            # Check if session was created and get chat history
            try:
                history = chatbot_manager.get_session_history(session_id)
                if history and 'messages' in history:
                    print(f"Chat history has {len(history['messages'])} messages")
            except ValueError:
                print("No session history available")
                 
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_chatbot_search())