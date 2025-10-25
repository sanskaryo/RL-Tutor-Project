"""
Collaborative Filtering Engine
Implements user-based collaborative filtering with cosine similarity
"""
import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
import math


class CollaborativeFiltering:
    """
    User-based collaborative filtering for content recommendations
    Uses cosine similarity to find similar students
    """
    
    def __init__(self, db: Session):
        """
        Initialize collaborative filtering engine
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_item_matrix = {}
        self.similarity_cache = {}
    
    def build_interaction_matrix(self, student_ids: List[int] = None):
        """
        Build user-item interaction matrix from database
        
        Args:
            student_ids: List of student IDs to include (None = all students)
        
        Matrix structure: {student_id: {content_id: rating}}
        """
        from app.models.smart_recommendations import UserInteraction
        
        # Query interactions
        query = self.db.query(UserInteraction)
        if student_ids:
            query = query.filter(UserInteraction.student_id.in_(student_ids))
        
        interactions = query.all()
        
        # Build matrix
        self.user_item_matrix = {}
        for interaction in interactions:
            if interaction.student_id not in self.user_item_matrix:
                self.user_item_matrix[interaction.student_id] = {}
            
            # Use implicit rating if explicit rating not available
            rating = interaction.rating if interaction.rating else interaction.implicit_rating
            if rating:
                self.user_item_matrix[interaction.student_id][interaction.content_id] = rating
    
    def calculate_cosine_similarity(
        self,
        student1_id: int,
        student2_id: int
    ) -> float:
        """
        Calculate cosine similarity between two students
        
        Args:
            student1_id: First student ID
            student2_id: Second student ID
        
        Returns:
            Cosine similarity (0-1 scale, 1 = most similar)
        """
        # Check cache
        cache_key = tuple(sorted([student1_id, student2_id]))
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
        
        # Get interaction vectors
        if student1_id not in self.user_item_matrix or student2_id not in self.user_item_matrix:
            return 0.0
        
        student1_ratings = self.user_item_matrix[student1_id]
        student2_ratings = self.user_item_matrix[student2_id]
        
        # Find common items
        common_items = set(student1_ratings.keys()) & set(student2_ratings.keys())
        
        if not common_items:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(
            student1_ratings[item] * student2_ratings[item]
            for item in common_items
        )
        
        magnitude1 = math.sqrt(sum(
            student1_ratings[item] ** 2
            for item in common_items
        ))
        
        magnitude2 = math.sqrt(sum(
            student2_ratings[item] ** 2
            for item in common_items
        ))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Cache result
        self.similarity_cache[cache_key] = similarity
        
        return similarity
    
    def find_similar_students(
        self,
        student_id: int,
        top_k: int = 10,
        min_similarity: float = 0.3
    ) -> List[Tuple[int, float]]:
        """
        Find K most similar students
        
        Args:
            student_id: Target student ID
            top_k: Number of similar students to return
            min_similarity: Minimum similarity threshold
        
        Returns:
            List of (student_id, similarity_score) tuples
        """
        if student_id not in self.user_item_matrix:
            return []
        
        similarities = []
        
        for other_student_id in self.user_item_matrix.keys():
            if other_student_id == student_id:
                continue
            
            similarity = self.calculate_cosine_similarity(student_id, other_student_id)
            
            if similarity >= min_similarity:
                similarities.append((other_student_id, similarity))
        
        # Sort by similarity (descending) and return top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def recommend_content(
        self,
        student_id: int,
        top_k: int = 5,
        exclude_seen: bool = True
    ) -> List[Tuple[int, float]]:
        """
        Recommend content based on similar students' preferences
        
        Args:
            student_id: Target student ID
            top_k: Number of recommendations to return
            exclude_seen: Exclude content already seen by student
        
        Returns:
            List of (content_id, predicted_rating) tuples
        """
        # Find similar students
        similar_students = self.find_similar_students(student_id, top_k=10)
        
        if not similar_students:
            return []
        
        # Get student's already seen content
        seen_content = set()
        if exclude_seen and student_id in self.user_item_matrix:
            seen_content = set(self.user_item_matrix[student_id].keys())
        
        # Aggregate recommendations from similar students
        content_scores = {}
        
        for similar_student_id, similarity_score in similar_students:
            if similar_student_id not in self.user_item_matrix:
                continue
            
            for content_id, rating in self.user_item_matrix[similar_student_id].items():
                if exclude_seen and content_id in seen_content:
                    continue
                
                # Weight rating by similarity
                weighted_rating = rating * similarity_score
                
                if content_id not in content_scores:
                    content_scores[content_id] = {
                        'total_weight': 0.0,
                        'weighted_sum': 0.0
                    }
                
                content_scores[content_id]['weighted_sum'] += weighted_rating
                content_scores[content_id]['total_weight'] += similarity_score
        
        # Calculate predicted ratings
        recommendations = []
        for content_id, scores in content_scores.items():
            if scores['total_weight'] > 0:
                predicted_rating = scores['weighted_sum'] / scores['total_weight']
                recommendations.append((content_id, predicted_rating))
        
        # Sort by predicted rating (descending) and return top K
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_k]
    
    def calculate_feature_similarity(
        self,
        student1_data: Dict,
        student2_data: Dict
    ) -> Dict[str, float]:
        """
        Calculate similarity across different features
        
        Args:
            student1_data: Dict with student1 features (performance, pace, style, etc.)
            student2_data: Dict with student2 features
        
        Returns:
            Dict with similarity scores for each feature
        """
        similarities = {}
        
        # Performance similarity (based on average scores)
        if 'avg_score' in student1_data and 'avg_score' in student2_data:
            score_diff = abs(student1_data['avg_score'] - student2_data['avg_score'])
            similarities['performance'] = 1.0 - (score_diff / 10.0)  # Normalize to 0-1
        
        # Pace similarity (based on speed)
        if 'pace_speed' in student1_data and 'pace_speed' in student2_data:
            pace_diff = abs(student1_data['pace_speed'] - student2_data['pace_speed'])
            similarities['pace'] = 1.0 - min(pace_diff, 1.0)  # Cap difference at 1.0
        
        # Learning style similarity (categorical match)
        if 'learning_style' in student1_data and 'learning_style' in student2_data:
            similarities['style'] = 1.0 if student1_data['learning_style'] == student2_data['learning_style'] else 0.5
        
        return similarities
    
    def get_peer_insights(
        self,
        student_id: int,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Get insights from similar students (what they struggled with, succeeded at)
        
        Args:
            student_id: Target student ID
            top_k: Number of peers to analyze
        
        Returns:
            List of insights with content, difficulty, peer performance
        """
        similar_students = self.find_similar_students(student_id, top_k=top_k)
        
        if not similar_students:
            return []
        
        insights = []
        
        for similar_student_id, similarity_score in similar_students:
            if similar_student_id not in self.user_item_matrix:
                continue
            
            # Analyze their interactions
            for content_id, rating in self.user_item_matrix[similar_student_id].items():
                insights.append({
                    'peer_id': similar_student_id,
                    'similarity': similarity_score,
                    'content_id': content_id,
                    'rating': rating,
                    'struggled': rating < 3.0,
                    'excelled': rating >= 4.5
                })
        
        return insights
    
    def clear_cache(self):
        """Clear similarity cache"""
        self.similarity_cache = {}
