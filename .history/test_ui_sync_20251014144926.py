#!/usr/bin/env python3

import sys
import asyncio
import time
sys.path.append('.')

from chatbot import ChatbotManager
from auth import create_new_session

async def test_ui_sync_issue():
    """Test to reproduce the UI sync issue between text and products"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a test session
    session_id = await create_new_session("test_user_123")
    print(f"Created session: {session_id}")
    
    print("\n=== TESTING UI SYNC ISSUE ===\n")
    
    # Test sequence that might cause the issue
    test_sequence = [
        "show me necklaces",  # Should show necklaces
        "show me watches",    # Should show watches
        "show me similar products"  # Should show similar to watches
    ]
    
    for i, query in enumerate(test_sequence, 1):
        print(f"Step {i}: {query}")
        print("-" * 40)
        
        try:
            response = await chatbot_manager.handle_text_query(session_id, query)
            
            print(f"Text Response: {response.response}")
            print(f"Products found: {len(response.products)}")
            
            if response.products:
                print("Products in response:")
                for j, product in enumerate(response.products[:3], 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    print(f"  {j}. {name} ({category})")
                    
                # Check if text matches products
                product_names = [p.get('name', '').lower() for p in response.products]
                response_text = response.response.lower()
                
                # Check for mismatches
                text_mentions_necklace = 'necklace' in response_text
                text_mentions_watch = 'watch' in response_text
                
                products_are_necklaces = any('necklace' in name for name in product_names)
                products_are_watches = any('watch' in name for name in product_names)
                
                if (text_mentions_necklace and not products_are_necklaces) or \
                   (text_mentions_watch and not products_are_watches):
                    print("⚠️  POTENTIAL MISMATCH DETECTED!")
                    print(f"   Text mentions necklace: {text_mentions_necklace}")
                    print(f"   Text mentions watch: {text_mentions_watch}")
                    print(f"   Products are necklaces: {products_are_necklaces}")
                    print(f"   Products are watches: {products_are_watches}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*60 + "\n")
        
        # Small delay to simulate user interaction time
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("Starting UI sync test...")
    asyncio.run(test_ui_sync_issue())
    print("Test completed!")