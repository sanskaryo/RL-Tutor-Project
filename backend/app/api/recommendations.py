"""
Recommendations API Endpoints
Provides personalized content recommendations based on RL agent and learning style
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.models import Student, Content
from app.models.learning_style import LearningStyleProfile
from app.api.deps import get_current_student
from app.services.rl_agent import agent
from app.services.student_model import StudentModelService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/dashboard")
def get_dashboard_recommendations(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get personalized recommendations for dashboard
    Includes learning style-based tips and RL-recommended content
    """
    # Get student's knowledge state
    knowledge_state = StudentModelService.get_knowledge_state(db, current_student.id)
    
    # Get learning style profile
    learning_style_profile = db.query(LearningStyleProfile).filter(
        LearningStyleProfile.student_id == current_student.id
    ).first()
    
    # Get all available content
    available_content = db.query(Content).limit(20).all()
    content_ids = [c.id for c in available_content]
    
    # Get RL recommendations
    recommendations = []
    if content_ids:
        learning_style = learning_style_profile.dominant_style if learning_style_profile else None
        
        try:
            recommended_id, confidence = agent.get_recommended_content(
                knowledge_state,
                content_ids,
                learning_style=learning_style
            )
            
            recommended_content = db.query(Content).filter(Content.id == recommended_id).first()
            if recommended_content:
                recommendations.append({
                    "id": recommended_content.id,
                    "title": recommended_content.title,
                    "topic": recommended_content.topic,
                    "difficulty": recommended_content.difficulty,
                    "confidence": confidence,
                    "reason": f"Recommended based on your {learning_style or 'current'} learning style"
                })
        except Exception as e:
            print(f"RL recommendation error: {e}")
    
    # Get study tips based on learning style
    study_tips = []
    if learning_style_profile:
        style = learning_style_profile.dominant_style
        
        # Learning style-specific tips
        style_tips = {
            "V": [
                "Use diagrams and charts to visualize concepts",
                "Watch educational videos and animations",
                "Color-code your notes for better retention"
            ],
            "A": [
                "Listen to audio explanations and podcasts",
                "Discuss topics with study partners",
                "Read your notes aloud to reinforce learning"
            ],
            "R": [
                "Take detailed written notes",
                "Read textbooks and articles thoroughly",
                "Create summaries and lists"
            ],
            "K": [
                "Practice with hands-on problems",
                "Take frequent breaks to stay focused",
                "Use real-world examples and applications"
            ],
            "Multimodal": [
                "Combine different learning methods",
                "Experiment with various study techniques",
                "Adapt your approach based on the subject"
            ]
        }
        
        study_tips = style_tips.get(style, style_tips["Multimodal"])
    
    # Calculate knowledge gaps
    knowledge_gaps = []
    for topic in ['algebra', 'calculus', 'geometry', 'statistics']:
        score = knowledge_state.get(f'{topic}_score', 0.0)
        if score < 0.6:
            knowledge_gaps.append({
                "topic": topic.capitalize(),
                "score": score,
                "recommendation": f"Focus on {topic} - current mastery: {int(score * 100)}%"
            })
    
    return {
        "learning_style": {
            "style": learning_style_profile.dominant_style if learning_style_profile else "Not assessed",
            "visual_score": learning_style_profile.visual_score if learning_style_profile else 0,
            "auditory_score": learning_style_profile.auditory_score if learning_style_profile else 0,
            "reading_score": learning_style_profile.reading_score if learning_style_profile else 0,
            "kinesthetic_score": learning_style_profile.kinesthetic_score if learning_style_profile else 0,
        },
        "recommended_content": recommendations,
        "study_tips": study_tips[:3],  # Top 3 tips
        "knowledge_gaps": knowledge_gaps,
        "next_action": "Take the learning style quiz" if not learning_style_profile else "Start learning session"
    }
