#!/usr/bin/env python3
"""
Test script to verify chatbot behavior when no products are found
"""
import asyncio
import logging
from chatbot import ChatbotManager

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_no_products():
    """Test chatbot when no products are available"""
    
    # Create chatbot manager
    chatbot = ChatbotManager()
    
    # Create test session
    from database import MongoDB
    sessions_collection = MongoDB.get_collection("sessions")
    
    test_session_id = "test_no_products_session"
    test_user_id = "test_user_123"
    
    # Create test session
    existing_session = sessions_collection.find_one({"session_id": test_session_id})
    if not existing_session:
        sessions_collection.insert_one({
            "session_id": test_session_id,
            "user_id": test_user_id,
            "created_at": "2024-01-01T00:00:00Z",
            "last_activity": "2024-01-01T00:00:00Z"
        })
        print(f"Created test session: {test_session_id}")
    
    # Test queries that should return no results
    test_queries = [
        "Do you have any smartphones?",
        "Show me iPhones",
        "Android phones available?",
        "Samsung Galaxy phones"
    ]
    
    print("\n" + "="*60)
    print("TESTING CHATBOT RESPONSES WHEN NO PHONE PRODUCTS AVAILABLE")
    print("="*60 + "\n")
    
    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        try:
            response = await chatbot.handle_text_query(
                session_id=test_session_id,
                query=query,
                limit=5
            )
            
            print(f"Response: {response.response}")
            print(f"Products found: {len(response.products)}")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_no_products())