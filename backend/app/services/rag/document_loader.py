"""
PDF Document Loader - Extract text from PDFs and prepare for embedding
"""
import pymupdf  # PyMuPDF
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFDocumentLoader:
    """
    Load and process PDF documents for the RAG pipeline.
    Extracts text, metadata, and prepares chunks for embedding.
    """
    
    def __init__(self):
        """Initialize the PDF loader."""
        logger.info("Initialized PDFDocumentLoader")
    
    def load_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Load a PDF file and extract text with metadata.
        
        Args:
            file_path: Path to the PDF file
        
        Returns:
            Dictionary containing full text and metadata
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            if path.suffix.lower() != '.pdf':
                raise ValueError(f"File is not a PDF: {file_path}")
            
            # Open PDF
            doc = pymupdf.open(file_path)
            
            # Extract metadata
            metadata = {
                "filename": path.name,
                "filepath": str(path.absolute()),
                "page_count": len(doc),
                "metadata": doc.metadata
            }
            
            # Extract text from all pages
            full_text = ""
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": page_text,
                    "char_count": len(page_text)
                })
                
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
            
            doc.close()
            
            logger.info(f"Loaded PDF: {path.name} ({len(doc)} pages)")
            
            return {
                "full_text": full_text,
                "pages": pages_data,
                "metadata": metadata
            }
        
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            raise
    
    def load_multiple_pdfs(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Load multiple PDF files.
        
        Args:
            file_paths: List of PDF file paths
        
        Returns:
            List of document dictionaries
        """
        documents = []
        
        for i, file_path in enumerate(file_paths):
            try:
                doc = self.load_pdf(file_path)
                documents.append(doc)
                logger.info(f"Processed {i + 1}/{len(file_paths)} PDFs")
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
        
        return documents
    
    def extract_by_chapter(
        self, 
        file_path: str, 
        chapter_markers: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract text organized by chapters (based on markers).
        
        Args:
            file_path: Path to PDF
            chapter_markers: List of strings that indicate chapter starts
        
        Returns:
            List of chapter dictionaries
        """
        if not chapter_markers:
            chapter_markers = ["Chapter", "CHAPTER", "Unit", "UNIT"]
        
        doc_data = self.load_pdf(file_path)
        full_text = doc_data["full_text"]
        
        # Simple chapter detection (can be improved)
        chapters = []
        current_chapter = {"title": "Introduction", "text": "", "start_page": 1}
        
        for page_data in doc_data["pages"]:
            page_text = page_data["text"]
            page_num = page_data["page_number"]
            
            # Check if page starts a new chapter
            is_new_chapter = False
            for marker in chapter_markers:
                if page_text.strip().startswith(marker):
                    is_new_chapter = True
                    # Save previous chapter
                    if current_chapter["text"]:
                        chapters.append(current_chapter)
                    
                    # Start new chapter
                    first_line = page_text.split('\n')[0]
                    current_chapter = {
                        "title": first_line,
                        "text": page_text,
                        "start_page": page_num
                    }
                    break
            
            if not is_new_chapter:
                current_chapter["text"] += f"\n{page_text}"
        
        # Add last chapter
        if current_chapter["text"]:
            chapters.append(current_chapter)
        
        logger.info(f"Extracted {len(chapters)} chapters from {Path(file_path).name}")
        return chapters
