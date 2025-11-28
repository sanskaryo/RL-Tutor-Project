"""
FastAPI Main Application - RL Educational Tutor Backend
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.database import init_db
from app.api import (
    auth, session, analytics, learning_style, students, 
    recommendations, skill_gaps, learning_pace, smart_recommendations, mastery,
    doubt_solver, mindmap, rl_quiz  # New: RAG-powered doubt solver and mind map
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for RL-Based Personalized Educational Tutor",
    version="1.0.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(session.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(learning_style.router, prefix=settings.API_V1_STR, tags=["Learning Style"])
app.include_router(students.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(skill_gaps.router, prefix=settings.API_V1_STR)
app.include_router(learning_pace.router, prefix=settings.API_V1_STR)
app.include_router(smart_recommendations.router, prefix=settings.API_V1_STR)
app.include_router(rl_quiz.router, prefix=settings.API_V1_STR + "/rl-quiz", tags=["RL Quiz"])
app.include_router(mastery.router, prefix=settings.API_V1_STR)
app.include_router(doubt_solver.router, prefix=settings.API_V1_STR)  # New: Doubt Solver
app.include_router(mindmap.router, prefix=settings.API_V1_STR)  # New: Mind Map


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    print("[+] Database initialized")
    print(f"[+] Server starting on {settings.API_V1_STR}")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "RL Educational Tutor API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
