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
    
    # Test 1: Basic jewelry search with ProductHandler
    print("\n1. Testing basic ProductHandler search for 'jewelry':")
    result1 = await product_handler.search_products(
        query="earrings",
        category="jewelry",
        limit=10,
        min_score=0.1
    )
    
    print(f"Status: {result1.get('status')}")
    print(f"Count: {result1.get('count', 0)}")
    print(f"Message: {result1.get('message', 'No message')}")
    
    if result1.get('results'):
        print("First few results:")
        for i, product in enumerate(result1['results'][:3]):
            print(f"  {i+1}. {product.get('name', 'Unknown')} - Category: {product.get('category', 'None')} - Score: {product.get('relevance_score', 0)}")
    
    # Test 2: Enhanced search
    print("\n2. Testing EnhancedProductHandler search for 'jewelry':")
    enhanced_handler = EnhancedProductHandler(product_handler)
    
    result2 = await enhanced_handler.search_products_enhanced(
        query="earrings",
        category="jewelry",
        limit=10,
        min_score=0.1
    )
    
    print(f"Status: {result2.get('status')}")
    print(f"Count: {result2.get('count', 0)}")
    print(f"Message: {result2.get('message', 'No message')}")
    
    if result2.get('results'):
        print("First few results:")
        for i, product in enumerate(result2['results'][:3]):
            print(f"  {i+1}. {product.get('name', 'Unknown')} - Category: {product.get('category', 'None')} - Score: {product.get('relevance_score', 0)}")
    
    # Test 3: Search without category filter
    print("\n3. Testing search without category filter:")
    result3 = await product_handler.search_products(
        query="earrings",
        limit=10,
        min_score=0.1
    )
    
    print(f"Status: {result3.get('status')}")
    print(f"Count: {result3.get('count', 0)}")
    
    if result3.get('results'):
        print("Jewelry results found:")
        jewelry_results = [p for p in result3['results'] if 'jewelry' in p.get('category', '').lower() or 'jewellery' in p.get('category', '').lower()]
        print(f"Found {len(jewelry_results)} jewelry items out of {result3.get('count', 0)} total")
        for i, product in enumerate(jewelry_results[:3]):
            print(f"  {i+1}. {product.get('name', 'Unknown')} - Category: {product.get('category', 'None')} - Score: {product.get('relevance_score', 0)}")

if __name__ == "__main__":
    asyncio.run(test_jewelry_search())