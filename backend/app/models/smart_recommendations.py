"""
Smart Recommendations Models
Includes Multi-Armed Bandit, Collaborative Filtering, and Spaced Repetition
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.core.database import Base


class BanditState(Base):
    """
    Multi-Armed Bandit state for content type optimization
    Tracks which content types (video, text, interactive, quiz) work best for each student
    """
    __tablename__ = "bandit_states"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    
    # Arm values (expected rewards) for each content type
    video_arm_value = Column(Float, default=0.5)
    text_arm_value = Column(Float, default=0.5)
    interactive_arm_value = Column(Float, default=0.5)
    quiz_arm_value = Column(Float, default=0.5)
    
    # Pull counts for each arm
    video_pulls = Column(Integer, default=0)
    text_pulls = Column(Integer, default=0)
    interactive_pulls = Column(Integer, default=0)
    quiz_pulls = Column(Integer, default=0)
    
    # Total rewards accumulated
    video_total_reward = Column(Float, default=0.0)
    text_total_reward = Column(Float, default=0.0)
    interactive_total_reward = Column(Float, default=0.0)
    quiz_total_reward = Column(Float, default=0.0)
    
    # Exploration parameters
    epsilon = Column(Float, default=0.1)  # Exploration rate
    total_pulls = Column(Integer, default=0)
    
    # Contextual features (JSON)
    contextual_data = Column(JSON, default=dict)  # Time of day preferences, etc.
    
    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="bandit_state")
    
    def __repr__(self):
        return f"<BanditState(student_id={self.student_id}, total_pulls={self.total_pulls})>"
    
    def get_best_content_type(self) -> str:
        """Get content type with highest expected reward"""
        arms = {
            'video': self.video_arm_value,
            'text': self.text_arm_value,
            'interactive': self.interactive_arm_value,
            'quiz': self.quiz_arm_value
        }
        return max(arms, key=arms.get)
    
    def get_arm_values(self) -> dict:
        """Get all arm values"""
        return {
            'video': self.video_arm_value,
            'text': self.text_arm_value,
            'interactive': self.interactive_arm_value,
            'quiz': self.quiz_arm_value
        }
    
    def get_pull_counts(self) -> dict:
        """Get all pull counts"""
        return {
            'video': self.video_pulls,
            'text': self.text_pulls,
            'interactive': self.interactive_pulls,
            'quiz': self.quiz_pulls
        }


class UserInteraction(Base):
    """
    Track user interactions with content for collaborative filtering
    """
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Interaction type
    interaction_type = Column(String(50))  # 'view', 'complete', 'like', 'skip'
    
    # Rating/score
    rating = Column(Float)  # 0-5 explicit rating
    implicit_rating = Column(Float)  # Calculated from behavior
    
    # Time spent
    time_spent_seconds = Column(Integer)
    completed = Column(Boolean, default=False)
    
    # Performance
    score = Column(Float)  # How well they did
    
    # Timestamps
    interaction_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")
    content = relationship("Content")
    
    def __repr__(self):
        return f"<UserInteraction(student={self.student_id}, content={self.content_id}, type={self.interaction_type})>"


class SimilarStudent(Base):
    """
    Store similar student pairs for collaborative filtering
    """
    __tablename__ = "similar_students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    similar_to_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Similarity metrics
    similarity_score = Column(Float)  # Cosine similarity (0-1)
    
    # Feature similarities
    performance_similarity = Column(Float)
    pace_similarity = Column(Float)
    style_similarity = Column(Float)
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SimilarStudent(student={self.student_id}, similar_to={self.similar_to_id}, score={self.similarity_score})>"


class FlashCard(Base):
    """
    Spaced Repetition System (SRS) flashcards using SM-2 algorithm
    """
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Card content
    concept_id = Column(Integer, ForeignKey("content.id"))
    concept_name = Column(String(200), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # SM-2 algorithm parameters
    interval = Column(Integer, default=1)  # Days until next review
    repetitions = Column(Integer, default=0)  # Number of successful reviews
    ease_factor = Column(Float, default=2.5)  # Ease factor (minimum 1.3)
    
    # Review scheduling
    next_review_date = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    
    # Performance tracking
    total_reviews = Column(Integer, default=0)
    correct_reviews = Column(Integer, default=0)
    streak = Column(Integer, default=0)  # Current correct streak
    
    # Card metadata
    difficulty = Column(Integer, default=3)  # 1-5 scale
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")
    concept = relationship("Content")
    
    def __repr__(self):
        return f"<FlashCard(student={self.student_id}, concept={self.concept_name}, next_review={self.next_review_date})>"
    
    def is_due(self) -> bool:
        """Check if card is due for review"""
        return datetime.utcnow() >= self.next_review_date
    
    def calculate_sm2_next_review(self, quality: int):
        """
        Calculate next review date using SM-2 algorithm
        
        Args:
            quality: 0-5 scale (0=complete blackout, 5=perfect response)
        
        SM-2 Algorithm:
        - EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        - If q < 3: repetitions = 0, interval = 1
        - If q >= 3:
            - If repetitions = 0: interval = 1
            - If repetitions = 1: interval = 6
            - If repetitions > 1: interval = interval * EF
        """
        # Update ease factor
        self.ease_factor = self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        self.ease_factor = max(1.3, self.ease_factor)  # Minimum ease factor
        
        # Update interval based on quality
        if quality < 3:
            # Incorrect response - restart
            self.repetitions = 0
            self.interval = 1
            self.streak = 0
        else:
            # Correct response
            self.correct_reviews += 1
            self.streak += 1
            
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
        
        # Update review tracking
        self.total_reviews += 1
        self.last_reviewed = datetime.utcnow()
        self.next_review_date = datetime.utcnow() + timedelta(days=self.interval)
        
        return self.next_review_date
    
    def get_retention_rate(self) -> float:
        """Calculate retention rate"""
        if self.total_reviews == 0:
            return 0.0
        return (self.correct_reviews / self.total_reviews) * 100


class ReviewSession(Base):
    """
    Track flashcard review sessions
    """
    __tablename__ = "review_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Session details
    cards_reviewed = Column(Integer, default=0)
    cards_correct = Column(Integer, default=0)
    session_duration_seconds = Column(Integer)
    
    # Performance
    average_quality = Column(Float)  # Average quality score (0-5)
    accuracy_rate = Column(Float)  # Percentage correct
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    student = relationship("Student")
    
    def __repr__(self):
        return f"<ReviewSession(student={self.student_id}, cards={self.cards_reviewed}, accuracy={self.accuracy_rate})>"
