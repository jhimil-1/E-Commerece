from datetime import datetime
import logging
from typing import List, Dict, Any
from bson import ObjectId
import requests
from database import MongoDB
from gemini_utils import gemini_manager
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

logger = logging.getLogger(__name__)

class ProductHandler:
    def __init__(self):
        self.db = MongoDB.get_db()
    
    async def process_product_upload(self, products: List[Dict[str, Any]], user_id: str) -> Dict[str, Any]:
        """Process and store uploaded products"""
        try:
            products_to_insert = []
            current_time = datetime.utcnow()
            
            for product in products:
                # Extract fields
                name = product.get("name", "")
                description = product.get("description", "")
                price = product.get("price", 0.0)
                category = product.get("category", "")
                image_data = product.get("image", "")  # Base64 encoded image
                
                # Generate text embedding using CLIP for consistency
                text_content = f"{name} {description} {category}"
                text_embedding = clip_manager.get_text_embedding(text_content)
                
                # Generate image embedding using CLIP if image provided
                image_embedding = None
                if image_data:
                    try:
                        # Handle image URLs from JSON files
                        if image_data.startswith('http'):
                            # Download image from URL
                            import requests
                            response = requests.get(image_data, timeout=10)
                            response.raise_for_status()
                            image_bytes = response.content
                            image_embedding = clip_manager.get_image_embedding(image_bytes)
                        else:
                            # Handle base64 or other formats
                            image_embedding = clip_manager.get_image_embedding(image_data)
                    except Exception as img_error:
                        logger.warning(f"Failed to generate image embedding: {img_error}")
                
                product_doc = {
                    **product,
                    "text_embedding": text_embedding,
                    "image_embedding": image_embedding,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "created_by": user_id,
                    "is_active": True
                }
                products_to_insert.append(product_doc)
            
            # Insert into MongoDB
            if products_to_insert:
                result = self.db.products.insert_many(products_to_insert)
                inserted_ids = [str(id) for id in result.inserted_ids]
                
                # Generate & store embeddings in Qdrant
                await self._generate_and_store_embeddings(products_to_insert, inserted_ids, user_id)
                
                return {
                    "inserted_count": len(inserted_ids),
                    "product_ids": inserted_ids
                }
            
            return {"inserted_count": 0}
        
        except Exception as e:
            logger.error(f"Error in process_product_upload: {str(e)}", exc_info=True)
            raise
    
    async def _generate_and_store_embeddings(self, products: List[Dict[str, Any]], product_ids: List[str], user_id: str):
        """Generate and store vector embeddings for products"""
        try:
            for product, product_id in zip(products, product_ids):
                text = f"{product['name']} {product['description']} {product['category']}"
                
                # Use CLIP embeddings for all products to ensure consistency with Qdrant collection
                embedding = clip_manager.get_text_embedding(text)
                
                # Prepare metadata with image information
                metadata = {
                    "name": product["name"],
                    "price": product["price"],
                    "created_by": user_id
                }
                
                # Include image information if available
                if "image" in product and product["image"]:
                    metadata["image_url"] = product["image"]
                if "image_url" in product and product["image_url"]:
                    metadata["image_url"] = product["image_url"]
                if "image_path" in product and product["image_path"]:
                    metadata["image_path"] = product["image_path"]
                
                qdrant_manager.upsert_product(
                    product_id=product_id,
                    text_embedding=embedding,
                    category=product["category"],
                    metadata=metadata
                )
        except Exception as e:
            logger.error(f"Error generating/storing embeddings: {str(e)}", exc_info=True)
            pass

    async def search_products(
        self,
        query: str = None,
        user_id: str = None,
        image_bytes: bytes = None,
        category: str = None,
        limit: int = 10,
        min_score: float = 0.1
    ) -> Dict[str, Any]:
        """
        Search for products using semantic vector search with category filtering
        
        Args:
            query: Text query for search
            user_id: ID of the user making the search
            image_bytes: Binary image data for image search
            category: Specific category to filter by
            limit: Maximum number of results to return
            min_score: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            Dictionary containing search results
        """
        try:
            logger.info(f"Starting search with params: query={query}, category={category}, limit={limit}, min_score={min_score}")
            
            # Common e-commerce categories
            ecommerce_categories = [
                "electronics", "phones", "laptops", "headphones", "tablets",
                "clothing", "shoes", "accessories", "bags", "watches",
                "home", "furniture", "decor", "kitchen", "appliances",
                "books", "toys", "sports", "fitness", "beauty", "health",
                "jewelry", "necklaces", "earrings", "bracelets", "rings"
            ]
            
            # If no explicit category is provided, try to infer from query
            if not category and query:
                query_lower = query.lower()
                for cat in ecommerce_categories:
                    if cat in query_lower:
                        category = cat
                        logger.info(f"Inferred category from query: {category}")
                        break
            
            # Generate embeddings based on input type
            query_embedding = None
            
            try:
                if query and image_bytes:
                    # Both text and image - combine embeddings
                    logger.debug("Generating combined text and image embeddings")
                    text_embedding = clip_manager.get_text_embedding(query)
                    image_embedding = clip_manager.get_image_embedding(image_bytes)
                    # Weighted combination (70% text, 30% image)
                    query_embedding = [
                        0.7 * t + 0.3 * i
                        for t, i in zip(text_embedding, image_embedding)
                    ]
                elif query:
                    # Text only
                    logger.debug(f"Generating text embedding for query: {query}")
                    query_embedding = clip_manager.get_text_embedding(query)
                elif image_bytes:
                    # Image only
                    logger.debug("Generating image embedding")
                    query_embedding = clip_manager.get_image_embedding(image_bytes)
                else:
                    raise ValueError("Either query text or image must be provided")
                
                if not query_embedding:
                    raise ValueError("Failed to generate query embedding")
                    
            except Exception as e:
                logger.error(f"Error generating embeddings: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "message": "Error processing your search request",
                    "results": []
                }
            
            # Get user info for filtering
            qdrant_user_id = None
            if user_id:
                try:
                    # Try to find user by ObjectId (for old users)
                    user = self.db.users.find_one({"_id": ObjectId(user_id)})
                    if not user:
                        # If ObjectId conversion fails, try by user_id (for new users)
                        user = self.db.users.find_one({"user_id": user_id})
                    
                    if user:
                        qdrant_user_id = user.get("user_id", str(user.get("_id")))
                        logger.debug(f"Found user ID for search: {qdrant_user_id}")
                except Exception as e:
                    logger.warning(f"Error looking up user {user_id}: {str(e)}")
            
            # Search in Qdrant with user filtering and category filtering
            logger.info(f"Searching Qdrant with user: {qdrant_user_id}, category: {category}, limit: {limit}")
            
            try:
                search_results = qdrant_manager.search_similar_products(
                    query_embedding=query_embedding,
                    user_id=qdrant_user_id,
                    category_filter=category,
                    limit=limit * 2,  # Get more results to filter further
                    min_score=min_score
                )
                
                logger.info(f"Qdrant search returned {len(search_results)} results")
                if search_results:
                    logger.debug(f"First result score: {search_results[0].get('score', 0):.2f}")
                
                if not search_results and category:
                    # Try without category filter if no results
                    logger.info("No results with category filter, trying without category")
                    search_results = qdrant_manager.search_similar_products(
                        query_embedding=query_embedding,
                        user_id=qdrant_user_id,
                        limit=limit,
                        min_score=min_score * 0.8  # Slightly lower threshold
                    )
                    
                    if search_results:
                        logger.info(f"Found {len(search_results)} results without category filter")
            
            except Exception as e:
                logger.error(f"Error in Qdrant search: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "message": "Error performing search",
                    "results": []
                }
            
            # Retrieve product documents from MongoDB
            if not search_results:
                return {
                    "status": "success",
                    "message": "No matching products found",
                    "results": []
                }
                
            try:
                # Extract product IDs from search results
                product_ids = []
                for hit in search_results:
                    if isinstance(hit, dict) and "product_id" in hit:
                        product_ids.append(hit["product_id"])
                    else:
                        logger.warning(f"Unexpected search result format: {hit}")
                
                if not product_ids:
                    return {
                        "status": "success",
                        "message": "No valid product IDs found in search results",
                        "results": []
                    }
                
                logger.info(f"Retrieving {len(product_ids)} products from MongoDB")
                
                # Convert string IDs to ObjectIds for MongoDB query
                object_ids = []
                invalid_ids = []
                for pid in product_ids:
                    try:
                        object_ids.append(ObjectId(pid))
                    except Exception as e:
                        invalid_ids.append(pid)
                        logger.warning(f"Invalid product ID format: {pid} - {str(e)}")
                
                if not object_ids and invalid_ids:
                    logger.error(f"All product IDs were invalid: {invalid_ids}")
                    return {
                        "status": "error",
                        "message": "Invalid product references found",
                        "results": []
                    }
                
                # Get products from MongoDB
                try:
                    products_cursor = self.db.products.find(
                        {"_id": {"$in": object_ids}}
                    )
                    
                    # Create a dictionary to store products by ID for efficient lookup
                    products_by_id = {}
                    for product in products_cursor:
                        try:
                            product_id = str(product.get("_id"))
                            if product_id:
                                products_by_id[product_id] = product
                            else:
                                logger.warning("Product missing _id field")
                        except Exception as e:
                            logger.error(f"Error processing product: {str(e)}")
                    
                    # Process search results and prepare response
                    products_dict = {}
                    seen_products = set()  # Track seen product IDs to avoid duplicates
                    
                    for hit in search_results:
                        if not isinstance(hit, dict) or "product_id" not in hit:
                            continue
                            
                        product_id = hit["product_id"]
                        
                        # Skip if we've already processed this product
                        if product_id in seen_products:
                            continue
                            
                        product = products_by_id.get(product_id)
                        
                        if not product:
                            logger.debug(f"Product not found in MongoDB: {product_id}")
                            continue
                        
                        # Mark this product as seen
                        seen_products.add(product_id)
                        
                        # Calculate a normalized score (0-100)
                        raw_score = hit.get("score", 0.0)
                        normalized_score = min(max(0, int(raw_score * 100)), 100)
                        
                        # Get additional metadata from Qdrant payload if available
                        payload = hit.get("payload", {})
                        
                        # Create result dictionary
                        result = {
                            "id": str(product.get("_", "")),
                            "name": payload.get("name") or product.get("name", "Unnamed Product"),
                            "description": payload.get("description") if payload.get("description") is not None else product.get("description", ""),
                            "price": float(payload.get("price") if payload.get("price") is not None else product.get("price", 0.0)),
                            "category": payload.get("category") if payload.get("category") is not None else product.get("category", "other"),
                            "image_url": payload.get("image_url") if payload.get("image_url") is not None else product.get("image_url", ""),
                            "similarity_score": raw_score,
                            "match_percentage": normalized_score,
                            "in_stock": product.get("in_stock", True),
                            "created_at": product.get("created_at", ""),
                            "created_by": product.get("created_by", ""),
                            "metadata": {
                                "source": "vector_search",
                                "has_image": bool(payload.get("image_url") or product.get("image_url")),
                                "category_matched": bool(category and category.lower() in (payload.get("category", "") or "").lower())
                            }
                        }
                        
                        # Add any additional fields from the payload
                        for key, value in payload.items():
                            if key not in result and key not in ["text_embedding", "image_embedding"]:
                                result[key] = value
                        
                        products_dict[product_id] = result
                    
                    if not products_dict:
                        logger.warning("No valid products found after processing search results")
                        return {
                            "status": "success",
                            "message": "No matching products found",
                            "results": []
                        }
                    
                    # Convert to list and sort by score
                    products = list(products_dict.values())
                    products.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
                    
                    # Apply category filter if specified
                    if category:
                        products = [p for p in products if category.lower() in p.get("category", "").lower()]
                    
                    # Apply limit
                    products = products[:limit]
                    
                    logger.info(f"Search completed. Found {len(products)} results")
                    if products:
                        logger.debug(f"Top result: {products[0]['name']} (Score: {products[0]['similarity_score']:.2f})")
                    
                    return {
                        "status": "success",
                        "count": len(products),
                        "query": query,
                        "category": category,
                        "results": products,
                        "metadata": {
                            "has_query": bool(query),
                            "has_image": bool(image_bytes),
                            "filtered_by_category": bool(category),
                            "user_id": user_id,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                    
                except Exception as e:
                    logger.error(f"Error processing search results: {str(e)}", exc_info=True)
                    return {
                        "status": "error",
                        "message": "Error processing search results",
                        "results": []
                    }
                        
            except Exception as e:
                logger.error(f"Error in search_products: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "message": "An error occurred while processing your search",
                    "results": []
                }
        
        except Exception as e:
            error_msg = f"Error in search_products: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while processing your search",
                "error": error_msg,
                "results": []
            }

    async def search_jewelry_by_image_and_category(
        self,
        query_text: str = None,
        query_image: str = None,
        category: str = None,
        limit: int = 10,
        min_score: float = 0.1  # Lowered from 0.3 to get more results
    ) -> Dict[str, Any]:
        """
        Search for jewelry using CLIP-based similarity on both image and category.
        
        Args:
            query_text: Text query describing the jewelry
            query_image: Base64 encoded image data
            category: Filter by jewelry category (e.g., 'earrings', 'rings')
            limit: Maximum number of results to return
            min_score: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            Dictionary with search results
        """
        logger.info(f"Starting image search - Category: {category}, Min Score: {min_score}, Has Text: {query_text is not None}, Has Image: {query_image is not None}")
        try:
            # Initialize variables
            text_embedding = None
            image_embedding = None
            
            # Check if we need to extract category from query text
            query_lower = (query_text or "").lower()
            jewelry_categories = ["earrings", "bracelets", "necklaces", "rings", "bangles", "watches"]
            
            # If no explicit category is provided, try to extract from query text
            if not category:
                for cat in jewelry_categories:
                    if cat in query_lower:
                        category = cat  # Set the category to the matched one
                        logger.info(f"Extracted category from query: {category}")
                        break
            
            # Generate text embedding if query_text is provided
            if query_text:
                text_embedding = clip_manager.get_text_embedding(query_text)
            
            # Generate image embedding if query_image is provided
            if query_image:
                image_embedding = clip_manager.get_image_embedding(query_image)
            
            # Determine which embedding to use for search
            if text_embedding is not None and image_embedding is not None:
                # Weighted combination (70% text, 30% image for jewelry)
                search_embedding = [
                    0.7 * t + 0.3 * i
                    for t, i in zip(text_embedding, image_embedding)
                ]
                query_type = "image_and_text"
            elif text_embedding is not None:
                search_embedding = text_embedding
                query_type = "text"
            elif image_embedding is not None:
                search_embedding = image_embedding
                query_type = "image"
            else:
                raise ValueError("Either query_text or query_image must be provided")
            
            # Search in Qdrant with category filter
            logger.info(f"Searching with embedding size: {len(search_embedding)}")
            search_results = qdrant_manager.search_similar(
                query_embedding=search_embedding,
                limit=limit,
                category_filter=category,
                min_score=min_score
            )
            logger.info(f"Raw search results count: {len(search_results)}")
            
            # Log top 3 results for debugging
            for i, result in enumerate(search_results[:3]):
                logger.info(f"Result {i+1} - ID: {result.get('id')}, Score: {result.get('score', 0):.4f}, Category: {result.get('category', 'N/A')}")
            
            # Get product details from MongoDB
            # Use a dictionary to store unique products by their ID
            unique_product_ids = {}
            for hit in search_results:
                product_id = hit["id"]
                # Keep the highest score for each product
                if product_id not in unique_product_ids or hit.get("score", 0) > unique_product_ids[product_id].get("score", 0):
                    unique_product_ids[product_id] = {"id": product_id, "score": hit.get("score", 0)}
            
            if not unique_product_ids:
                return {
                    "status": "success",
                    "message": "No jewelry found matching your criteria",
                    "results": [],
                    "count": 0,
                    "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                    "category_filter": category
                }
            
            # Filter out invalid ObjectIds and get unique product IDs
            valid_ids = []
            for pid in unique_product_ids:
                try:
                    valid_ids.append(ObjectId(pid))
                except:
                    logger.warning(f"Invalid ObjectId: {pid}")
                    continue
            
            if not valid_ids:
                return {
                    "status": "success",
                    "message": "No valid jewelry items found",
                    "results": [],
                    "count": 0,
                    "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                    "category_filter": category
                }
            
            # Get products from MongoDB
            products_cursor = self.db.products.find(
                {"_id": {"$in": valid_ids}}
            )
            
            # Create a list of products with their scores
            products = []
            for product in products_cursor:  # Use regular for loop since it's not async
                product_id = str(product["_id"])
                if product_id in unique_product_ids:
                    product["_id"] = product_id
                    product["similarity_score"] = unique_product_ids[product_id]["score"]
                    products.append(product)
            
            # Sort by score in descending order
            products.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
            
            # Limit to the requested number of results
            products = products[:limit]
            
            return {
                "status": "success",
                "message": f"Found {len(products)} jewelry items",
                "results": products,
                "count": len(products),
                "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                "category_filter": category
            }
        
        except Exception as e:
            logger.error(f"Error searching jewelry by image and category: {str(e)}", exc_info=True)
            raise


# ✅ Global instance
product_handler = ProductHandler()
