"""
MongoDB Vector Database Utilities
"""
from pymongo import MongoClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    """
    MongoDB client for vector database operations.
    """
    
    def __init__(self, connection_uri: str):
        """
        Initialize MongoDB client.
        
        Args:
            connection_uri: MongoDB connection string
        """
        self.uri = connection_uri
        self.client = None
        logger.info("Initialized MongoDBClient")
    
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            # Test connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def get_database(self, db_name: str):
        """
        Get a database instance.
        
        Args:
            db_name: Name of the database
        
        Returns:
            Database object
        """
        if not self.client:
            self.connect()
        return self.client[db_name]
    
    def get_collection(self, db_name: str, collection_name: str):
        """
        Get a collection instance.
        
        Args:
            db_name: Name of the database
            collection_name: Name of the collection
        
        Returns:
            Collection object
        """
        db = self.get_database(db_name)
        return db[collection_name]
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")


def get_mongo_client(uri: Optional[str] = None) -> MongoDBClient:
    """
    Factory function to get MongoDB client.
    
    Args:
        uri: Optional MongoDB URI (uses env var if not provided)
    
    Returns:
        MongoDBClient instance
    """
    if not uri:
        from app.core.config import settings
        uri = getattr(settings, 'MONGODB_URI', None)
        
        if not uri:
            raise ValueError("MongoDB URI not configured")
    
    client = MongoDBClient(uri)
    client.connect()
    return client
