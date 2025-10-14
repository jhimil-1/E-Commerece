from database import MongoDB
import re

def comprehensive_phone_search():
    try:
        mongo = MongoDB()
        db = mongo.get_db()
        
        # Search for phone-related terms in ALL products
        phone_patterns = [
            r'phone', r'smartphone', r'mobile', r'cell', r'telephone',
            r'iphone', r'samsung', r'pixel', r'android', r'ios'
        ]
        
        all_phone_products = []
        
        for pattern in phone_patterns:
            regex_pattern = re.compile(pattern, re.IGNORECASE)
            matches = list(db.products.find({
                "$or": [
                    {"name": regex_pattern},
                    {"description": regex_pattern}
                ]
            }))
            all_phone_products.extend(matches)
        
        # Remove duplicates
        seen_ids = set()
        unique_phone_products = []
        for product in all_phone_products:
            if product['_id'] not in seen_ids:
                seen_ids.add(product['_id'])
                unique_phone_products.append(product)
        
        print(f"Found {len(unique_phone_products)} products matching phone-related terms:")
        for i, product in enumerate(unique_phone_products, 1):
            print(f"{i}. {product['name']} (Category: {product['category']})")
            print(f"   Description: {product['description'][:150]}...")
            print()
        
        # Also check if there are any products with "phone" in category
        all_categories = db.products.distinct("category")
        print(f"All categories in database: {all_categories}")
        
        # Check each category for phone-related terms
        for category in all_categories:
            category_products = list(db.products.find({"category": category}))
            phone_matches = []
            for product in category_products:
                name_desc = f"{product['name']} {product['description']}".lower()
                if any(term in name_desc for term in ['phone', 'smartphone', 'mobile']):
                    phone_matches.append(product)
            
            if phone_matches:
                print(f"\nPhones found in category '{category}': {len(phone_matches)}")
                for product in phone_matches:
                    print(f"  - {product['name']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    comprehensive_phone_search()