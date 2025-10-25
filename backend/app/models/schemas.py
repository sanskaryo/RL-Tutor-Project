"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


# ==================== AUTH SCHEMAS ====================
class StudentCreate(BaseModel):
    """Schema for student registration"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class StudentLogin(BaseModel):
    """Schema for student login"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class StudentResponse(BaseModel):
    """Student data response"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== CONTENT SCHEMAS ====================
class ContentCreate(BaseModel):
    """Schema for creating content"""
    title: str
    description: Optional[str]
    topic: str
    difficulty: int = Field(ge=1, le=5)
    content_type: str
    question_text: Optional[str]
    correct_answer: Optional[str]
    options: Optional[List[str]]
    explanation: Optional[str]
    tags: Optional[List[str]]


class ContentResponse(BaseModel):
    """Content data response"""
    id: int
    title: str
    description: Optional[str]
    topic: str
    difficulty: int
    content_type: str
    question_text: Optional[str]
    options: Optional[List[str]]
    
    class Config:
        from_attributes = True


# ==================== SESSION SCHEMAS ====================
class SessionStart(BaseModel):
    """Schema for starting a learning session"""
    topic: Optional[str] = None
    difficulty: Optional[int] = None


class AnswerSubmit(BaseModel):
    """Schema for submitting an answer"""
    session_id: int
    student_answer: str
    time_spent: float


class SessionResponse(BaseModel):
    """Learning session response"""
    id: int
    content_id: int
    is_correct: bool
    reward: float
    explanation: Optional[str]
    next_content: Optional[ContentResponse]


# ==================== STUDENT KNOWLEDGE SCHEMAS ====================
class KnowledgeState(BaseModel):
    """Student knowledge state"""
    algebra_score: float
    calculus_score: float
    geometry_score: float
    statistics_score: float
    accuracy_rate: float
    preferred_difficulty: int
    learning_style: str
    
    class Config:
        from_attributes = True


# ==================== ANALYTICS SCHEMAS ====================
class ProgressData(BaseModel):
    """Student progress analytics"""
    total_attempts: int
    correct_answers: int
    accuracy_rate: float
    topics_mastered: List[str]
    current_streak: int
    time_spent_today: float
    skill_improvements: Dict[str, float]


class DashboardData(BaseModel):
    """Complete dashboard analytics"""
    student: StudentResponse
    knowledge: KnowledgeState
    progress: ProgressData
    recent_sessions: List[Dict]
