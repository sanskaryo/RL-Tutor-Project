"""
Database models for RL Educational Tutor
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Student(Base):
    """Student/User model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sessions = relationship("LearningSession", back_populates="student")
    knowledge = relationship("StudentKnowledge", back_populates="student", uselist=False)
    learning_style_profile = relationship("LearningStyleProfile", back_populates="student", uselist=False)
    skill_gaps = relationship("SkillGap", back_populates="student")
    learning_pace = relationship("LearningPace", back_populates="student", uselist=False)
    bandit_state = relationship("BanditState", back_populates="student", uselist=False)
    skill_mastery = relationship("app.models.mastery.StudentMastery", back_populates="student")
    badges = relationship("app.models.mastery.StudentBadge", back_populates="student")
    study_plans = relationship("app.models.mastery.StudyPlan", back_populates="student")


class Content(Base):
    """Educational content (questions, materials)"""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    topic = Column(String, index=True)  # e.g., "algebra", "calculus"
    difficulty = Column(Integer)  # 1-5 scale
    content_type = Column(String)  # "question", "lesson", "quiz"
    question_text = Column(Text)
    correct_answer = Column(String)
    options = Column(JSON)  # For multiple choice
    explanation = Column(Text)
    tags = Column(JSON)  # ["linear_equations", "beginner"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sessions = relationship("LearningSession", back_populates="content")


class LearningSession(Base):
    """Track individual learning interactions"""
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    content_id = Column(Integer, ForeignKey("content.id"))
    
    # Interaction data
    student_answer = Column(String)
    is_correct = Column(Boolean)
    time_spent = Column(Float)  # seconds
    attempts = Column(Integer, default=1)
    hint_used = Column(Boolean, default=False)
    
    # Time tracking for pace detection
    concept_name = Column(String)  # Name of the concept being learned
    start_time = Column(DateTime(timezone=True))  # Session start time
    end_time = Column(DateTime(timezone=True))  # Session end time
    time_spent_seconds = Column(Integer, default=0)  # Calculated time spent
    
    # RL data
    state_before = Column(JSON)  # Student state before interaction
    action_taken = Column(JSON)  # Content selection decision
    reward = Column(Float)  # Calculated reward
    state_after = Column(JSON)  # Student state after interaction
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="sessions")
    content = relationship("Content", back_populates="sessions")
    concept_time_logs = relationship("ConceptTimeLog", back_populates="session")


class StudentKnowledge(Base):
    """Track student's knowledge state"""
    __tablename__ = "student_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    
    # Knowledge vectors by JEE topics (JSON format)
    # Physics topics
    mechanics_score = Column(Float, default=0.5)
    electromagnetism_score = Column(Float, default=0.5)
    optics_score = Column(Float, default=0.5)
    modern_physics_score = Column(Float, default=0.5)
    
    # Chemistry topics
    physical_chemistry_score = Column(Float, default=0.5)
    organic_chemistry_score = Column(Float, default=0.5)
    inorganic_chemistry_score = Column(Float, default=0.5)
    
    # Mathematics topics
    algebra_score = Column(Float, default=0.5)
    calculus_score = Column(Float, default=0.5)
    coordinate_geometry_score = Column(Float, default=0.5)
    trigonometry_score = Column(Float, default=0.5)
    vectors_score = Column(Float, default=0.5)
    probability_score = Column(Float, default=0.5)
    
    # Learning metrics
    total_attempts = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    average_time = Column(Float, default=0.0)
    preferred_difficulty = Column(Integer, default=2)
    learning_style = Column(String, default="balanced")  # visual, auditory, kinesthetic, balanced
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="knowledge")


class PerformanceMetrics(Base):
    """Aggregate performance metrics for analytics"""
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    # Daily/weekly metrics
    date = Column(DateTime(timezone=True))
    questions_attempted = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)
    average_difficulty = Column(Float)
    total_time_spent = Column(Float)  # minutes
    topics_covered = Column(JSON)
    
    # Progress indicators
    skill_improvement = Column(Float)  # % improvement
    streak_days = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
