"""
Text Chunker - Split documents into manageable chunks for embedding
"""
import tiktoken
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Split text into chunks using token-based splitting.
    Ensures chunks are within token limits for embedding models.
    """
    
    def __init__(
        self, 
        chunk_size: int = 500, 
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base"
    ):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
            encoding_name: Tokenizer encoding to use
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)
        logger.info(f"Initialized TextChunker (size={chunk_size}, overlap={chunk_overlap})")
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text."""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
        
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []
        
        # Tokenize the text
        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)
        
        if total_tokens == 0:
            return []
        
        chunks = []
        start_idx = 0
        chunk_id = 0
        
        while start_idx < total_tokens:
            # Calculate end index for this chunk
            end_idx = min(start_idx + self.chunk_size, total_tokens)
            
            # Get chunk tokens
            chunk_tokens = tokens[start_idx:end_idx]
            
            # Decode back to text
            chunk_text = self.encoding.decode(chunk_tokens)
            
            # Create chunk with metadata
            chunk_data = {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_token": start_idx,
                "end_token": end_idx,
                "token_count": len(chunk_tokens),
                "metadata": metadata or {}
            }
            
            chunks.append(chunk_data)
            
            # Move to next chunk with overlap
            start_idx += self.chunk_size - self.chunk_overlap
            chunk_id += 1
        
        logger.info(f"Split text into {len(chunks)} chunks ({total_tokens} total tokens)")
        return chunks
    
    def chunk_by_sentences(
        self, 
        text: str, 
        metadata: Dict[str, Any] = None,
        max_sentences: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Split text into chunks by sentences (alternative method).
        
        Args:
            text: Text to chunk
            metadata: Optional metadata
            max_sentences: Maximum sentences per chunk
        
        Returns:
            List of chunk dictionaries
        """
        # Simple sentence splitting (can be improved with NLTK/spaCy)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        chunks = []
        chunk_id = 0
        
        for i in range(0, len(sentences), max_sentences):
            chunk_sentences = sentences[i:i + max_sentences]
            chunk_text = '. '.join(chunk_sentences) + '.'
            
            # Check token count
            token_count = self.count_tokens(chunk_text)
            
            if token_count > self.chunk_size:
                # If chunk is too large, fall back to token-based chunking
                sub_chunks = self.chunk_text(chunk_text, metadata)
                chunks.extend(sub_chunks)
            else:
                chunk_data = {
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "sentence_range": f"{i}-{i + len(chunk_sentences)}",
                    "token_count": token_count,
                    "metadata": metadata or {}
                }
                chunks.append(chunk_data)
                chunk_id += 1
        
        logger.info(f"Split text into {len(chunks)} sentence-based chunks")
        return chunks
