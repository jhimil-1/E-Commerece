import asyncio
from chatbot import ChatbotManager
from database import MongoDB
from datetime import datetime

async def test_similar_products():
    """Test how chatbot handles 'similar product' queries"""
    
    chatbot = ChatbotManager()
    
    # Create a valid session
    sessions_collection = MongoDB.get_collection("sessions")
    test_session_id = "test_session_similar_123"
    test_user_id = "test_user_similar"
    
    # Create session
    sessions_collection.update_one(
        {"session_id": test_session_id},
        {
            "$set": {
                "user_id": test_user_id,
                "created_at": datetime.utcnow(),
                "last_activity": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    print(f'Created test session: {test_session_id}')
    
    # Test various "similar" queries
    test_queries = [
        "show me similar products",
        "similar product",
        "find similar items",
        "what else is similar",
        "show me something similar to what I was looking at",
        "recommend similar products"
    ]
    
    print('\n=== TESTING SIMILAR PRODUCT QUERIES ===\n')
    
    for query in test_queries:
        print(f'Query: "{query}"')
        print("-" * 50)
        
        try:
            response = await chatbot.handle_text_query(test_session_id, query)
            print(f'Response: {response.response}')
            print(f'Products found: {len(response.products)}')
            
            if response.products:
                print("Products found:")
                for i, product in enumerate(response.products[:3], 1):
                    name = product.get('name', 'Unknown')
                    category = product.get('category', 'Unknown')
                    print(f"  {i}. {name} ({category})")
            
        except Exception as e:
            print(f'Error: {str(e)}')
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(test_similar_products())