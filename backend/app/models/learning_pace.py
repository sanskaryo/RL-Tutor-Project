"""
Learning Pace Models
Tracks student learning speed, time-on-task, and difficulty preferences
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class LearningPace(Base):
    """
    Tracks a student's learning pace and difficulty preferences
    
    Attributes:
        student_id: Foreign key to Student
        avg_speed: Average speed compared to baseline (1.0 = normal, >1 = fast, <1 = slow)
        difficulty_preference: Preferred difficulty level (1-10)
        fast_track_mode: Boolean indicating if student prefers accelerated learning
        deep_dive_mode: Boolean indicating if student prefers thorough learning
        time_on_task_data: JSON storing concept-wise time spent
        total_concepts_completed: Count of completed concepts
        avg_time_per_concept_seconds: Average time spent per concept
        completion_rate: Percentage of concepts completed successfully
        adjustment_history: JSON array tracking difficulty adjustments over time
        last_analyzed: Timestamp of last pace analysis
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """
    __tablename__ = "learning_pace"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    
    # Pace metrics
    avg_speed = Column(Float, default=1.0)  # 1.0 = baseline, >1 = faster, <1 = slower
    difficulty_preference = Column(Integer, default=5)  # 1-10 scale
    fast_track_mode = Column(Boolean, default=False)
    deep_dive_mode = Column(Boolean, default=False)
    
    # Time tracking
    time_on_task_data = Column(JSON, default=dict)  # {concept: avg_time_seconds}
    total_concepts_completed = Column(Integer, default=0)
    avg_time_per_concept_seconds = Column(Float, default=0.0)
    completion_rate = Column(Float, default=0.0)  # Percentage 0-100
    
    # Adjustment history
    adjustment_history = Column(JSON, default=list)  # [{date, from_difficulty, to_difficulty, reason}]
    last_analyzed = Column(DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="learning_pace")
    
    def __repr__(self):
        return f"<LearningPace(student_id={self.student_id}, avg_speed={self.avg_speed}, difficulty={self.difficulty_preference})>"
    
    def get_pace_category(self) -> str:
        """Categorize learning pace"""
        if self.avg_speed >= 1.5:
            return "very_fast"
        elif self.avg_speed >= 1.2:
            return "fast"
        elif self.avg_speed >= 0.8:
            return "normal"
        elif self.avg_speed >= 0.6:
            return "slow"
        else:
            return "very_slow"
    
    def get_recommended_difficulty(self) -> int:
        """Get recommended difficulty based on pace and preferences"""
        base_difficulty = self.difficulty_preference
        
        # Adjust based on pace
        if self.fast_track_mode:
            base_difficulty = min(10, base_difficulty + 2)
        elif self.deep_dive_mode:
            base_difficulty = max(1, base_difficulty - 1)
        
        # Adjust based on completion rate
        if self.completion_rate < 50:
            base_difficulty = max(1, base_difficulty - 2)
        elif self.completion_rate > 85:
            base_difficulty = min(10, base_difficulty + 1)
        
        return base_difficulty
    
    def should_increase_difficulty(self) -> bool:
        """Determine if difficulty should be increased"""
        return (
            self.avg_speed > 1.3 and 
            self.completion_rate > 80 and
            self.difficulty_preference < 10
        )
    
    def should_decrease_difficulty(self) -> bool:
        """Determine if difficulty should be decreased"""
        return (
            self.avg_speed < 0.7 or
            self.completion_rate < 50 and
            self.difficulty_preference > 1
        )


class ConceptTimeLog(Base):
    """
    Detailed time tracking per concept per session
    
    Attributes:
        session_id: Foreign key to LearningSession
        student_id: Foreign key to Student
        concept_name: Name of the concept/topic
        start_time: When student started the concept
        end_time: When student finished the concept
        time_spent_seconds: Total time spent on this concept
        performance_score: Score achieved (0-10)
        difficulty_level: Difficulty level of the content (1-10)
        completed: Whether the concept was fully completed
    """
    __tablename__ = "concept_time_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Concept details
    concept_name = Column(String(200), nullable=False)
    difficulty_level = Column(Integer, default=5)
    
    # Time tracking
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    
    # Performance
    performance_score = Column(Float, default=0.0)
    completed = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("LearningSession", back_populates="concept_time_logs")
    student = relationship("Student")
    
    def __repr__(self):
        return f"<ConceptTimeLog(concept={self.concept_name}, time={self.time_spent_seconds}s, score={self.performance_score})>"
    
    def calculate_time_spent(self):
        """Calculate and update time spent"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            self.time_spent_seconds = int(delta.total_seconds())
        return self.time_spent_seconds
    
    def get_pace_compared_to_baseline(self, baseline_seconds: int) -> float:
        """
        Compare time spent to baseline
        Returns: speed multiplier (1.0 = baseline, >1 = faster, <1 = slower)
        """
        if self.time_spent_seconds == 0 or baseline_seconds == 0:
            return 1.0
        
        # Speed = baseline / actual (faster = higher number)
        speed = baseline_seconds / self.time_spent_seconds
        return round(speed, 2)
