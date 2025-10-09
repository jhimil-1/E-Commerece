from qdrant_utils import QdrantManager
import json

qdrant = QdrantManager()

# Search for all products
try:
    results = qdrant.search_products('', limit=20, min_score=0.0)
    print(f'Found {len(results)} products in Qdrant:')
    for i, result in enumerate(results[:5]):
        print(f'{i+1}. Name: {result.get("name", "N/A")}')
        print(f'   Category: {result.get("category", "N/A")}')
        print(f'   Price: {result.get("price", "N/A")}')
        print(f'   Image URL: {result.get("image_url", "N/A")}')
        print(f'   Image Path: {result.get("image_path", "N/A")}')
        print(f'   Image: {result.get("image", "N/A")}')
        print(f'   Created by: {result.get("created_by", "N/A")}')
        print('')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()