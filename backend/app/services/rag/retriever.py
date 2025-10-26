"""
Vector Retriever - Search for relevant documents using vector similarity
"""
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class VectorRetriever:
    """
    Retrieve relevant document chunks from MongoDB Atlas using vector search.
    """
    
    def __init__(
        self, 
        mongodb_uri: str,
        database_name: str = "jee_tutor",
        collection_name: str = "document_chunks",
        index_name: str = "vector_index"
    ):
        """
        Initialize the vector retriever.
        
        Args:
            mongodb_uri: MongoDB connection string
            database_name: Name of the database
            collection_name: Name of the collection storing chunks
            index_name: Name of the vector search index
        """
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.index_name = index_name
        logger.info(f"Initialized VectorRetriever (db={database_name}, collection={collection_name})")
    
    def search(
        self, 
        query_embedding: List[float],
        top_k: int = 3,
        subject_filter: Optional[str] = None,
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Embedding vector of the search query
            top_k: Number of top results to return
            subject_filter: Optional filter by subject (Physics, Chemistry, Math)
            min_score: Minimum similarity score threshold
        
        Returns:
            List of matching documents with scores
        """
        try:
            # Build aggregation pipeline for vector search
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": self.index_name,
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": top_k * 10,  # Search more candidates
                        "limit": top_k
                    }
                },
                {
                    "$project": {
                        "text": 1,
                        "metadata": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            # Add subject filter if provided
            if subject_filter:
                pipeline.insert(1, {
                    "$match": {"metadata.subject": subject_filter}
                })
            
            # Execute search
            results = list(self.collection.aggregate(pipeline))
            
            # Filter by minimum score
            filtered_results = [
                r for r in results 
                if r.get("score", 0) >= min_score
            ]
            
            logger.info(f"Found {len(filtered_results)} results (query top_k={top_k})")
            return filtered_results
        
        except Exception as e:
            logger.error(f"Error during vector search: {e}")
            return []
    
    def insert_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Insert document chunks into the collection.
        
        Args:
            chunks: List of chunk dictionaries with text, embedding, and metadata
        
        Returns:
            Number of inserted documents
        """
        try:
            if not chunks:
                logger.warning("No chunks to insert")
                return 0
            
            result = self.collection.insert_many(chunks)
            count = len(result.inserted_ids)
            logger.info(f"Inserted {count} chunks into MongoDB")
            return count
        
        except Exception as e:
            logger.error(f"Error inserting chunks: {e}")
            raise
    
    def create_vector_index(self):
        """
        Create a vector search index on the collection.
        Note: For MongoDB Atlas, this is usually done via the Atlas UI.
        This method provides the index specification.
        """
        index_spec = {
            "name": self.index_name,
            "type": "vectorSearch",
            "definition": {
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": 768,  # For text-embedding-004
                        "similarity": "cosine"
                    },
                    {
                        "type": "filter",
                        "path": "metadata.subject"
                    },
                    {
                        "type": "filter",
                        "path": "metadata.chapter"
                    }
                ]
            }
        }
        
        logger.info(f"Vector index specification: {index_spec}")
        return index_spec
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count_documents({})
            
            # Get subjects distribution
            subjects = self.collection.distinct("metadata.subject")
            
            stats = {
                "total_chunks": count,
                "subjects": subjects,
                "collection_name": self.collection.name
            }
            
            return stats
        
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()
        logger.info("Closed MongoDB connection")
