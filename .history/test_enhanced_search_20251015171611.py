import asyncio
import sys
sys.path.append('.')
from enhanced_product_handler import EnhancedProductHandler

async def test_search():
    handler = EnhancedProductHandler()
    try:
        # Test the search_products_enhanced method
        results = await handler.search_products_enhanced('earrings', 'test_user')
        print(f'Found {len(results)} products')
        for product in results[:3]:
            print(f'- {product.get("name", "No name")}: {product.get("category", "No category")}')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search())