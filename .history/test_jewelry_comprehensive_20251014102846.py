#!/usr/bin/env python3
"""
Comprehensive test for jewelry search functionality
Tests both "jewelry" and "jewellery" spellings with various scenarios
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from database import MongoDB
import uuid
from datetime import datetime, timezone

async def create_test_session():
    """Create a test session in MongoDB"""
    try:
        db = MongoDB.get_db()
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "user_id": "test_user",
            "created_at": datetime.now(timezone.utc),
            "last_activity": datetime.now(timezone.utc)
        }
        
        result = db.sessions.insert_one(session_data)
        if result.inserted_id:
            return session_id
        return None
    except Exception as e:
        print(f"Error creating test session: {e}")
        return None

async def test_jewelry_search():
    """Test jewelry search with comprehensive scenarios"""
    print("=== Comprehensive Jewelry Search Test ===\n")
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create test session
    session_id = await create_test_session()
    if not session_id:
        print("❌ Failed to create test session")
        return False
    
    print(f"✅ Created test session: {session_id}")
    
    # Test scenarios
    test_cases = [
        "show jewelry",
        "show jewellery", 
        "jewelry",
        "jewellery",
        "I want to see jewelry",
        "Do you have any jewellery?",
        "Show me some jewelry items",
        "What jewellery do you have?"
    ]
    
    all_passed = True
    results = []
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {query} ---")
        
        try:
            # Process the query
            response = await chatbot_manager.handle_text_query(session_id, query)
            
            if response and hasattr(response, 'products'):
                products = response.products if response.products else []
                count = len(products)
                
                if count > 0:
                    print(f"✅ Found {count} products")
                    # Show first few products
                    for j, product in enumerate(products[:3]):
                        name = product.get('name', 'Unknown')
                        category = product.get('category', 'Unknown')
                        price = product.get('price', 'Unknown')
                        print(f"  {j+1}. {name} - {category} (${price})")
                    
                    if count > 3:
                        print(f"  ... and {count - 3} more")
                    
                    results.append({
                        'query': query,
                        'status': 'success',
                        'count': count,
                        'products': products
                    })
                else:
                    print(f"❌ No products found")
                    results.append({
                        'query': query,
                        'status': 'no_products',
                        'count': 0
                    })
                    all_passed = False
            else:
                print(f"❌ Query failed: Invalid response format")
                results.append({
                    'query': query,
                    'status': 'failed',
                    'error': 'Invalid response format'
                })
                all_passed = False
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            results.append({
                'query': query,
                'status': 'exception',
                'error': str(e)
            })
            all_passed = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    successful_tests = sum(1 for r in results if r['status'] == 'success' and r['count'] > 0)
    total_tests = len(test_cases)
    
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    
    if all_passed and successful_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Jewelry search is working correctly.")
        return True
    else:
        print(f"\n❌ {total_tests - successful_tests} tests failed.")
        return False

async def main():
    success = await test_jewelry_search()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())