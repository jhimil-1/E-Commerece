from database import MongoDB
import asyncio

async def check_phone_products():
    mongodb = MongoDB()
    products = await mongodb.get_all_products()
    
    print(f'Total products in database: {len(products)}')
    print('\nProducts containing "phone" in name or description:')
    
    phone_products = []
    for product in products:
        name = product.get('name', '').lower()
        description = product.get('description', '').lower()
        
        if 'phone' in name or 'phone' in description or 'smartphone' in name or 'smartphone' in description:
            phone_products.append(product)
            print(f'  - {product["name"]}: {product.get("description", "")[:100]}...')
    
    if not phone_products:
        print('  No products found with "phone" or "smartphone" in name/description')
    
    print('\nAll product categories:')
    categories = {}
    for product in products:
        category = product.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
    
    for category, count in sorted(categories.items()):
        print(f'  - {category}: {count} products')

if __name__ == "__main__":
    asyncio.run(check_phone_products())