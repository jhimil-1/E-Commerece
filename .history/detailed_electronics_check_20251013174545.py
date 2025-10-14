from database import MongoDB
import json

def detailed_check():
    try:
        mongo = MongoDB()
        db = mongo.get_db()
        
        # Get all electronics products
        electronics_products = list(db.products.find({"category": "electronics"}))
        
        print(f"Total electronics products: {len(electronics_products)}")
        print("\nAll electronics products:")
        for i, product in enumerate(electronics_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Description: {product['description']}")
            print(f"   Category: {product['category']}")
            print()
        
        # Check for phone-related terms
        phone_terms = ['phone', 'smartphone', 'mobile', 'cell', 'telephone']
        phone_products = []
        
        for product in electronics_products:
            name_desc = f"{product['name']} {product['description']}".lower()
            if any(term in name_desc for term in phone_terms):
                phone_products.append(product)
        
        print(f"\nProducts containing phone-related terms: {len(phone_products)}")
        for product in phone_products:
            print(f"- {product['name']}: {product['description'][:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    detailed_check()