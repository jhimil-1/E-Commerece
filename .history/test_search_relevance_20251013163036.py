#!/usr/bin/env python3
"""
Test script to analyze search relevance issues
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_search_relevance():
    """Test search relevance for different queries"""
    
    # Initialize product handler
    product_handler = ProductHandler()
    
    # Test queries
    test_queries = [
        "pant",
        "pants",
        "trousers", 
        "jeans",
        "business professional dress",
        "dress",
        "formal dress"
    ]
    
    print("=== SEARCH RELEVANCE ANALYSIS ===\n")
    
    for query in test_queries:
        print(f"Testing query: '{query}'")
        print("-" * 50)
        
        try:
            # Get search results from product handler
            result = await product_handler.search_products(
                query=query,
                user_id=None,
                category=None,
                limit=10
            )
            
            if result['status'] == 'success':
                products = result['results']
                print(f"Found {len(products)} products")
                
                if products:
                    print("\nTop 5 results (sorted by relevance score):")
                    for i, product in enumerate(products[:5], 1):
                        name = product.get('name', 'Unknown')
                        category = product.get('category', 'Unknown')
                        score = product.get('similarity_score', 0)
                        match_pct = product.get('match_percentage', 0)
                        print(f"  {i}. {name} ({category}) - Score: {score:.3f} ({match_pct}%)")
                    
                    # Check if results are relevant
                    query_lower = query.lower()
                    relevant_count = 0
                    for product in products[:5]:
                        name_lower = product.get('name', '').lower()
                        category_lower = product.get('category', '').lower()
                        
                        # Simple relevance check
                        if (query_lower in name_lower or 
                            query_lower in category_lower or
                            any(word in name_lower for word in query_lower.split())):
                            relevant_count += 1
                    
                    print(f"\nRelevance: {relevant_count}/5 top results appear relevant")
                else:
                    print("No products found")
                    
            else:
                print(f"Search failed: {result['message']}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*50 + "\n")

async def test_embedding_similarity():
    """Test how similar different query embeddings are"""
    
    print("=== EMBEDDING SIMILARITY ANALYSIS ===\n")
    
    test_queries = ["pant", "pants", "trousers", "jeans", "dress", "business dress"]
    
    # Generate embeddings
    embeddings = {}
    for query in test_queries:
        try:
            embedding = clip_manager.get_text_embedding(query)
            embeddings[query] = embedding
            print(f"Generated embedding for '{query}': {len(embedding)} dimensions")
        except Exception as e:
            print(f"Failed to generate embedding for '{query}': {str(e)}")
    
    print("\nCosine similarity between queries:")
    print("-" * 40)
    
    # Calculate cosine similarities
    import numpy as np
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    for i, query1 in enumerate(test_queries):
        for query2 in test_queries[i+1:]:
            if query1 in embeddings and query2 in embeddings:
                sim = cosine_similarity(embeddings[query1], embeddings[query2])
                print(f"'{query1}' vs '{query2}': {sim:.3f}")

if __name__ == "__main__":
    print("Starting search relevance analysis...")
    
    # Run tests
    asyncio.run(test_search_relevance())
    print("\n" + "="*60 + "\n")
    asyncio.run(test_embedding_similarity())
    
    print("Analysis complete!")