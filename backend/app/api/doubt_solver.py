"""
Doubt Solver API - RAG-powered Q&A endpoint
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from app.core.config import settings
from app.services.rag.embedder import GeminiEmbedder
from app.services.rag.retriever import VectorRetriever
from app.services.llm.gemini_client import GeminiClient
from app.services.llm.prompts import JEEPromptTemplates

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/doubt", tags=["Doubt Solver"])


# Pydantic models
class DoubtRequest(BaseModel):
    """Request model for doubt solver."""
    question: str = Field(..., min_length=5, max_length=1000, description="Student's question")
    subject: Optional[str] = Field(None, description="Subject filter (Physics, Chemistry, Math)")
    context_limit: int = Field(3, ge=1, le=10, description="Number of context chunks to retrieve")
    include_sources: bool = Field(True, description="Include source citations in response")


class SourceInfo(BaseModel):
    """Information about a source document."""
    text: str
    subject: Optional[str] = None
    chapter: Optional[str] = None
    source: Optional[str] = None
    relevance_score: float


class DoubtResponse(BaseModel):
    """Response model for doubt solver."""
    answer: str
    sources: Optional[List[SourceInfo]] = None
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    subject_detected: Optional[str] = None


# Dependency: Get initialized services
def get_rag_services():
    """Initialize and return RAG services."""
    try:
        # Get API key from settings
        gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
        mongodb_uri = getattr(settings, 'MONGODB_URI', None)
        
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured in settings")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not configured in settings")
        
        # Initialize services
        embedder = GeminiEmbedder(api_key=gemini_api_key)
        retriever = VectorRetriever(mongodb_uri=mongodb_uri)
        llm_client = GeminiClient(api_key=gemini_api_key)
        
        return {
            "embedder": embedder,
            "retriever": retriever,
            "llm": llm_client
        }
    except Exception as e:
        logger.error(f"Error initializing RAG services: {e}")
        raise HTTPException(status_code=500, detail="RAG services not available")


@router.post("/ask", response_model=DoubtResponse)
async def ask_doubt(
    request: DoubtRequest,
    services: dict = Depends(get_rag_services)
):
    """
    Ask a question and get an answer using RAG pipeline.
    
    This endpoint:
    1. Embeds the question
    2. Retrieves relevant context from vector database
    3. Generates answer using LLM with retrieved context
    4. Returns answer with source citations
    """
    try:
        embedder = services["embedder"]
        retriever = services["retriever"]
        llm_client = services["llm"]
        
        # Step 1: Embed the question
        logger.info(f"Processing question: {request.question[:50]}...")
        query_embedding = embedder.embed_query(request.question)
        
        # Step 2: Retrieve relevant context
        search_results = retriever.search(
            query_embedding=query_embedding,
            top_k=request.context_limit,
            subject_filter=request.subject,
            min_score=0.7
        )
        
        if not search_results:
            return DoubtResponse(
                answer="I couldn't find relevant information in the study materials to answer this question. Please try rephrasing or ask about a different topic.",
                confidence=0.0,
                sources=[]
            )
        
        # Step 3: Format context
        context = JEEPromptTemplates.format_context(search_results)
        
        # Step 4: Generate answer using LLM
        answer = llm_client.generate_with_context(
            question=request.question,
            context=context,
            system_instruction=JEEPromptTemplates.DOUBT_SOLVER_SYSTEM
        )
        
        # Step 5: Prepare response with sources
        sources = []
        if request.include_sources:
            for result in search_results:
                metadata = result.get("metadata", {})
                sources.append(SourceInfo(
                    text=result.get("text", "")[:200] + "...",  # First 200 chars
                    subject=metadata.get("subject"),
                    chapter=metadata.get("chapter"),
                    source=metadata.get("source"),
                    relevance_score=result.get("score", 0.0)
                ))
        
        # Calculate confidence based on retrieval scores
        avg_score = sum(r.get("score", 0) for r in search_results) / len(search_results)
        confidence = min(avg_score, 1.0)
        
        # Detect subject from top result
        subject_detected = None
        if search_results:
            subject_detected = search_results[0].get("metadata", {}).get("subject")
        
        logger.info(f"Successfully answered question (confidence: {confidence:.2f})")
        
        return DoubtResponse(
            answer=answer,
            sources=sources if request.include_sources else None,
            confidence=confidence,
            subject_detected=subject_detected
        )
    
    except Exception as e:
        logger.error(f"Error processing doubt: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@router.get("/stats")
async def get_doubt_stats(services: dict = Depends(get_rag_services)):
    """
    Get statistics about the doubt solver knowledge base.
    """
    try:
        retriever = services["retriever"]
        stats = retriever.get_collection_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving stats")


@router.get("/health")
async def health_check():
    """Health check endpoint for doubt solver service."""
    return {
        "status": "healthy",
        "service": "doubt_solver",
        "version": "1.0.0"
    }
