"""
Learning Style Profile Model
Tracks student VARK learning style assessment results
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class LearningStyleProfile(Base):
    """Student learning style profile based on VARK model"""
    __tablename__ = "learning_style_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True)
    
    # VARK Scores (0-100 percentage)
    visual_score = Column(Float, default=0.0)
    auditory_score = Column(Float, default=0.0)
    reading_score = Column(Float, default=0.0)
    kinesthetic_score = Column(Float, default=0.0)
    
    # Dominant style(s)
    dominant_style = Column(String, nullable=False)  # "V", "A", "R", "K", or "Multimodal"
    
    # Assessment metadata
    assessed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="learning_style_profile")
    
    def __repr__(self):
        return f"<LearningStyleProfile(student_id={self.student_id}, dominant={self.dominant_style})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "visual_score": round(self.visual_score, 2),
            "auditory_score": round(self.auditory_score, 2),
            "reading_score": round(self.reading_score, 2),
            "kinesthetic_score": round(self.kinesthetic_score, 2),
            "dominant_style": self.dominant_style,
            "assessed_at": self.assessed_at.isoformat() if self.assessed_at else None,
            "recommendations": self.get_study_recommendations()
        }
    
    def get_study_recommendations(self):
        """Get personalized study tips based on learning style"""
        recommendations = {
            "V": [
                "Use diagrams, charts, and mind maps",
                "Watch video lectures and demonstrations",
                "Color-code your notes and highlight key concepts",
                "Use flashcards with images"
            ],
            "A": [
                "Listen to audio lectures and podcasts",
                "Discuss concepts with study partners",
                "Record yourself explaining topics",
                "Use text-to-speech for reading materials"
            ],
            "R": [
                "Take detailed written notes",
                "Read textbooks and articles thoroughly",
                "Create lists and written summaries",
                "Write essays to solidify understanding"
            ],
            "K": [
                "Do hands-on practice and experiments",
                "Take frequent breaks and move around",
                "Use real-world examples and case studies",
                "Build models or create physical representations"
            ],
            "Multimodal": [
                "Combine multiple learning methods",
                "Use a variety of resources (videos, texts, practice)",
                "Adapt your study method to the content type",
                "Experiment to find what works best for each topic"
            ]
        }
        
        return recommendations.get(self.dominant_style, recommendations["Multimodal"])
