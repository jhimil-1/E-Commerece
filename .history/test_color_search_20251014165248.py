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
    
    # Test color-specific# Test queries
    test_queries = [
        "red dress"
    ]Non-color query for comparison
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
                for i, product in enumerate(response.products[:5], 1):
                    name = product.get('name', 'Unknown')
                    description = product.get('description', 'No description')
                    category = product.get('category', 'Unknown')
                    price = product.get('price', 'N/A')
                    
                    print(f"  {i}. {name} - ${price}")
                    print(f"     Category: {category}")
                    print(f"     Description: {description[:100]}...")
            else:
                print("No products found")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(test_color_search())