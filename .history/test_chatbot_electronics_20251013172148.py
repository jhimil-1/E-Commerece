import asyncio
from chatbot import ChatbotManager

async def test_chatbot():
    chatbot = ChatbotManager()
    
    print('Testing smartphone query...')
    response = await chatbot.process_message('show me smartphones', 'test_user')
    print(f'Response: {response}')
    
    print('\nTesting phone query...')
    response = await chatbot.process_message('show me phone', 'test_user')
    print(f'Response: {response}')
    
    print('\nTesting electronics query...')
    response = await chatbot.process_message('show me electronics', 'test_user')
    print(f'Response: {response}')

if __name__ == "__main__":
    asyncio.run(test_chatbot())