#!/usr/bin/env python3
"""
Enhanced Product Handler with improved search relevance
"""

print("ENHANCED_PRODUCT_HANDLER MODULE LOADED")

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class EnhancedProductHandler:
    """Enhanced product handler with semantic relevance filtering"""
    
    def __init__(self, product_handler):
        """Initialize with existing product handler"""
        self.product_handler = product_handler
        self.db = product_handler.db
        self.min_relevance_score = 0.7  # Higher threshold for relevance
        
    def calculate_semantic_relevance(self, query: str, product: Dict[str, Any]) -> float:
        """
        Calculate semantic relevance score between query and product
        Returns score from 0.0 to 1.0
        """
        query_lower = query.lower().strip()
        product_name = product.get('name', '').lower()
        product_desc = product.get('description', '').lower()
        product_category = product.get('category', '').lower()
        
        # Debug output for headphones calculation
        if 'headphones' in query_lower:
            print(f"DEBUG SEMANTIC: Calculating relevance for '{product_name}' in category '{product_category}'")
        
        # Exact match bonuses
        exact_name_match = query_lower in product_name
        exact_desc_match = query_lower in product_desc
        exact_category_match = query_lower in product_category
        
        # Word-level matching
        query_words = set(query_lower.split())
        name_words = set(product_name.split())
        desc_words = set(product_desc.split())
        category_words = set(product_category.split())
        
        # Calculate word overlap
        name_overlap = len(query_words.intersection(name_words)) / max(len(query_words), 1)
        desc_overlap = len(query_words.intersection(desc_words)) / max(len(query_words), 1)
        category_overlap = len(query_words.intersection(category_words)) / max(len(query_words), 1)
        
        # Category-specific relevance scoring
        category_scores = {
            'pant': {
                'clothing': 1.0, 'pants': 1.0, 'jeans': 1.0, 'trousers': 1.0,
                'joggers': 0.9, 'leggings': 0.8, 'shorts': 0.7
            },
            'dress': {
                'clothing': 1.0, 'dress': 1.0, 'gown': 1.0, 'frock': 1.0
            },
            'shirt': {
                'clothing': 1.0, 'shirt': 1.0, 'top': 1.0, 'blouse': 1.0
            },
            'smartphone': {
                'electronics': 1.0, 'phone': 1.0, 'smartphone': 1.0, 'mobile': 1.0
            },
            'phone': {
                'electronics': 1.0, 'phone': 1.0, 'smartphone': 1.0, 'mobile': 1.0,
                'camera': 0.8, 'webcam': 0.7, 'dash cam': 0.6
            },
            'headphones': {
                'electronics': 1.0, 'headphones': 1.0, 'headphone': 1.0, 'earbuds': 1.0, 'earphone': 1.0,
                'audio': 0.9, 'wireless': 0.8, 'bluetooth': 0.8, 'noise cancelling': 0.9
            },
            'electronics': {
                'electronics': 1.0, 'electronic': 1.0, 'tech': 0.9, 'gadget': 0.9,
                'smart': 0.8, 'digital': 0.8, 'wifi': 0.7, 'bluetooth': 0.7
            },
            'jewelry': {
                'jewelry': 1.0, 'jewellery': 1.0, 'earrings': 1.0, 'necklace': 1.0, 
                'bracelet': 1.0, 'ring': 1.0, 'watch': 0.8, 'pendant': 1.0, 
                'chain': 0.9, 'accessories': 0.7
            },
            'jewellery': {
                'jewelry': 1.0, 'jewellery': 1.0, 'jewellry': 1.0, 'earrings': 1.0, 
                'necklace': 1.0, 'bracelet': 1.0, 'ring': 1.0, 'watch': 0.8, 'pendant': 1.0, 
                'chain': 0.9, 'accessories': 0.7
            }
        }
        
        # Base relevance score
        relevance_score = 0.0
        
        # Exact matches get highest scores
        if exact_name_match:
            relevance_score += 0.8
        if exact_desc_match:
            relevance_score += 0.4
        if exact_category_match:
            relevance_score += 0.3
            
        # Word overlap scores
        relevance_score += name_overlap * 0.6
        relevance_score += desc_overlap * 0.3
        relevance_score += category_overlap * 0.2
        
        # Category-specific scoring
        # Special handling for headphones - check this first to avoid conflicts
        if 'headphones' in query_lower or 'headphone' in query_lower or 'earbuds' in query_lower or 'earphone' in query_lower:
            product_cat = product_category.lower()
            if product_cat == 'electronics':
                # Only give bonus if product name contains headphones-related terms
                product_name_lower = product.get('name', '').lower()
                if any(term in product_name_lower for term in ['headphone', 'earbuds', 'earphone']):
                    relevance_score += 0.5  # Full bonus for actual headphones
                    if 'headphones' in query_lower:
                        print(f"DEBUG SEMANTIC: Headphones product found! Adding 0.5 bonus")
                else:
                    # NO bonus for other electronics when searching for headphones
                    if 'headphones' in query_lower:
                        print(f"DEBUG SEMANTIC: Non-headphones electronics, adding 0.0 bonus")
                    relevance_score += 0.0
            elif 'clothing' in product_cat:
                relevance_score += 0.3  # General clothing bonus
                if 'headphones' in query_lower:
                    print(f"DEBUG SEMANTIC: Clothing bonus: 0.3")
        else:
            # Regular category scoring for non-headphones queries
            for keyword, categories in category_scores.items():
                if keyword in query_lower:
                    product_cat = product_category.lower()
                    if product_cat in categories:
                        relevance_score += categories[product_cat] * 0.5
                        if 'headphones' in query_lower:
                            print(f"DEBUG SEMANTIC: Regular category bonus: {categories[product_cat] * 0.5}")
                    elif 'clothing' in product_cat:
                        relevance_score += 0.3  # General clothing bonus
                        if 'headphones' in query_lower:
                            print(f"DEBUG SEMANTIC: Clothing bonus: 0.3")
                    
        # Penalize obviously wrong categories (but be more lenient on broad terms)
        wrong_category_penalties = {
            'pant': ['electronics', 'home', 'kitchen', 'appliance'],
            'dress': ['electronics', 'home', 'kitchen', 'appliance'],
            'shirt': ['electronics', 'home', 'kitchen', 'appliance'],
            'smartphone': ['clothing', 'jewelry', 'home', 'kitchen'],
            'phone': ['clothing', 'jewelry', 'home', 'kitchen']
        }
        
        # Don't penalize broad electronics queries as harshly
        if any(broad_term in query_lower for broad_term in ['electronics', 'tech', 'gadget']):
            penalty_weight = 0.2  # Lighter penalty for broad terms
        else:
            penalty_weight = 0.5  # Standard penalty for specific mismatches
            
        for keyword, wrong_cats in wrong_category_penalties.items():
            if keyword in query_lower and product_category in wrong_cats:
                relevance_score -= penalty_weight  # Adjusted penalty for wrong category
                
        if 'headphones' in query_lower:
            print(f"DEBUG SEMANTIC: Final relevance score for '{product_name}': {relevance_score}")
        
        return min(relevance_score, 1.0)  # Cap at 1.0
    
    def filter_irrelevant_results(self, query: str, products: List[Dict[str, Any]], 
                                 min_semantic_score: float = None) -> List[Dict[str, Any]]:
        """
        Filter out irrelevant products based on semantic analysis
        """
        print(f"FILTER_IRRELEVANT_RESULTS: ENTERING METHOD!")
        print(f"🎯 FILTER CALLED: filter_irrelevant_results with query: '{query}', min_semantic_score: {min_semantic_score}")
        print(f"🎯 FILTER CALLED: Number of products to filter: {len(products)}")
        print(f"🎯 THRESHOLDS: min_relevance_score={self.min_relevance_score}")
        # Set default minimum semantic score based on query type
        query_lower = query.lower()
        print(f"DEBUG: Setting min_semantic_score for query: '{query}' (lower: '{query_lower}')")
        print(f"DEBUG: Checking headphones words in query: 'headphones' in '{query_lower}' = {'headphones' in query_lower}")
        print(f"DEBUG: Checking headphones words in query: 'headphone' in '{query_lower}' = {'headphone' in query_lower}")
        print(f"DEBUG: Checking headphones words in query: 'earbuds' in '{query_lower}' = {'earbuds' in query_lower}")
        print(f"DEBUG: Checking headphones words in query: 'earphone' in '{query_lower}' = {'earphone' in query_lower}")
        
        if min_semantic_score is None:
            # Special handling for specific product queries
            headphones_words = ['headphones', 'headphone', 'earbuds', 'earphone']
            if any(word in query_lower for word in headphones_words):
                # For headphones queries, require higher semantic relevance to avoid showing other electronics
                min_semantic_score = 0.8  # Very high threshold - only allow actual headphones with very high semantic scores
                print(f"DEBUG: Headphones detected! Words found: {[word for word in headphones_words if word in query_lower]}")
            elif any(word in query_lower for word in ['phone', 'smartphone', 'mobile', 'cell', 'telephone']):
                # For specific phone queries, be more lenient with electronics but still filter obvious mismatches
                min_semantic_score = 0.05  # Very low threshold - mainly filter by vector score
                print(f"DEBUG: Phone detected, setting min_semantic_score to 0.05")
            elif any(word in query_lower for word in ['electronics', 'tech', 'gadget']):
                # For broad electronics queries, be quite lenient
                min_semantic_score = 0.02  # Very low threshold for broad electronics
                print(f"DEBUG: Electronics detected, setting min_semantic_score to 0.02")
            elif any(word in query_lower for word in ['jewelry', 'jewellery', 'jewellry', 'earrings', 'necklace', 'bracelet', 'ring']):
                # For jewelry queries, be more lenient to allow jewelry-related items
                min_semantic_score = 0.1  # Lower threshold for jewelry queries
                print(f"DEBUG: Jewelry detected, setting min_semantic_score to 0.1")
            else:
                # Standard threshold for clothing/jewelry
                min_semantic_score = 0.3
                print(f"DEBUG: No specific category detected, setting min_semantic_score to 0.3")
            
            print(f"DEBUG: Final min_semantic_score set to: {min_semantic_score}")
        
        filtered_products = []
        
        for product in products:
            # Calculate semantic relevance
            semantic_score = self.calculate_semantic_relevance(query, product)
            
            # Get the vector similarity score
            vector_score = product.get('similarity_score', 0.0)
            
            # Combined score (weighted average)
            combined_score = (vector_score * 0.7) + (semantic_score * 0.3)
            
            # Special logic for phone queries: if it's electronics and has decent vector score, allow it
            product_category = product.get('category', '').lower()
            is_electronics = product_category == 'electronics'
            is_jewelry = product_category == 'jewelry'
            has_decent_vector = vector_score >= self.min_relevance_score * 0.5  # Lower vector threshold for electronics
            
            # For phone queries, prioritize vector score over semantic score for electronics
            if any(word in query_lower for word in ['phone', 'smartphone', 'mobile', 'cell', 'telephone']):
                if is_electronics and has_decent_vector:
                    # Allow electronics products with decent vector scores for phone queries
                    product['enhanced_score'] = combined_score
                    product['semantic_relevance'] = semantic_score
                    filtered_products.append(product)
                    continue
            
            # For jewelry queries, prioritize vector score over semantic score for jewelry
            if any(word in query_lower for word in ['jewelry', 'jewellery', 'jewellry', 'earrings', 'necklace', 'bracelet', 'ring']):
                if is_jewelry and has_decent_vector:
                    # Allow jewelry products with decent vector scores for jewelry queries
                    product['enhanced_score'] = combined_score
                    product['semantic_relevance'] = semantic_score
                    filtered_products.append(product)
                    continue
            
            # Special handling for headphones queries - prioritize semantic relevance
            if 'headphones' in query_lower or 'headphone' in query_lower or 'earbuds' in query_lower or 'earphone' in query_lower:
                print(f"🎯 HEADPHONES DETECTED: Processing {product.get('name', 'Unknown')} with semantic score: {semantic_score}")
                # For headphones, semantic score is more important than vector score
                print(f"🎯 FILTER CHECK: {product.get('name', 'Unknown')} - semantic: {semantic_score} vs {min_semantic_score}, vector: {vector_score} vs {self.min_relevance_score * 0.5}")
                if semantic_score >= min_semantic_score and vector_score >= self.min_relevance_score * 0.5:
                    # Update the product with enhanced scores
                    product['enhanced_score'] = combined_score
                    product['semantic_relevance'] = semantic_score
                    filtered_products.append(product)
                    logger.debug(f"HEADPHONES PASSED: {product.get('name', 'Unknown')} "
                               f"(vector: {vector_score:.3f}, semantic: {semantic_score:.3f}, "
                               f"combined: {combined_score:.3f})")
                    print(f"✅ FILTER PASSED: {product.get('name', 'Unknown')}")
                else:
                    print(f"❌ FILTER FAILED: {product.get('name', 'Unknown')} - semantic too low: {semantic_score} < {min_semantic_score}")
                    print(f"❌ FILTER FAILED: {product.get('name', 'Unknown')} - vector too low: {vector_score} < {self.min_relevance_score * 0.5}")
            # Standard filtering for other queries
            elif vector_score >= self.min_relevance_score and semantic_score >= min_semantic_score:
                # Update the product with enhanced scores
                product['enhanced_score'] = combined_score
                product['semantic_relevance'] = semantic_score
                filtered_products.append(product)
                logger.debug(f"PASSED: {product.get('name', 'Unknown')} "
                           f"(vector: {vector_score:.3f}, semantic: {semantic_score:.3f}, "
                           f"min_vector: {self.min_relevance_score}, min_semantic: {min_semantic_score})")
            else:
                logger.debug(f"Filtered out: {product.get('name', 'Unknown')} "
                           f"(vector: {vector_score:.3f}, semantic: {semantic_score:.3f}, "
                           f"min_vector: {self.min_relevance_score}, min_semantic: {min_semantic_score})")
            
            # Add a debug statement to show what min_semantic_score is being used
            print(f"DEBUG: Query: '{query_lower}', checking for headphones words: {['headphones', 'headphone', 'earbuds', 'earphone']}")
            print(f"DEBUG: 'headphones' in query: {'headphones' in query_lower}")
            print(f"DEBUG: 'headphone' in query: {'headphone' in query_lower}")
            print(f"DEBUG: 'earbuds' in query: {'earbuds' in query_lower}")
            print(f"DEBUG: 'earphone' in query: {'earphone' in query_lower}")
            
            if 'headphones' in query_lower or 'headphone' in query_lower or 'earbuds' in query_lower or 'earphone' in query_lower:
                print(f"DEBUG: Headphones word found in query! Current min_semantic: {min_semantic_score}")
            else:
                print(f"DEBUG: No headphones words found. Current min_semantic: {min_semantic_score}")
        
        # Sort by combined score
        filtered_products.sort(key=lambda x: x.get('enhanced_score', 0), reverse=True)
        
        return filtered_products
    
    async def search_products_enhanced(self, query: str, user_id: str = None, 
                                     category: str = None, limit: int = 10) -> Dict[str, Any]:
        """
        Enhanced search with semantic relevance filtering
        """
        print(f"🚀 ENHANCED_SEARCH: Starting search for query: '{query}'")
        print(f"🚀 ENHANCED_SEARCH: Current instance min_relevance_score: {self.min_relevance_score}")
        logger.info(f"Enhanced search: '{query}' (category: {category}, user: {user_id})")
        
        # First, get results from the original product handler
        result = await self.product_handler.search_products(
            query=query,
            user_id=user_id,
            category=category,
            limit=50  # Get more results to filter
        )
        
        if result['status'] != 'success':
            return result
            
        products = result['results']
        
        if not products:
            return {
                "status": "success",
                "message": "No matching products found",
                "results": [],
                "metadata": {
                    "filtered_by_semantic": True,
                    "original_count": 0,
                    "filtered_count": 0
                }
            }
        
        logger.info(f"Found {len(products)} products, applying semantic filtering...")
        
        # Apply semantic filtering
        print(f"🚀 ABOUT TO FILTER: Calling filter_irrelevant_results with {len(products)} products")
        print(f"🚀 CALLING FILTER: Method exists? {hasattr(self, 'filter_irrelevant_results')}")
        filtered_products = self.filter_irrelevant_results(query, products, min_semantic_score=None)
        print(f"🚀 FILTER RESULT: Got {len(filtered_products)} products after filtering")
        
        logger.info(f"Semantic filtering: {len(products)} -> {len(filtered_products)} products")
        
        # Apply final limit
        filtered_products = filtered_products[:limit]
        
        # Update metadata
        for product in filtered_products:
            if 'metadata' not in product:
                product['metadata'] = {}
            product['metadata']['semantic_filtered'] = True
            product['metadata']['original_score'] = product.get('similarity_score', 0)
        
        return {
            "status": "success",
            "count": len(filtered_products),
            "query": query,
            "category": category,
            "results": filtered_products,
            "metadata": {
                "has_query": bool(query),
                "has_image": False,
                "filtered_by_category": bool(category),
                "filtered_by_semantic": True,
                "original_count": len(products),
                "filtered_count": len(filtered_products),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        }