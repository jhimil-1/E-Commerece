from database import MongoDB
import asyncio

async def check_products():
    await MongoDB.connect()
    db = MongoDB.get_database()
    
    # Count total products
    total_count = await db.products.count_documents({})
    print(f'Total products: {total_count}')
    
    # Check a few products
    products = await db.products.find().limit(3).to_list(None)
    for product in products:
        print(f'Product: {product.get("name")}, Category: {product.get("category")}, Created by: {product.get("created_by")}')

if __name__ == "__main__":
    asyncio.run(check_products())