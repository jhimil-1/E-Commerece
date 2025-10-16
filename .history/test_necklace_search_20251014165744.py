#!/usr/bin/env python3
"""
Test script for necklace image search functionality
"""

import asyncio
import sys
import os
import base64
from io import BytesIO
from PIL import Image
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

async def test_necklace_search():
    """Test the necklace image search functionality"""
    print("Initializing ChatbotManager...")
    chatbot = ChatbotManager()
    
    # Create a test session
    session_id = "test_necklace_search_session"
    
    # Test queries
    test_query = "show me necklaces"
    
    print(f"\nTesting query: '{test_query}'")
    response = await chatbot.handle_text_query(session_id, test_query)
    
    print("\nResponse:")
    print(response.get('message', 'No message'))
    
    if 'products' in response and response['products']:
        print(f"\nFound {len(response['products'])} products:")
        for i, product in enumerate(response['products']):
            print(f"{i+1}. {product.get('name')} - ${product.get('price')}")
            print(f"   {product.get('description')}")
    else:
        print("No products found")
    
    # Test image search for necklaces
    print("\nTesting image search for necklaces...")
    
    # Simulate an image search (in a real scenario, you would use an actual image)
    # For testing, we'll use a text query with the image search endpoint
    image_query_response = await chatbot.handle_text_query(
        session_id, 
        "find necklaces like this image", 
        category="necklaces"
    )
    
    print("\nImage Search Response:")
    print(image_query_response.get('message', 'No message'))
    
    if 'products' in image_query_response and image_query_response['products']:
        print(f"\nFound {len(image_query_response['products'])} products:")
        for i, product in enumerate(image_query_response['products']):
            print(f"{i+1}. {product.get('name')} - ${product.get('price')}")
            print(f"   {product.get('description')}")
    else:
        print("No products found in image search")

if __name__ == "__main__":
    asyncio.run(test_necklace_search())