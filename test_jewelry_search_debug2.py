import asyncio
import logging
from product_handler import product_handler
from enhanced_product_handler import EnhancedProductHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_jewelry_search():
    """Test jewelry search with detailed debugging"""
    
    print("=== Testing Jewelry Search ===")
    
    # Test EnhancedProductHandler search
    print("\n1. Testing EnhancedProductHandler search for 'jewelry':")
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    result2 = await enhanced_handler.search_products_enhanced(
        query="earrings",
        category="jewelry",
        limit=10,
        min_relevance_score=0.1
    )
    
    print(f"Enhanced Handler Result Keys: {list(result2.keys())}")
    print(f"Status: {result2.get('status')}")
    print(f"Count: {result2.get('count', 0)}")
    print(f"Total Found: {result2.get('total_found', 'Not found')}")
    print(f"Message: {result2.get('message', 'No message')}")
    
    # Check different possible keys for products
    products_key = None
    if 'products' in result2:
        products_key = 'products'
    elif 'results' in result2:
        products_key = 'results'
    
    if products_key:
        products = result2.get(products_key, [])
        print(f"Found {len(products)} products using key '{products_key}'")
        
        if products:
            print("First few results:")
            for i, product in enumerate(products[:3]):
                print(f"  {i+1}. {product.get('name', 'Unknown')} - Category: {product.get('category', 'None')} - Score: {product.get('relevance_score', product.get('score', 0))}")
    else:
        print("No products found - checking search_metadata:")
        print(f"Search metadata: {result2.get('search_metadata', {})}")
    
    # Test 2: Try without category to see if that works
    print("\n2. Testing EnhancedProductHandler search without category:")
    result3 = await enhanced_handler.search_products_enhanced(
        query="earrings",
        limit=10,
        min_relevance_score=0.1
    )
    
    print(f"Without category - Status: {result3.get('status')}")
    print(f"Without category - Count: {result3.get('count', 0)}")
    print(f"Without category - Total Found: {result3.get('total_found', 'Not found')}")
    
    products_key = 'products' if 'products' in result3 else 'results' if 'results' in result3 else None
    if products_key:
        products = result3.get(products_key, [])
        print(f"Without category - Found {len(products)} products")
        if products:
            jewelry_products = [p for p in products if 'jewelry' in p.get('category', '').lower() or 'jewellery' in p.get('category', '').lower()]
            print(f"Without category - Found {len(jewelry_products)} jewelry products")

if __name__ == "__main__":
    asyncio.run(test_jewelry_search())