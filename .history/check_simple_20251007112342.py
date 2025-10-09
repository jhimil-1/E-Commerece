#!/usr/bin/env python3

from database import MongoDB

def check_products():
    db = MongoDB.get_db()
    products = list(db.products.find({'created_by': 'testuser1'}))
    print(f'testuser1 products: {len(products)}')
    for p in products:
        print(f'- {p["name"]} - Category: {p["category"]}')

if __name__ == "__main__":
    check_products()