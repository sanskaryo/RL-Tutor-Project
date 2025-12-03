import os
import sys
import pandas as pd
from dotenv import load_dotenv
import logging

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.rag.embedder import GeminiEmbedder
from app.services.rag.retriever import VectorRetriever
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_data():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY") or getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables.")
        return

    # Initialize services
    embedder = GeminiEmbedder(api_key=api_key)
    retriever = VectorRetriever(collection_name="questions") # Use a specific collection name

    # Load data
    csv_path = os.path.join(os.path.dirname(__file__), "../personalized_learning_rl/data/questions.csv")
    if not os.path.exists(csv_path):
        logger.error(f"Questions file not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    logger.info(f"Loaded {len(df)} questions from CSV.")

    chunks = []
    batch_size = 10 # Small batch size to avoid rate limits if any
    
    for i, row in df.iterrows():
        # Create a meaningful text representation for retrieval
        text = f"Question: {row['question_text']}\nAnswer: {row['answer']}\nSkill: {row['skill']}\nDifficulty: {row['difficulty']}"
        
        # Metadata
        metadata = {
            "id": str(row['id']),
            "skill": row['skill'],
            "difficulty": row['difficulty'],
            "type": row['question_type'],
            "subject": "Math", # Assuming Math based on content
            "text": text # Store text for retrieval
        }
        
        try:
            embedding = embedder.embed_text(text)
            chunks.append({
                "text": text,
                "embedding": embedding,
                **metadata
            })
            
            if len(chunks) >= batch_size:
                retriever.insert_chunks(chunks)
                chunks = []
                logger.info(f"Processed {i+1}/{len(df)} questions.")
                
        except Exception as e:
            logger.error(f"Error processing row {i}: {e}")
            continue

    # Insert remaining
    if chunks:
        retriever.insert_chunks(chunks)
        
    logger.info("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
