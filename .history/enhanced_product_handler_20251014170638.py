#!/usr/bin/env python3
"""
Enhanced Product Handler with Targeted Search Filtering
Ensures only the most relevant products are returned for specific queries
"""

import re
import numpy as np
from typing import List, Dict, Any, Optional, Union
from product_handler import ProductHandler
from qdrant_utils import QdrantManager
import logging

logger = logging.getLogger(__name__)

class EnhancedProductHandler:
    """Enhanced product handler with targeted filtering"""
    
    def __init__(self, base_handler: ProductHandler):
        self.base_handler = base_handler
        self.qdrant = QdrantManager()
        
        # Define category-specific keywords for better filtering
        self.category_keywords = {
            'jewelry': {
                'primary': ['necklace', 'necklaces', 'pendant', 'chain', 'jewelry', 'jewellery'],
                'specific': ['diamond', 'gold', 'silver', 'pearl', 'ring', 'earring', 'bracelet', 'watch'],
                'min_score': 0.7  # Higher threshold for jewelry
            },
            'clothing': {
                'primary': ['dress', 'dresses', 'shirt', 'pants', 'jeans', 'clothing', 'apparel', 'wear'],
                'specific': ['women', 'men', 'casual', 'formal', 'summer', 'winter'],
                'min_score': 0.6
            },
            'electronics': {
                'primary': ['phone', 'smartphone', 'laptop', 'computer', 'electronics', 'device'],
                'specific': ['apple', 'samsung', 'wireless', 'bluetooth', 'smart'],
                'min_score': 0.65
            }
        }
        
        # Enhanced query understanding
        self.query_patterns = {
            'exact_match': r'\b(gold|silver|diamond|pearl)\s+(necklace|ring|earring|bracelet)\b',
            'type_specific': r'\b(necklace|necklaces|pendant|chain)\b',
            'material_specific': r'\b(gold|silver|diamond|pearl)\b',
            'gender_specific': r'\b(women|men|women\'s|men\'s)\b',
            'color_specific': r'\b(red|blue|green|black|white|yellow|purple|pink|orange|brown)\b'
        }
        
        # Color keywords for color-based filtering
        self.color_keywords = {
            'red': ['red', 'crimson', 'scarlet', 'maroon', 'burgundy', 'ruby'],
            'blue': ['blue', 'navy', 'azure', 'teal', 'turquoise', 'cyan'],
            'green': ['green', 'emerald', 'lime', 'olive', 'mint'],
            'black': ['black', 'onyx', 'ebony', 'charcoal'],
            'white': ['white', 'ivory', 'cream', 'pearl', 'off-white'],
            'yellow': ['yellow', 'gold', 'amber', 'mustard'],
            'purple': ['purple', 'violet', 'lavender', 'plum', 'mauve'],
            'pink': ['pink', 'rose', 'fuchsia', 'magenta', 'salmon'],
            'orange': ['orange', 'coral', 'peach', 'amber'],
            'brown': ['brown', 'tan', 'beige', 'khaki', 'caramel']
        }
    
    def calculate_semantic_relevance(self, query: str, product: Dict[str, Any]) -> float:
        """Calculate semantic relevance score between query and product"""
        query_lower = query.lower()
        product_name = product.get('name', '').lower()
        product_description = product.get('description', '').lower()
        product_category = product.get('category', '').lower()
        
        # Start with base similarity score
        relevance_score = product.get('similarity_score', 0.0)
        
        # Exact match bonus
        if query_lower in product_name:
            relevance_score += 0.3
        elif any(word in product_name for word in query_lower.split()):
            relevance_score += 0.2
        
        # Category-specific scoring
        for category, keywords in self.category_keywords.items():
            if product_category == category:
                # Check for primary keywords
                primary_matches = sum(1 for keyword in keywords['primary'] if keyword in query_lower)
                if primary_matches > 0:
                    relevance_score += 0.15 * primary_matches
                
                # Check for specific keywords
                specific_matches = sum(1 for keyword in keywords['specific'] if keyword in query_lower)
                if specific_matches > 0:
                    relevance_score += 0.1 * specific_matches
                
                # Pattern matching
                for pattern_name, pattern in self.query_patterns.items():
                    if re.search(pattern, query_lower) and re.search(pattern, product_name):
                        relevance_score += 0.25
        
        # Color-based relevance scoring
        color_match_found = False
        for color, synonyms in self.color_keywords.items():
            # Check if color is mentioned in query
            if any(color_term in query_lower for color_term in synonyms):
                # Check if same color is in product name or description
                if any(color_term in product_name or color_term in product_description for color_term in synonyms):
                    relevance_score += 0.4  # Significant boost for color match
                    color_match_found = True
                    break
        
        # If color was in query but not found in product, penalize the score
        if not color_match_found and re.search(self.query_patterns['color_specific'], query_lower):
            relevance_score -= 0.3  # Penalize products that don't match the requested color
        
        # Description relevance
        if query_lower in product_description:
            relevance_score += 0.15
        
        # Normalize score
        relevance_score = min(relevance_score, 1.0)
        relevance_score = max(relevance_score, 0.0)  # Ensure score doesn't go negative
        
        return relevance_score
    
    def filter_irrelevant_results(self, query: str, results: List[Dict[str, Any]], 
                                min_relevance_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """Filter out irrelevant results based on query analysis"""
        if not results:
            return results
        
        query_lower = query.lower()
        
        # Determine minimum relevance threshold based on query specificity
        if min_relevance_threshold is None:
            min_relevance_threshold = self._determine_min_threshold(query)
        
        # Calculate relevance scores
        scored_results = []
        for product in results:
            relevance_score = self.calculate_semantic_relevance(query, product)
            scored_results.append({
                'product': product,
                'relevance_score': relevance_score
            })
        
        # Filter by relevance threshold
        filtered_results = [
            item['product'] for item in scored_results 
            if item['relevance_score'] >= min_relevance_threshold
        ]
        
        # If too few results, relax threshold slightly
        if len(filtered_results) < 2 and min_relevance_threshold > 0.4:
            relaxed_threshold = min_relevance_threshold - 0.1
            filtered_results = [
                item['product'] for item in scored_results 
                if item['relevance_score'] >= relaxed_threshold
            ]
        
        # Sort by relevance score
        filtered_results.sort(key=lambda x: self.calculate_semantic_relevance(query, x), reverse=True)
        
        logger.info(f"Filtered {len(results)} results to {len(filtered_results)} relevant products for query '{query}' (threshold: {min_relevance_threshold:.2f})")
        
        return filtered_results
    
    def _determine_min_threshold(self, query: str) -> float:
        """Determine minimum relevance threshold based on query characteristics"""
        query_lower = query.lower()
        
        # Very specific queries get higher thresholds
        if re.search(self.query_patterns['exact_match'], query_lower):
            return 0.8
        elif re.search(self.query_patterns['type_specific'], query_lower):
            return 0.75
        elif re.search(self.query_patterns['material_specific'], query_lower):
            return 0.7
        elif re.search(self.query_patterns['gender_specific'], query_lower):
            return 0.65
        else:
            return 0.6  # Default threshold
    
    def extract_product_type_from_query(self, query: str) -> Optional[str]:
        """Extract specific product type from query"""
        query_lower = query.lower()
        
        # Jewelry-specific extraction
        jewelry_types = ['necklace', 'necklaces', 'pendant', 'chain', 'ring', 'earring', 'bracelet', 'watch']
        for jewelry_type in jewelry_types:
            if jewelry_type in query_lower:
                return jewelry_type
        
        # Clothing-specific extraction
        clothing_types = ['dress', 'dresses', 'shirt', 'pants', 'jeans', 'skirt', 'jacket']
        for clothing_type in clothing_types:
            if clothing_type in query_lower:
                return clothing_type
        
        # Electronics-specific extraction
        electronics_types = ['phone', 'smartphone', 'laptop', 'computer', 'tablet', 'headphones']
        for electronics_type in electronics_types:
            if electronics_type in query_lower:
                return electronics_type
        
        return None
        
    def extract_color_from_query(self, query: str) -> Optional[str]:
        """Extract color information from query"""
        query_lower = query.lower()
        
        # Check for color terms in query
        for color, synonyms in self.color_keywords.items():
            if any(color_term in query_lower for color_term in synonyms):
                return color
                
        return None
    
    async def search_products(self, 
                            query: Optional[str] = None,
                            image_bytes: Optional[bytes] = None,
                            user_id: Optional[str] = None,
                            category: Optional[str] = None,
                            limit: int = 10,
                            min_score: float = 0.1) -> Dict[str, Any]:
        """Enhanced search with targeted filtering"""
        
        logger.info(f"Enhanced search - Query: '{query}', Category: {category}, User: {user_id}, Limit: {limit}")
        
        # First, perform the base search
        base_result = await self.base_handler.search_products(
            query=query,
            image_bytes=image_bytes,
            user_id=user_id,
            category=category,
            limit=limit * 2,  # Get more results for better filtering
            min_score=min_score
        )
        
        if base_result['status'] != 'success':
            return base_result
        
        results = base_result['results']
        
        # Apply enhanced filtering if we have a text query
        if query and results:
            # Extract product type from query for additional filtering
            product_type = self.extract_product_type_from_query(query)
            
            # Extract color from query for color-based filtering
            color = self.extract_color_from_query(query)
            
            # Apply relevance filtering
            filtered_results = self.filter_irrelevant_results(query, results)
            
            # If we extracted a specific product type, prioritize it
            if product_type:
                # Boost products that match the specific type
                for product in filtered_results:
                    product_name = product.get('name', '').lower()
                    if product_type in product_name:
                        # Increase similarity score for exact matches
                        product['similarity_score'] = min(product.get('similarity_score', 0) + 0.2, 1.0)
            
            # If we extracted a color, STRICTLY filter by color - no exceptions
            if color:
                color_filtered_results = []
                for product in filtered_results:
                    product_name = product.get('name', '').lower()
                    product_description = product.get('description', '').lower()
                    
                    # Check if product matches the requested color
                    color_terms = self.color_keywords.get(color, [])
                    if any(term in product_name or term in product_description for term in color_terms):
                        # Significantly boost color-matching products
                        product['similarity_score'] = min(product.get('similarity_score', 0) + 0.4, 1.0)
                        color_filtered_results.append(product)
                
                # ALWAYS use only color-matching products when a color is specified
                filtered_results = color_filtered_results if color_filtered_results else []
                
                # Re-sort by updated similarity score
                filtered_results.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            
            # Limit to requested number
            filtered_results = filtered_results[:limit]
            
            logger.info(f"Enhanced search completed. Found {len(filtered_results)} highly relevant products for '{query}'")
            
            return {
                'status': 'success',
                'results': filtered_results,
                'message': f'Found {len(filtered_results)} relevant products'
            }
        
        # For image-only searches, return base results but ensure they're relevant
        if image_bytes and results:
            # Apply basic relevance filtering for image searches too
            filtered_results = self.filter_irrelevant_results("image_search", results, min_relevance_threshold=0.5)
            filtered_results = filtered_results[:limit]
            
            return {
                'status': 'success', 
                'results': filtered_results,
                'message': f'Found {len(filtered_results)} relevant products'
            }
        
        return base_result
    
    async def search_jewelry_by_image_and_category(self, 
                                                  text_query: Optional[str] = None,
                                                  image_bytes: Optional[bytes] = None,
                                                  category: Optional[str] = None,
                                                  limit: int = 10,
                                                  min_score: float = 0.3) -> Dict[str, Any]:
        """
        Enhanced search specifically for jewelry items using image and category.
        
        Args:
            text_query: Optional text query to refine the search
            image_bytes: Image data as bytes
            category: Jewelry category (e.g., 'rings', 'necklaces')
            limit: Maximum number of results to return
            min_score: Minimum similarity score threshold
            
        Returns:
            Dictionary with search results and metadata
        """
        logger.info(f"Enhanced jewelry search - Query: '{text_query}', Category: {category}")
        
        # Detect specific jewelry category searches
        jewelry_terms = {
            "necklaces": ["necklace", "necklaces", "pendant", "chain"],
            "rings": ["ring", "rings", "band"],
            "earrings": ["earring", "earrings", "stud", "hoop"],
            "bracelets": ["bracelet", "bracelets", "bangle", "cuff"],
            "watches": ["watch", "watches", "timepiece"]
        }
        
        detected_category = None
        
        # Check if category is explicitly provided
        if category and category.lower() in jewelry_terms:
            detected_category = category.lower()
            logger.info(f"Explicit jewelry category search: {detected_category}")
        # Otherwise try to detect from query
        elif text_query:
            text_query_lower = text_query.lower()
            for cat, terms in jewelry_terms.items():
                if any(term in text_query_lower for term in terms):
                    detected_category = cat
                    category = cat
                    logger.info(f"Detected {cat} search from query, setting category to '{cat}'")
                    break
        
        # Use the base search_products method but with jewelry-specific processing
        search_results = await self.search_products(
            query=text_query,
            image_bytes=image_bytes,
            category=category,
            limit=limit * 2 if detected_category else limit,  # Get more results for category-specific searches
            min_score=min_score * 0.8 if detected_category else min_score  # Lower threshold for category-specific searches
        )
        
        if search_results.get('status') != 'success':
            return search_results
            
        results = search_results.get('results', [])
        
        # For specific jewelry searches, prioritize products matching the detected category
        if detected_category and results:
            # First, separate category-specific products from others
            category_products = []
            other_products = []
            
            # Get the relevant terms for the detected category
            relevant_terms = jewelry_terms.get(detected_category, [])
            
            for product in results:
                name = product.get('name', '').lower()
                desc = product.get('description', '').lower()
                product_category = product.get('category', '').lower()
                
                # Check if product matches the detected category
                if (any(term in name or term in desc for term in relevant_terms) or 
                    detected_category in product_category or 
                    'jewelry' in product_category):
                    category_products.append(product)
                else:
                    other_products.append(product)
            
            # Combine results with category-specific products first
            prioritized_results = category_products + other_products
            search_results['results'] = prioritized_results[:limit]
            search_results['message'] = f'Found {len(search_results["results"])} {detected_category} and similar items'
            
        return search_results
        
    async def search_products_enhanced(self, 
                                     query: Optional[str] = None,
                                     image_bytes: Optional[bytes] = None,
                                     user_id: Optional[str] = None,
                                     category: Optional[str] = None,
                                     limit: int = 10,
                                     min_score: float = 0.1) -> Dict[str, Any]:
        """Hybrid search combining keyword, category, and vision-based approaches"""
        
        logger.info(f"Hybrid search - Query: '{query}', Category: {category}, User: {user_id}, Limit: {limit}")
        
        # Extract color from query if present
        color = None
        if query:
            color = self.extract_color_from_query(query)
            
        # First, perform the base search
        base_result = await self.base_handler.search_products(
            query=query,
            image_bytes=image_bytes,
            user_id=user_id,
            category=category,
            limit=limit * 3,  # Get more results for better filtering
            min_score=min_score
        )
        
        if base_result['status'] != 'success':
            return base_result
        
        results = base_result['results']
        
        # Apply enhanced filtering if we have a text query
        if query and results:
            # Extract product type from query for additional filtering
            product_type = self.extract_product_type_from_query(query)
            
            # Apply relevance filtering
            filtered_results = self.filter_irrelevant_results(query, results)
            
            # For color-specific queries like "red dress", strictly filter by color
            if color and product_type and "dress" in query.lower():
                color_filtered_results = []
                color_terms = self.color_keywords.get(color, [])
                
                for product in filtered_results:
                    product_name = product.get('name', '').lower()
                    product_description = product.get('description', '').lower()
                    
                    # Check if product matches the requested color
                    if any(term in product_name or term in product_description for term in color_terms):
                        # Significantly boost color-matching products
                        product['similarity_score'] = min(product.get('similarity_score', 0) + 0.5, 1.0)
                        color_filtered_results.append(product)
                
                # If we found color-matching products, use only those
                if color_filtered_results:
                    filtered_results = color_filtered_results
                    logger.info(f"Color filtering applied for '{color} {product_type}'. Found {len(filtered_results)} matching products.")
            
            # Re-sort by updated similarity score
            filtered_results.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            
            # Limit to requested number
            filtered_results = filtered_results[:limit]
            
            return {
                'status': 'success',
                'results': filtered_results,
                'message': f'Found {len(filtered_results)} relevant products'
            }
        
        # For image-only searches, return base results
        return base_result