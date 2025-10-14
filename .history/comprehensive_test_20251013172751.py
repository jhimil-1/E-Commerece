import asyncio
from chatbot import ChatbotManager
from database import MongoDB
from datetime import datetime

async def comprehensive_test():
    chatbot = ChatbotManager()
    
    # Create a valid session first
    sessions_collection = MongoDB.get_collection("sessions")
    test_session_id = "test_session_comprehensive_123"
    test_user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"  # Use a valid ObjectId from the database
    
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
    
    print(f'=== COMPREHENSIVE ENHANCED SEARCH TEST ===')
    print(f'Created test session: {test_session_id}')
    
    test_queries = [
        'show me smartphones',
        'show me phone', 
        'show me electronics',
        'show me dress',
        'show me shirt',
        'show me pant'
    ]
    
    for query in test_queries:
        print(f'\n--- Testing: {query} ---')
        try:
            response = await chatbot.handle_text_query(test_session_id, query)
            print(f'Products found: {len(response.products)}')
            if response.products:
                for i, product in enumerate(response.products[:3], 1):
                    print(f'  {i}. {product["name"]} ({product["category"]}) - Score: {product.get("enhanced_score", "N/A")}')
            print(f'Response preview: {response.response[:100]}...')
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(comprehensive_test())