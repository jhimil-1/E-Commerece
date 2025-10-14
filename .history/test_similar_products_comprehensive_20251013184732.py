#!/usr/bin/env python3
"""Comprehensive test script to verify similar products context handling"""

import asyncio
import uuid
from datetime import datetime
from pymongo import MongoClient
from chatbot import ChatbotManager

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['jewelry_chatbot']
sessions_collection = db['sessions']
chat_collection = db['chat_history']

async def create_test_session():
    """Create a test session in MongoDB"""
    session_id = str(uuid.uuid4())
    session_data = {
        'session_id': session_id,
        'user_id': 'test_user_123',  # Use string user_id instead of ObjectId
        'created_at': datetime.utcnow(),
        'last_activity': datetime.utcnow()
    }
    sessions_collection.insert_one(session_data)
    return session_id

async def test_similar_products_scenarios():
    """Test various similar product scenarios"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    print("=== TESTING SIMILAR PRODUCTS WITH CONTEXT ===\n")
    
    # Test Case 1: Phones -> Similar products
    print("=== Test Case 1: Phones -> Similar products ===")
    session_id = create_test_session()
    
    # First ask about phones
    print("Step 1: Ask about phones")
    response1 = await chatbot_manager.handle_text_query(session_id, "Do you have any phones?")
    print(f"Assistant: {response1.response}")
    print(f"Products found: {len(response1.products)}")
    print()
    
    # Then ask for similar products
    print("Step 2: Ask for similar products")
    response2 = await chatbot_manager.handle_text_query(session_id, "Show me similar products")
    print(f"Assistant: {response2.response}")
    print(f"Products found: {len(response2.products)}")
    print()
    
    # Test Case 2: Jewelry -> Similar products
    print("=== Test Case 2: Jewelry -> Similar products ===")
    session_id2 = create_test_session()
    
    # First ask about jewelry
    print("Step 1: Ask about jewelry")
    response3 = await chatbot_manager.handle_text_query(session_id2, "Do you have any jewelry?")
    print(f"Assistant: {response3.response}")
    print(f"Products found: {len(response3.products)}")
    print()
    
    # Then ask for similar products
    print("Step 2: Ask for similar products")
    response4 = await chatbot_manager.handle_text_query(session_id2, "Can you recommend similar products?")
    print(f"Assistant: {response4.response}")
    print(f"Products found: {len(response4.products)}")
    print()
    
    # Test Case 3: Direct similar product query (no context)
    print("=== Test Case 3: Direct similar product query (no context) ===")
    session_id3 = create_test_session()
    
    print("Step 1: Direct similar product query")
    response5 = await chatbot_manager.handle_text_query(session_id3, "Show me similar products")
    print(f"Assistant: {response5.response}")
    print(f"Products found: {len(response5.products)}")
    print()
    
    # Test Case 4: Multiple context layers
    print("=== Test Case 4: Multiple context layers ===")
    session_id4 = create_test_session()
    
    # Ask about watches
    print("Step 1: Ask about watches")
    response6 = await chatbot_manager.handle_text_query(session_id4, "Do you have any watches?")
    print(f"Assistant: {response6.response}")
    print(f"Products found: {len(response6.products)}")
    print()
    
    # Ask about jewelry
    print("Step 2: Ask about jewelry")
    response7 = await chatbot_manager.handle_text_query(session_id4, "What about jewelry?")
    print(f"Assistant: {response7.response}")
    print(f"Products found: {len(response7.products)}")
    print()
    
    # Ask for similar products (should use most recent context - jewelry)
    print("Step 3: Ask for similar products")
    response8 = await chatbot_manager.handle_text_query(session_id4, "Show me similar items")
    print(f"Assistant: {response8.response}")
    print(f"Products found: {len(response8.products)}")
    print()

if __name__ == "__main__":
    asyncio.run(test_similar_products_scenarios())