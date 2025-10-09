#!/usr/bin/env python3

from qdrant_utils import QdrantManager
from clip_utils import CLIPUtils
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant and CLIP
qdrant_manager = QdrantManager()
clip_utils = CLIPUtils()

# Generate embedding for 'smartphone' query
query_embedding = clip_utils.encode_text('smartphone')

# Search for similar products
results = qdrant_manager.search_similar_products(
    query_embedding=query_embedding,
    limit=5,
    min_score=0.1
)

print('Found products:')
for i, result in enumerate(results, 1):
    print(f"{i}. {result['name']} - {result['image_url']}")
    print(f"   Score: {result['score']:.4f}")
    print(f"   Category: {result['category']}")
    print()