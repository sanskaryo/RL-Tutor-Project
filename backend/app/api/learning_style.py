"""
Learning Style API Endpoints
Handles VARK learning style assessment
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List
from pydantic import BaseModel
import json
import os
from app.core.database import get_db
from app.models.models import Student
from app.models.learning_style import LearningStyleProfile
from app.api.deps import get_current_student

router = APIRouter()


class QuizAnswers(BaseModel):
    """Student's quiz answers"""
    answers: List[str]  # List of 20 answers: ["V", "A", "R", "K", ...]


class LearningStyleResponse(BaseModel):
    """Learning style assessment results"""
    visual_score: float
    auditory_score: float
    reading_score: float
    kinesthetic_score: float
    dominant_style: str
    description: str
    study_tips: List[str]
    assessed_at: str


@router.get("/quiz")
def get_learning_style_quiz():
    """Get the VARK learning style quiz questions"""
    try:
        quiz_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "data", 
            "vark_quiz.json"
        )
        with open(quiz_path, 'r') as f:
            quiz_data = json.load(f)
        return quiz_data
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Quiz data not found"
        )


@router.post("/students/{student_id}/learning-style", response_model=LearningStyleResponse)
def submit_learning_style_assessment(
    student_id: int,
    quiz_answers: QuizAnswers,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """Submit VARK quiz answers and calculate learning style"""
    
    # Verify student owns this profile
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to submit for this student"
        )
    
    # Validate answer count
    if len(quiz_answers.answers) != 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide exactly 20 answers"
        )
    
    # Calculate scores
    scores = calculate_vark_scores(quiz_answers.answers)
    dominant_style = determine_dominant_style(scores)
    
    # Get or create profile
    profile = db.query(LearningStyleProfile).filter(
        LearningStyleProfile.student_id == student_id
    ).first()
    
    if profile:
        # Update existing
        profile.visual_score = scores["V"]
        profile.auditory_score = scores["A"]
        profile.reading_score = scores["R"]
        profile.kinesthetic_score = scores["K"]
        profile.dominant_style = dominant_style
    else:
        # Create new
        profile = LearningStyleProfile(
            student_id=student_id,
            visual_score=scores["V"],
            auditory_score=scores["A"],
            reading_score=scores["R"],
            kinesthetic_score=scores["K"],
            dominant_style=dominant_style
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    # Load style descriptions
    quiz_path = os.path.join(
        os.path.dirname(__file__), 
        "..", 
        "data", 
        "vark_quiz.json"
    )
    with open(quiz_path, 'r') as f:
        quiz_data = json.load(f)
    
    style_info = quiz_data["style_descriptions"][dominant_style]
    
    return {
        "visual_score": scores["V"],
        "auditory_score": scores["A"],
        "reading_score": scores["R"],
        "kinesthetic_score": scores["K"],
        "dominant_style": dominant_style,
        "description": style_info["description"],
        "study_tips": style_info["study_tips"],
        "assessed_at": profile.assessed_at.isoformat()
    }


@router.get("/students/{student_id}/learning-style")
def get_learning_style(
    student_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """Get student's learning style profile"""
    
    # Verify student owns this profile
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    
    profile = db.query(LearningStyleProfile).filter(
        LearningStyleProfile.student_id == student_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning style not assessed yet"
        )
    
    return profile.to_dict()


def calculate_vark_scores(answers: List[str]) -> Dict[str, float]:
    """Calculate percentage scores for each learning style"""
    counts = {"V": 0, "A": 0, "R": 0, "K": 0}
    
    for answer in answers:
        if answer in counts:
            counts[answer] += 1
    
    total = sum(counts.values())
    if total == 0:
        return {"V": 25.0, "A": 25.0, "R": 25.0, "K": 25.0}
    
    scores = {
        style: round((count / total) * 100, 2)
        for style, count in counts.items()
    }
    
    return scores


def determine_dominant_style(scores: Dict[str, float]) -> str:
    """Determine dominant learning style from scores"""
    max_score = max(scores.values())
    
    # Count how many styles have the max score
    dominant_styles = [style for style, score in scores.items() if score == max_score]
    
    # If more than one style is dominant, it's multimodal
    if len(dominant_styles) > 1:
        return "Multimodal"
    
    # If one style is clearly dominant (>35%), return it
    if max_score > 35:
        return dominant_styles[0]
    
    # If scores are relatively balanced (all within 10% of each other)
    min_score = min(scores.values())
    if (max_score - min_score) < 15:
        return "Multimodal"
    
    return dominant_styles[0]
