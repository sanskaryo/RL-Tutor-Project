"""
RAG (Retrieval-Augmented Generation) Services
Provides document processing, embedding, and retrieval capabilities for the doubt solver.
"""

from .embedder import GeminiEmbedder
from .chunker import TextChunker
from .retriever import VectorRetriever

__all__ = ["GeminiEmbedder", "TextChunker", "VectorRetriever"]
