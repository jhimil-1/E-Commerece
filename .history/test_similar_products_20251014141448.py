#!/usr/bin/env python3

import sys
import asyncio
sys.path.append('.')

from chatbot import ChatbotManager
from auth import create_new_session
from database import MongoDB
import json

async def test_similar_products():
    """Test the similar products functionality with proper chat history"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a proper session
    user_id = "test_user_123"
    session_id = await create_new_session(user_id)
    print(f"Created session: {session_id}")
    
    print("Testing similar products with proper chat history...")
    print("=" * 60)
    
    # Step 1: Ask for men's watch first
    print("\nStep 1: Ask for men's watch")
    print("-" * 40)
    
    try:
        response1 = await chatbot_manager.handle_text_query(session_id, "men's watch")
        print(f"Response: {response1.response}")
        print(f"Products found: {len(response1.products)}")
        if response1.products:
            for i, product in enumerate(response1.products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return
    
    # Step 2: Now ask for similar products
    print("\nStep 2: Ask for similar products")
    print("-" * 40)
    
    try:
        response2 = await chatbot_manager.handle_text_query(session_id, "show me similar product")
        print(f"Response: {response2.response}")
        print(f"Products found: {len(response2.products)}")
        if response2.products:
            for i, product in enumerate(response2.products[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')}")
        else:
            print("No products found for similar search")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Step 3: Check chat history
    print("\nStep 3: Check chat history")
    print("-" * 40)
    
    try:
        history = chatbot_manager.get_session_history(session_id)
        if history and 'messages' in history:
            print(f"Chat history has {len(history['messages'])} messages:")
            for i, msg in enumerate(history['messages'][-4:], 1):  # Show last 4 messages
                print(f"  {i}. {msg.get('role', 'unknown')}: {msg.get('content', 'no content')}")
                if msg.get('products'):
                    print(f"     Products: {[p.get('name', 'Unknown') for p in msg['products'][:2]]}")
    except Exception as e:
        print(f"Error getting history: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_similar_products())