#!/usr/bin/env python3
"""
Test script for color-based product search
Tests the enhanced search functionality with color-specific queries
"""

import asyncio
import logging
from chatbot import ChatbotManager
from auth import create_new_session

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_color_search():
    """Test the color-based search functionality"""
    
    print("\n=== TESTING COLOR-BASED SEARCH ===\n")
    
    # Initialize chatbot
    chatbot = ChatbotManager()
    
    # Create a test session
    session_id = await create_new_session("test_user")
    print(f"Created test session: {session_id}")
    
    # Test queries - focusing on red dress
    test_queries = [
        "red dress"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        
        try:
            # Get chatbot response
            response = await chatbot.handle_text_query(
                session_id=session_id,
                query=query
            )
            
            print(f"Response: {response.response}")
            print(f"Products found: {len(response.products)}")
            
            # Display products
            if response.products:
                print("\nProducts:")
                for i, product in enumerate(response.products, 1):
                    print(f"  {i}. {product.get('name')} - ${product.get('price')}")
                    print(f"     Category: {product.get('category')}")
                    print(f"     Description: {product.get('description')[:100]}...")
            else:
                print("No products found.")
                
            print("-" * 60)
            
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
    
    print("\n=== COLOR SEARCH TEST COMPLETED ===\n")

if __name__ == "__main__":
    asyncio.run(test_color_search())