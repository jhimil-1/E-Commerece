#!/usr/bin/env python3
"""
Test script to debug original product handler without enhanced filtering
"""
import asyncio
import logging
from product_handler import ProductHandler
from database import MongoDB

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_original_handler():
    """Test original product handler for phone queries"""
    
    # Create product handler
    product_handler = ProductHandler()
    
    # Test user ID
    test_user_id = "test_user_123"
    
    # Test various phone-related queries
    test_queries = [
        "Do you have any smartphones?",
        "Show me phones",
        "I need a new phone",
        "What mobile phones do you have?",
        "iPhone or Android phones",
        "Smartphone recommendations",
        "Cell phones available?",
        "Telephone options",
        "Phone accessories",
        "Mobile devices",
        "electronics"  # Test broad category
    ]
    
    print("\n" + "="*60)
    print("TESTING ORIGINAL PRODUCT HANDLER (NO ENHANCED FILTERING)")
    print("="*60 + "\n")
    
    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        try:
            # Process the query with original handler
            result = await product_handler.search_products(
                query=query,
                user_id=test_user_id,
                category="electronics",  # Try filtering by electronics
                limit=10
            )
            
            print(f"Status: {result['status']}")
            print(f"Message: {result.get('message', 'No message')}")
            
            if result['status'] == 'success':
                products = result['results']
                print(f"Products found: {len(products)}")
                
                if products:
                    for i, product in enumerate(products, 1):
                        name = product.get('name', 'Unknown')
                        category = product.get('category', 'Unknown')
                        price = product.get('price', 'N/A')
                        description = product.get('description', '')[:100]
                        score = product.get('score', 0.0)
                        
                        print(f"  {i}. {name} - {category} - ${price} (score: {score:.3f})")
                        if description:
                            print(f"     Desc: {description}...")
                        
                        # Check if it contains phone-related terms
                        if any(term in name.lower() or term in description.lower() for term in ['phone', 'smartphone', 'mobile', 'cell']):
                            print(f"     [CONTAINS PHONE-RELATED TERMS]")
                else:
                    print("  No products found")
            else:
                print(f"Error: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_original_handler())