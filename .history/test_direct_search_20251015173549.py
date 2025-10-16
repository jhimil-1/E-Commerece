import asyncio
import sys
sys.path.append('.')
from product_handler import ProductHandler

async def test_search():
    # Initialize product handler
    product_handler = ProductHandler()
    
    try:
        # Test the search_products method directly
        print("Testing direct search...")
        results = await product_handler.search_products(
            query='earrings',
            user_id='9ba7d438-2066-4466-991d-e4f78e728a78',
            category='jewelry',
            limit=10,
            min_score=0.1
        )
        
        print(f"Search results status: {results.get('status')}")
        print(f"Found {results.get('count', 0)} products")
        
        if results.get('results'):
            for product in results['results'][:3]:
                print(f"- {product.get('name', 'No name')}: {product.get('category', 'No category')} (Relevance: {product.get('relevance_score', 0):.1f})")
        else:
            print("No products found")
            
        print(f"Metadata: {results.get('metadata', {})}")
        
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test_search())