import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FAISSStore:
    """
    Local vector store using FAISS for similarity search.
    """
    def __init__(self, dimension: int = 768, index_path: str = "faiss_index.bin", metadata_path: str = "faiss_metadata.pkl"):
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = [] # List of dicts corresponding to vectors
        
        self.load()

    def load(self):
        """Load index and metadata from disk if they exist."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "rb") as f:
                    self.metadata = pickle.load(f)
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors.")
            except Exception as e:
                logger.error(f"Failed to load FAISS index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Create a new FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        logger.info("Created new FAISS index.")

    def save(self):
        """Save index and metadata to disk."""
        if self.index:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.metadata, f)
            logger.info("Saved FAISS index to disk.")

    def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]):
        """
        Add vectors and metadata to the store.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dicts
        """
        if len(vectors) != len(metadata):
            raise ValueError("Number of vectors and metadata items must match.")
        
        if not vectors:
            return

        vectors_np = np.array(vectors).astype('float32')
        
        if self.index is None:
            self._create_new_index()
            
        self.index.add(vectors_np)
        self.metadata.extend(metadata)
        self.save()
        logger.info(f"Added {len(vectors)} vectors to FAISS store.")

    def search(self, query_vector: List[float], k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of metadata dicts with 'score' added.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        query_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx].copy()
                # FAISS L2 distance: lower is better. 
                # Convert to similarity score if needed, or just return distance.
                item['distance'] = float(distances[0][i])
                # Simple similarity conversion for compatibility (1 / (1 + distance))
                item['relevance_score'] = 1.0 / (1.0 + item['distance'])
                results.append(item)
                
        return results
