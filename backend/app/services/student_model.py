"""
Student Model Service - Track and update student knowledge state
"""
from sqlalchemy.orm import Session
from app.models.models import Student, StudentKnowledge, LearningSession
from typing import Dict, Optional


class StudentModelService:
    """Service for managing student knowledge state and learning profile"""
    
    @staticmethod
    def initialize_knowledge(db: Session, student_id: int) -> StudentKnowledge:
        """
        Initialize knowledge state for new student
        
        Args:
            db: Database session
            student_id: Student ID
        
        Returns:
            StudentKnowledge object
        """
        knowledge = StudentKnowledge(
            student_id=student_id,
            # Physics topics
            mechanics_score=0.5,
            electromagnetism_score=0.5,
            optics_score=0.5,
            modern_physics_score=0.5,
            # Chemistry topics
            physical_chemistry_score=0.5,
            organic_chemistry_score=0.5,
            inorganic_chemistry_score=0.5,
            # Mathematics topics
            algebra_score=0.5,
            calculus_score=0.5,
            coordinate_geometry_score=0.5,
            trigonometry_score=0.5,
            vectors_score=0.5,
            probability_score=0.5,
            # Metrics
            total_attempts=0,
            correct_answers=0,
            accuracy_rate=0.0,
            preferred_difficulty=2,
            learning_style="balanced"
        )
        db.add(knowledge)
        db.commit()
        db.refresh(knowledge)
        return knowledge
    
    @staticmethod
    def get_knowledge_state(db: Session, student_id: int) -> Dict:
        """
        Get current knowledge state as dictionary
        
        Args:
            db: Database session
            student_id: Student ID
        
        Returns:
            Knowledge state dictionary
        """
        knowledge = db.query(StudentKnowledge).filter(
            StudentKnowledge.student_id == student_id
        ).first()
        
        if not knowledge:
            knowledge = StudentModelService.initialize_knowledge(db, student_id)
        
        return {
            # Physics
            'mechanics_score': knowledge.mechanics_score,
            'electromagnetism_score': knowledge.electromagnetism_score,
            'optics_score': knowledge.optics_score,
            'modern_physics_score': knowledge.modern_physics_score,
            # Chemistry
            'physical_chemistry_score': knowledge.physical_chemistry_score,
            'organic_chemistry_score': knowledge.organic_chemistry_score,
            'inorganic_chemistry_score': knowledge.inorganic_chemistry_score,
            # Mathematics
            'algebra_score': knowledge.algebra_score,
            'calculus_score': knowledge.calculus_score,
            'coordinate_geometry_score': knowledge.coordinate_geometry_score,
            'trigonometry_score': knowledge.trigonometry_score,
            'vectors_score': knowledge.vectors_score,
            'probability_score': knowledge.probability_score,
            # Metrics
            'accuracy_rate': knowledge.accuracy_rate,
            'preferred_difficulty': knowledge.preferred_difficulty,
            'learning_style': knowledge.learning_style,
            'total_attempts': knowledge.total_attempts,
            'correct_answers': knowledge.correct_answers
        }
    
    @staticmethod
    def update_knowledge(db: Session, 
                        student_id: int,
                        topic: str,
                        is_correct: bool,
                        difficulty: int,
                        time_spent: float) -> StudentKnowledge:
        """
        Update student knowledge based on learning interaction
        
        Args:
            db: Database session
            student_id: Student ID
            topic: Topic of content (algebra, calculus, etc.)
            is_correct: Whether answer was correct
            difficulty: Content difficulty (1-5)
            time_spent: Time spent on content
        
        Returns:
            Updated StudentKnowledge object
        """
        knowledge = db.query(StudentKnowledge).filter(
            StudentKnowledge.student_id == student_id
        ).first()
        
        if not knowledge:
            knowledge = StudentModelService.initialize_knowledge(db, student_id)
        
        # Update attempt counters
        knowledge.total_attempts += 1
        if is_correct:
            knowledge.correct_answers += 1
        
        # Update accuracy rate
        knowledge.accuracy_rate = knowledge.correct_answers / knowledge.total_attempts
        
        # Update topic-specific score using exponential moving average
        alpha = 0.2  # Learning rate for knowledge update
        score_change = alpha * (1.0 if is_correct else -0.3)
        
        # JEE topic mapping
        topic_map = {
            'mechanics': 'mechanics_score',
            'electromagnetism': 'electromagnetism_score',
            'optics': 'optics_score',
            'modern_physics': 'modern_physics_score',
            'physical_chemistry': 'physical_chemistry_score',
            'organic_chemistry': 'organic_chemistry_score',
            'inorganic_chemistry': 'inorganic_chemistry_score',
            'algebra': 'algebra_score',
            'calculus': 'calculus_score',
            'coordinate_geometry': 'coordinate_geometry_score',
            'trigonometry': 'trigonometry_score',
            'vectors': 'vectors_score',
            'probability': 'probability_score'
        }
        
        if topic in topic_map:
            current_score = getattr(knowledge, topic_map[topic])
            new_score = max(0.0, min(1.0, current_score + score_change))
            setattr(knowledge, topic_map[topic], new_score)
        
        # Update preferred difficulty based on performance
        if is_correct and difficulty == knowledge.preferred_difficulty:
            # Doing well at current level, consider increasing
            if knowledge.accuracy_rate > 0.75:
                knowledge.preferred_difficulty = min(5, knowledge.preferred_difficulty + 1)
        elif not is_correct and difficulty <= knowledge.preferred_difficulty:
            # Struggling at current level, consider decreasing
            if knowledge.accuracy_rate < 0.50:
                knowledge.preferred_difficulty = max(1, knowledge.preferred_difficulty - 1)
        
        # Update average time
        if knowledge.total_attempts == 1:
            knowledge.average_time = time_spent
        else:
            knowledge.average_time = (knowledge.average_time * 0.9 + time_spent * 0.1)
        
        db.commit()
        db.refresh(knowledge)
        
        return knowledge
    
    @staticmethod
    def get_learning_style(db: Session, student_id: int) -> str:
        """
        Determine student's learning style based on interaction patterns
        
        Args:
            db: Database session
            student_id: Student ID
        
        Returns:
            Learning style (visual, auditory, kinesthetic, balanced)
        """
        # Get recent sessions
        sessions = db.query(LearningSession).filter(
            LearningSession.student_id == student_id
        ).order_by(LearningSession.timestamp.desc()).limit(20).all()
        
        if len(sessions) < 10:
            return "balanced"
        
        # Analyze time spent and accuracy by content type
        # This is simplified - in real system would analyze more factors
        avg_time = sum(s.time_spent for s in sessions) / len(sessions)
        accuracy = sum(1 for s in sessions if s.is_correct) / len(sessions)
        
        if avg_time < 30 and accuracy > 0.7:
            return "visual"  # Quick learner, benefits from visual aids
        elif avg_time > 60:
            return "auditory"  # Takes time, benefits from explanations
        elif accuracy > 0.8:
            return "kinesthetic"  # Hands-on learner
        else:
            return "balanced"
    
    @staticmethod
    def get_progress_summary(db: Session, student_id: int) -> Dict:
        """
        Get comprehensive progress summary for student
        
        Args:
            db: Database session
            student_id: Student ID
        
        Returns:
            Progress summary dictionary
        """
        knowledge = db.query(StudentKnowledge).filter(
            StudentKnowledge.student_id == student_id
        ).first()
        
        if not knowledge:
            return {
                'total_attempts': 0,
                'accuracy_rate': 0.0,
                'topics_mastered': [],
                'areas_for_improvement': []
            }
        
        # Identify mastered topics (score > 0.7)
        topics_mastered = []
        areas_for_improvement = []
        
        # JEE topic scores
        topic_scores = {
            'mechanics': knowledge.mechanics_score,
            'electromagnetism': knowledge.electromagnetism_score,
            'optics': knowledge.optics_score,
            'modern_physics': knowledge.modern_physics_score,
            'physical_chemistry': knowledge.physical_chemistry_score,
            'organic_chemistry': knowledge.organic_chemistry_score,
            'inorganic_chemistry': knowledge.inorganic_chemistry_score,
            'algebra': knowledge.algebra_score,
            'calculus': knowledge.calculus_score,
            'coordinate_geometry': knowledge.coordinate_geometry_score,
            'trigonometry': knowledge.trigonometry_score,
            'vectors': knowledge.vectors_score,
            'probability': knowledge.probability_score
        }
        
        for topic, score in topic_scores.items():
            if score > 0.7:
                topics_mastered.append(topic)
            elif score < 0.4:
                areas_for_improvement.append(topic)
        
        return {
            'total_attempts': knowledge.total_attempts,
            'correct_answers': knowledge.correct_answers,
            'accuracy_rate': knowledge.accuracy_rate,
            'topics_mastered': topics_mastered,
            'areas_for_improvement': areas_for_improvement,
            'preferred_difficulty': knowledge.preferred_difficulty,
            'learning_style': knowledge.learning_style
        }
