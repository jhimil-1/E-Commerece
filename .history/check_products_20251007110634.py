from database import MongoDB
import asyncio
from pymongo import MongoClient

async def check_products():
    db = MongoDB.get_db()
    
    # Count total products
    total_count = db.products.count_documents({})
    print(f'Total products: {total_count}')
    
    # Check a few products
    products = list(db.products.find().limit(3))
    for product in products:
        print(f'Product: {product.get(\"name\")}, Category: {product.get(\"category\")}, Created by: {product.get(\"created_by\")}')

if __name__ == "__main__":
    check_products()