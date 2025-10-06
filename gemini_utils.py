# gemini_utils.py
import os
import logging
import time
import random
import hashlib
from typing import List, Optional, Dict
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

logger = logging.getLogger(__name__)

class EmbeddingCache:
    """Simple in-memory cache for embeddings"""
    def __init__(self):
        self.cache: Dict[str, List[float]] = {}
    
    def get(self, text: str) -> Optional[List[float]]:
        key = hashlib.md5(text.encode()).hexdigest()
        return self.cache.get(key)
    
    def set(self, text: str, embedding: List[float]):
        key = hashlib.md5(text.encode()).hexdigest()
        self.cache[key] = embedding

class GeminiManager:
    """Handles interaction with the Google Gemini API with fallback to local model"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cache = EmbeddingCache()
        self.local_model = None
        self.use_local = False
        self.rate_limited_until = 0
        self.initialize_models()

    def initialize_models(self):
        """Initialize both Gemini and local models"""
        # Initialize local model (only if needed)
        try:
            logger.info("Loading local embedding model...")
            self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Local model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load local model: {e}")

        # Initialize Gemini
        if not self.api_key:
            logger.warning("No Gemini API key found. Using local model only.")
            self.use_local = True
            return

        try:
            genai.configure(api_key=self.api_key)
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini: {e}")
            self.use_local = True

    def get_text_embedding(self, text: str) -> List[float]:
        """Get embedding with automatic fallback to local model"""
        # Check cache first
        cached = self.cache.get(text)
        if cached:
            return cached

        # If we're rate limited or in local-only mode
        if self.use_local or time.time() < self.rate_limited_until:
            return self._get_local_embedding(text)

        # Try Gemini API
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            embedding = response["embedding"]
            self.cache.set(text, embedding)
            return embedding
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                logger.warning("Gemini API rate limit hit. Falling back to local model for 1 hour.")
                self.rate_limited_until = time.time() + 3600  # Block for 1 hour
            else:
                logger.error(f"Gemini API error: {e}")
            return self._get_local_embedding(text)

    def _get_local_embedding(self, text: str) -> List[float]:
        """Get embedding using the local model"""
        try:
            if not self.local_model:
                raise RuntimeError("Local model not available")
            embedding = self.local_model.encode(text, convert_to_numpy=True).tolist()
            self.cache.set(text, embedding)
            return embedding
        except Exception as e:
            logger.error(f"Local embedding failed: {e}")
            # Return a zero vector as last resort
            return [0.0] * 384  # Default size for all-MiniLM-L6-v2

    def get_query_embedding(self, query: str) -> List[float]:
        """Alias for get_text_embedding with query prefix"""
        return self.get_text_embedding(f"query: {query}")

# Global instance
gemini_manager = GeminiManager()