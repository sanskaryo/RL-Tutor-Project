"""
Skill Gap Analysis Model
Tracks identified skill gaps and learning prerequisites
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SkillGap(Base):
    """Student skill gap assessment"""
    __tablename__ = "skill_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Gap identification
    topic = Column(String, nullable=False, index=True)  # e.g., "algebra", "calculus"
    subtopic = Column(String)  # e.g., "linear_equations", "derivatives"
    proficiency_level = Column(Float, default=0.0)  # 0.0 to 1.0
    target_level = Column(Float, default=0.8)  # Desired proficiency
    gap_severity = Column(String)  # "low", "medium", "high", "critical"
    
    # Prerequisites
    prerequisites = Column(JSON)  # List of prerequisite topics/skills
    missing_prerequisites = Column(JSON)  # Prerequisites not yet mastered
    
    # Assessment data
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    assessment_method = Column(String)  # "pre_test", "session_analysis", "manual"
    
    # Recommendations
    recommended_content_ids = Column(JSON)  # List of content IDs to address gap
    estimated_time_hours = Column(Float)  # Estimated time to close gap
    priority = Column(Integer, default=5)  # 1-10 scale
    
    # Progress tracking
    is_addressed = Column(Integer, default=0)  # Boolean: has student worked on this?
    progress_percentage = Column(Float, default=0.0)  # Progress toward closing gap
    last_practiced_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="skill_gaps")


class Skill(Base):
    """Master skill/topic tree"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    display_name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # "mathematics", "science", etc.
    
    # Hierarchy
    parent_skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    prerequisite_skill_ids = Column(JSON)  # List of skill IDs that must be learned first
    
    # Metadata
    difficulty_level = Column(Integer)  # 1-5
    estimated_time_hours = Column(Float)  # Typical time to master
    
    # Content mapping
    related_content_ids = Column(JSON)  # Content that teaches this skill
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PreAssessmentResult(Base):
    """Results from pre-assessment tests"""
    __tablename__ = "pre_assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Assessment details
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    score = Column(Float, nullable=False)  # 0.0 to 1.0
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    time_taken_seconds = Column(Integer)
    
    # Analysis
    mastery_level = Column(String)  # "beginner", "intermediate", "advanced", "expert"
    identified_gaps = Column(JSON)  # List of specific gaps found
    
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student")
    skill = relationship("Skill")


def to_dict(self):
    """Convert SkillGap to dictionary"""
    return {
        "id": self.id,
        "student_id": self.student_id,
        "topic": self.topic,
        "subtopic": self.subtopic,
        "skill_name": self.topic,  # Frontend expects skill_name
        "current_level": self.proficiency_level,  # Frontend expects current_level
        "proficiency_level": self.proficiency_level,
        "target_level": self.target_level,
        "gap_severity": self.gap_severity,
        "severity": self.gap_severity or "medium",  # Frontend expects severity
        "prerequisites": self.prerequisites or [],
        "missing_prerequisites": self.missing_prerequisites or [],
        "assessed_at": self.assessed_at.isoformat() if self.assessed_at else None,
        "created_at": self.assessed_at.isoformat() if self.assessed_at else None,  # Frontend expects created_at
        "assessment_method": self.assessment_method,
        "recommended_content_ids": self.recommended_content_ids or [],
        "recommendations": self.recommended_content_ids or [],  # Frontend expects recommendations
        "estimated_time_hours": self.estimated_time_hours or 0,
        "priority": self.priority,
        "is_addressed": bool(self.is_addressed),
        "progress_percentage": self.progress_percentage,
        "progress": self.progress_percentage,  # Frontend expects progress
        "last_practiced_at": self.last_practiced_at.isoformat() if self.last_practiced_at else None
    }


# Add to_dict method to SkillGap class
SkillGap.to_dict = to_dict
