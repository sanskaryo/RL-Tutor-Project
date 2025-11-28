"""
Vector Retriever - Search for relevant documents using vector similarity (FAISS)
"""
from typing import List, Dict, Any, Optional
import logging
from app.services.vector_db.faiss_store import FAISSStore

logger = logging.getLogger(__name__)


class VectorRetriever:
    """
    Retrieve relevant document chunks using FAISS vector search.
    """
    
    def __init__(
        self, 
        mongodb_uri: str = None, # Kept for compatibility
        database_name: str = "jee_tutor", # Kept for compatibility
        collection_name: str = "document_chunks", # Kept for compatibility
        index_name: str = "vector_index" # Kept for compatibility
    ):
        """
        Initialize the vector retriever.
        """
        # Initialize FAISS store
        # We use a local file path based on the collection name to keep it organized
        index_path = f"{collection_name}_faiss.bin"
        metadata_path = f"{collection_name}_metadata.pkl"
        
        self.store = FAISSStore(
            dimension=768, # Gemini text-embedding-004 dimension
            index_path=index_path,
            metadata_path=metadata_path
        )
        logger.info(f"Initialized VectorRetriever with FAISS (index={index_path})")
    
    def search(
        self, 
        query_embedding: List[float],
        top_k: int = 3,
        subject_filter: Optional[str] = None,
        min_score: float = 0.0 # FAISS distance is not 0-1 score, so we ignore min_score for now or adapt
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.
        """
        try:
            results = self.store.search(query_embedding, k=top_k)
            
            # Filter by subject if provided
            if subject_filter:
                results = [
                    r for r in results 
                    if r.get('metadata', {}).get('subject') == subject_filter
                ]
            
            # Filter by score if needed (relevance_score is 1/(1+dist))
            if min_score > 0:
                 results = [r for r in results if r.get('relevance_score', 0) >= min_score]

            logger.info(f"Found {len(results)} results (query top_k={top_k})")
            return results
        
        except Exception as e:
            logger.error(f"Error during vector search: {e}")
            return []
    
    def insert_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Insert document chunks into the store.
        """
        try:
            if not chunks:
                logger.warning("No chunks to insert")
                return 0
            
            vectors = [chunk['embedding'] for chunk in chunks]
            # Store the whole chunk as metadata, excluding the embedding to save space if needed
            # But FAISSStore expects metadata list.
            metadata_list = []
            for chunk in chunks:
                meta = chunk.copy()
                if 'embedding' in meta:
                    del meta['embedding']
                metadata_list.append(meta)
            
            self.store.add_vectors(vectors, metadata_list)
            count = len(vectors)
            logger.info(f"Inserted {count} chunks into FAISS")
            return count
        
        except Exception as e:
            logger.error(f"Error inserting chunks: {e}")
            raise
    
    def create_vector_index(self):
        """
        No-op for FAISS as index is created automatically.
        """
        pass
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.store.index.ntotal if self.store.index else 0
            
            stats = {
                "total_chunks": count,
                "backend": "FAISS"
            }
            
            return stats
        
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def close(self):
        """No-op for FAISS."""
        pass
