import asyncio
import sys
sys.path.append('.')
from enhanced_product_handler import EnhancedProductHandler
from product_handler import ProductHandler

async def test_search():
    # Initialize product handler (it gets db internally)
    product_handler = ProductHandler()
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    try:
        # Test the search_products_enhanced method with a real user
        results = await enhanced_handler.search_products_enhanced('earrings', '9ba7d438-2066-4466-991d-e4f78e728a78')
        if isinstance(results, dict) and 'results' in results:
            products = results['results']
            print(f'Found {len(products)} products')
            for product in products[:3]:
                print(f'- {product.get("name", "No name")}: {product.get("category", "No category")}')
        elif isinstance(results, list):
            print(f'Found {len(results)} products')
            for product in results[:3]:
                print(f'- {product.get("name", "No name")}: {product.get("category", "No category")}')
        else:
            print('No products found or unexpected result format')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search())