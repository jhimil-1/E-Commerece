#!/usr/bin/env python3
"""
Test script to debug phone-related chatbot queries
"""
import asyncio
import logging
from chatbot import ChatbotManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_phone_queries():
    """Test various phone-related queries"""
    
    # Create chatbot manager
    chatbot = ChatbotManager()
    
    # Create a test session (we'll need to create one first)
    from database import MongoDB
    sessions_collection = MongoDB.get_collection("sessions")
    
    # Create test session with a known user
    test_session_id = "test_phone_session_123"
    test_user_id = "test_user_123"
    
    # Check if session exists, create if not
    existing_session = sessions_collection.find_one({"session_id": test_session_id})
    if not existing_session:
        sessions_collection.insert_one({
            "session_id": test_session_id,
            "user_id": test_user_id,
            "created_at": "2024-01-01T00:00:00Z",
            "last_activity": "2024-01-01T00:00:00Z"
        })
        print(f"Created test session: {test_session_id}")
    
    # Test various phone-related queries
    test_queries = [
        "Do you have any smartphones?",
        "Show me phones",
        "I need a new phone",
        "What mobile phones do you have?",
        "iPhone or Android phones",
        "Smartphone recommendations",
        "Cell phones available?",
        "Telephone options",
        "Phone accessories",
        "Mobile devices"
    ]
    
    print("\n" + "="*60)
    print("TESTING PHONE-RELATED CHATBOT QUERIES")
    print("="*60 + "\n")
    
    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        try:
            # Process the query
            response = await chatbot.handle_text_query(
                session_id=test_session_id,
                query=query,
                category="electronics",  # Try filtering by electronics
                limit=10
            )
            
            print(f"Response: {response.response}")
            print(f"Products found: {len(response.products)}")
            
            if response.products:
                for i, product in enumerate(response.products, 1):
                    print(f"  {i}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} - ${product.get('price', 'N/A')}")
                    if 'phone' in product.get('description', '').lower() or 'phone' in product.get('name', '').lower():
                        print(f"     [CONTAINS PHONE-RELATED TERMS]")
            else:
                print("  No products found")
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_phone_queries())