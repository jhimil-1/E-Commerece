#!/usr/bin/env python3

from qdrant_utils import QdrantManager
from clip_utils import clip_manager
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant
qdrant_manager = QdrantManager()

# Generate embedding for 'gold diamond jewelry' query
query_embedding = clip_manager.get_text_embedding('gold diamond jewelry')

# Search for similar products
results = qdrant_manager.search_similar_products(
    query_embedding=query_embedding,
    limit=10,
    min_score=0.1
)

print('Found products:')
for i, result in enumerate(results, 1):
    print(f"{i}. {result['name']} - {result['image_url']}")
    print(f"   Score: {result['score']:.4f}")
    print(f"   Category: {result['category']}")
    print()