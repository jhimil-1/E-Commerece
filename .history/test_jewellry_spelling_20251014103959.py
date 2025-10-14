#!/usr/bin/env python3
"""
Test script to verify the "jewellry" spelling fix
"""

import asyncio
import uuid
from database import MongoDB
from chatbot import ChatbotManager

async def test_jewellry_spelling():
    """Test the jewellry spelling specifically"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a test session directly in MongoDB
    session_id = str(uuid.uuid4())
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"  # Valid UUID format
    
    # Insert session directly
    db = MongoDB()
    await db.sessions.insert_one({
        "session_id": session_id,
        "user_id": user_id,
        "created_at": "2024-01-01T00:00:00Z",
        "last_accessed": "2024-01-01T00:00:00Z"
    })
    
    print(f"Created test session: {session_id}")
    print(f"Using user ID: {user_id}")
    
    # Test the problematic query from the logs
    query = "show me jewellry"
    print(f"\nTesting query: '{query}'")
    
    try:
        # Process the query
        response = await chatbot_manager.handle_text_query(session_id, query)
        
        if response and hasattr(response, 'products'):
            products = response.products if response.products else []
            count = len(products)
            
            print(f"✅ Found {count} products")
            print(f"Response: {response.response}")
            
            if count > 0:
                print("\nFirst 5 products:")
                for j, product in enumerate(products[:5]):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    price = product.get('price', 'Unknown')
                    score = product.get('similarity_score', 0)
                    print(f"  {j+1}. {name} - {category} (${price}) - Score: {score:.3f}")
                
                return True
            else:
                print("❌ No products found")
                return False
        else:
            print(f"❌ Query failed: Invalid response format")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_jewellry_spelling())
    if result:
        print("\n🎉 Test PASSED! The jewellry spelling fix is working.")
    else:
        print("\n❌ Test FAILED! The jewellry spelling still has issues.")