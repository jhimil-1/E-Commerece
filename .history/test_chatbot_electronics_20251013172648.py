import asyncio
from chatbot import ChatbotManager
from database import MongoDB
from datetime import datetime

async def test_chatbot():
    chatbot = ChatbotManager()
    
    # Create a valid session first
    sessions_collection = MongoDB.get_collection("sessions")
    test_session_id = "test_session_electronics_123"
    test_user_id = "test_user_electronics"
    
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
    
    print('Testing smartphone query...')
    response = await chatbot.handle_text_query(test_session_id, 'show me smartphones')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')
    
    print('\nTesting phone query...')
    response = await chatbot.handle_text_query(test_session_id, 'show me phone')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')
    
    print('\nTesting electronics query...')
    response = await chatbot.handle_text_query(test_session_id, 'show me electronics')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')

if __name__ == "__main__":
    asyncio.run(test_chatbot())