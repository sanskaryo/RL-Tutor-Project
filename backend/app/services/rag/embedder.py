"""
Gemini Embedder - Generate embeddings for text using Google Gemini API
"""
import google.generativeai as genai
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class GeminiEmbedder:
    """
    Wrapper for Google Gemini text embedding API.
    Uses text-embedding-004 model for high-quality embeddings.
    """
    
    def __init__(self, api_key: str, model: str = "models/text-embedding-004"):
        """
        Initialize the Gemini embedder.
        
        Args:
            api_key: Google Gemini API key
            model: Embedding model to use (default: text-embedding-004)
        """
        genai.configure(api_key=api_key)
        self.model = model
        logger.info(f"Initialized GeminiEmbedder with model: {model}")
    
    def embed_text(self, text: str, task_type: str = "retrieval_document") -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            task_type: Type of task (retrieval_document, retrieval_query, semantic_similarity)
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_batch(
        self, 
        texts: List[str], 
        task_type: str = "retrieval_document"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            task_type: Type of task
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for i, text in enumerate(texts):
            try:
                embedding = self.embed_text(text, task_type)
                embeddings.append(embedding)
                if (i + 1) % 10 == 0:
                    logger.info(f"Embedded {i + 1}/{len(texts)} texts")
            except Exception as e:
                logger.error(f"Error embedding text {i}: {e}")
                embeddings.append([])  # Append empty list for failed embeddings
        
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding specifically for search queries.
        
        Args:
            query: Search query text
        
        Returns:
            Embedding vector optimized for retrieval
        """
        return self.embed_text(query, task_type="retrieval_query")
    
    @property
    def dimension(self) -> int:
        """Return the dimension of embeddings (768 for text-embedding-004)"""
        return 768
