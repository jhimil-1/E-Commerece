import asyncio
import sys
sys.path.append('.')
from product_handler import ProductHandler

async def test_search():
    # Initialize product handler
    product_handler = ProductHandler()
    
    try:
        # Test the search_products method directly with correct category
        print("Testing direct search with 'Jewellery' category...")
        results = await product_handler.search_products(
            query='earrings',
            user_id='9ba7d438-2066-4466-991d-e4f78e728a78',
            category='Jewellery',  # Correct spelling
            limit=10,
            min_score=0.1
        )
        
        print(f"Search results status: {results.get('status')}")
        print(f"Found {results.get('count', 0)} products")
        
        if results.get('results'):
            for product in results['results'][:5]:
                print(f"- {product.get('name', 'No name')}: {product.get('category', 'No category')} (Relevance: {product.get('relevance_score', 0):.1f})")
        else:
            print("No products found")
            
        print(f"Metadata: {results.get('metadata', {})}")
        
        # Test without category filter
        print("\nTesting without category filter...")
        results2 = await product_handler.search_products(
            query='earrings',
            user_id='9ba7d438-2066-4466-991d-e4f78e728a78',
            category=None,
            limit=10,
            min_score=0.1
        )
        
        print(f"Search results status: {results2.get('status')}")
        print(f"Found {results2.get('count', 0)} products")
        
        if results2.get('results'):
            for product in results2['results'][:5]:
                print(f"- {product.get('name', 'No name')}: {product.get('category', 'No category')} (Relevance: {product.get('relevance_score', 0):.1f})")
        else:
            print("No products found")
        
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test_search())