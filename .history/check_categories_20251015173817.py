from database import MongoDB

db = MongoDB.get_db()
user_id = '9ba7d438-2066-4466-991d-e4f78e728a78'

# Check categories for this user's products
products = list(db.products.find({'created_by': user_id}, {'name': 1, 'category': 1, 'created_by': 1}))
categories = set()
for product in products:
    categories.add(product.get('category', 'Unknown'))

print(f'Categories for user {user_id}:')
for category in sorted(categories):
    print(f'  - {category}')

# Check Qdrant categories
print('\nQdrant categories:')
from qdrant_utils import qdrant_manager

# Get all points for this user
from qdrant_client.http import models
search_results = qdrant_manager.client.search(
    collection_name=qdrant_manager.collection_name,
    query_vector=[0.0] * 512,  # Zero vector to get random results
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key='created_by',
                match=models.MatchValue(value=user_id)
            )
        ]
    ),
    limit=100
)

qdrant_categories = set()
for result in search_results:
    category = result.payload.get('category', 'Unknown')
    qdrant_categories.add(category)

for category in sorted(qdrant_categories):
    print(f'  - {category}')