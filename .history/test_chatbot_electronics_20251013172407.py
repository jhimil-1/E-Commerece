import asyncio
from chatbot import ChatbotManager

async def test_chatbot():
    chatbot = ChatbotManager()
    
    print('Testing smartphone query...')
    response = await chatbot.handle_text_query('test_session_123', 'show me smartphones')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')
    
    print('\nTesting phone query...')
    response = await chatbot.handle_text_query('test_session_123', 'show me phone')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')
    
    print('\nTesting electronics query...')
    response = await chatbot.handle_text_query('test_session_123', 'show me electronics')
    print(f'Response: {response.response}')
    print(f'Products found: {len(response.products)}')

if __name__ == "__main__":
    asyncio.run(test_chatbot())