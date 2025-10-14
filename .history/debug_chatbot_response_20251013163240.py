#!/usr/bin/env python3
"""
Debug script to see exactly what the chatbot returns for different queries
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from session_manager import SessionManager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_chatbot_responses():
    """Test chatbot responses for different queries"""
    
    # Initialize managers
    session_manager = SessionManager()
    chatbot_manager = ChatbotManager()
    
    # Create a test session
    session_id = session_manager.create_session("test_user")
    print(f"Created test session: {session_id}")
    
    # Test queries
    test_queries = [
        "I want to buy a pant",
        "I want to buy pants", 
        "I want to buy trousers",
        "I want to buy jeans",
        "Business Professional Dress",
        "I want to buy a dress"
    ]
    
    print("\n=== CHATBOT RESPONSE DEBUG ===\n")
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 60)
        
        try:
            # Get chatbot response
            response = await chatbot_manager.handle_text_query(session_id, query)
            
            print(f"Response: {response.response}")
            print(f"Products returned: {len(response.products)}")
            
            if response.products:
                print("\nProducts:")
                for i, product in enumerate(response.products[:5], 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    score = product.get('similarity_score', 0)
                    print(f"  {i}. {name} ({category}) - Score: {score:.3f}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("Starting chatbot response debug...")
    asyncio.run(debug_chatbot_responses())
    print("Debug complete!")