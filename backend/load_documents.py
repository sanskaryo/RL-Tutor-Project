"""
Load JEE study materials into MongoDB vector database.

Usage:
    python load_documents.py

Make sure to:
1. Set GEMINI_API_KEY in .env file
2. Set MONGODB_URI in .env file
3. Place PDF files in data/documents/ directory
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.rag.embedder import GeminiEmbedder
from app.services.rag.chunker import TextChunker
from app.services.rag.document_loader import PDFDocumentLoader
from app.services.rag.retriever import VectorRetriever

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


def load_documents_from_directory(pdf_dir: str, subject: str):
    """
    Load all PDFs from a directory into the vector database.
    
    Args:
        pdf_dir: Path to directory containing PDF files
        subject: Subject name (Physics, Chemistry, Mathematics)
    """
    
    # Initialize services
    api_key = os.getenv("GEMINI_API_KEY")
    mongodb_uri = os.getenv("MONGODB_URI")
    
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables")
        return
    
    if not mongodb_uri:
        logger.error("MONGODB_URI not found in environment variables")
        return
    
    logger.info(f"Initializing services for subject: {subject}")
    
    embedder = GeminiEmbedder(api_key=api_key)
    chunker = TextChunker(chunk_size=500, chunk_overlap=50)
    loader = PDFDocumentLoader()
    retriever = VectorRetriever(mongodb_uri=mongodb_uri)
    
    # Get all PDF files
    pdf_path = Path(pdf_dir)
    if not pdf_path.exists():
        logger.warning(f"Directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_path.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {pdf_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF(s) in {pdf_dir}")
    
    total_chunks_inserted = 0
    
    for pdf_file in pdf_files:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {pdf_file.name}")
            logger.info(f"{'='*60}")
            
            # Load PDF
            doc_data = loader.load_pdf(str(pdf_file))
            logger.info(f"Loaded {doc_data['metadata']['page_count']} pages")
            
            # Chunk the text
            chunks = chunker.chunk_text(
                doc_data["full_text"],
                metadata={
                    "filename": pdf_file.name,
                    "subject": subject,
                    "source": f"NCERT - {pdf_file.stem}",
                    "page_count": doc_data['metadata']['page_count']
                }
            )
            
            logger.info(f"Created {len(chunks)} chunks")
            
            # Generate embeddings and prepare for insertion
            documents_to_insert = []
            
            for i, chunk in enumerate(chunks):
                # Progress indicator
                if (i + 1) % 10 == 0 or i == 0:
                    logger.info(f"Embedding chunk {i+1}/{len(chunks)}...")
                
                try:
                    embedding = embedder.embed_text(chunk["text"])
                    
                    doc = {
                        "text": chunk["text"],
                        "embedding": embedding,
                        "metadata": chunk["metadata"],
                        "chunk_id": chunk["chunk_id"],
                        "token_count": chunk["token_count"]
                    }
                    documents_to_insert.append(doc)
                
                except Exception as e:
                    logger.error(f"Error embedding chunk {i}: {e}")
                    continue
            
            # Insert into MongoDB
            logger.info(f"Inserting {len(documents_to_insert)} chunks into MongoDB...")
            inserted_count = retriever.insert_chunks(documents_to_insert)
            total_chunks_inserted += inserted_count
            
            logger.info(f"✅ Completed: {pdf_file.name} ({inserted_count} chunks)")
        
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf_file.name}: {e}")
            continue
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎉 Processing complete!")
    logger.info(f"Total chunks inserted: {total_chunks_inserted}")
    logger.info(f"{'='*60}\n")
    
    # Show stats
    stats = retriever.get_collection_stats()
    logger.info(f"Database stats: {stats}")
    
    retriever.close()


def main():
    """Main function to load all subjects."""
    
    logger.info("="*60)
    logger.info("JEE Study Materials Loader")
    logger.info("="*60)
    
    # Define directories for each subject
    subjects_config = [
        ("data/documents/physics", "Physics"),
        ("data/documents/chemistry", "Chemistry"),
        ("data/documents/math", "Mathematics"),
    ]
    
    for pdf_dir, subject in subjects_config:
        load_documents_from_directory(pdf_dir, subject)
    
    logger.info("\n✨ All subjects processed successfully!")
    logger.info("\nNext steps:")
    logger.info("1. Verify data in MongoDB Atlas UI")
    logger.info("2. Check vector index status (should be 'Active')")
    logger.info("3. Start the backend server: uvicorn main:app --reload")
    logger.info("4. Test the API: curl http://localhost:8002/api/v1/doubt/stats")


if __name__ == "__main__":
    main()
