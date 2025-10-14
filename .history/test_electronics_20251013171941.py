import asyncio
from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def test_electronics():
    handler = ProductHandler()
    enhanced = EnhancedProductHandler(handler)
    
    print('Testing smartphone search...')
    result = await enhanced.search_products_enhanced('smartphone', limit=5)
    print(f'Found {result["count"]} products:')
    for product in result['results']:
        print(f'  - {product["name"]} ({product["category"]}) - Score: {product["enhanced_score"]:.3f}')
    
    print('\nTesting electronics search...')
    result = await enhanced.search_products_enhanced('electronics', limit=5)
    print(f'Found {result["count"]} products:')
    for product in result['results']:
        print(f'  - {product["name"]} ({product["category"]}) - Score: {product["enhanced_score"]:.3f}')
    
    print('\nTesting phone search...')
    result = await enhanced.search_products_enhanced('phone', limit=5)
    print(f'Found {result["count"]} products:')
    for product in result['results']:
        print(f'  - {product["name"]} ({product["category"]}) - Score: {product["enhanced_score"]:.3f}')

if __name__ == "__main__":
    asyncio.run(test_electronics())