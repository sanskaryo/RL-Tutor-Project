"""
Smart Recommendations API
Includes Multi-Armed Bandit, Collaborative Filtering, and Spaced Repetition endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.models.models import Student, Content, LearningSession
from app.models.smart_recommendations import (
    BanditState, UserInteraction, SimilarStudent,
    FlashCard, ReviewSession
)
from app.api.auth import get_current_student
from app.services.content_bandit import ContentBandit, calculate_content_reward
from app.services.collaborative_filtering import CollaborativeFiltering

router = APIRouter(prefix="/smart-recommendations", tags=["smart-recommendations"])


# ============================================================================
# MULTI-ARMED BANDIT ENDPOINTS
# ============================================================================

@router.get("/content-type")
async def get_recommended_content_type(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Get recommended content type using Multi-Armed Bandit
    
    Returns the best content type (video, text, interactive, quiz)
    based on student's historical performance with each type
    """
    # Get or create bandit state
    bandit_state = db.query(BanditState).filter(
        BanditState.student_id == current_student.id
    ).first()
    
    if not bandit_state:
        # Create new bandit state
        bandit_state = BanditState(student_id=current_student.id)
        db.add(bandit_state)
        db.commit()
        db.refresh(bandit_state)
    
    # Initialize bandit and load state
    bandit = ContentBandit(epsilon=bandit_state.epsilon)
    bandit.load_state(bandit_state)
    
    # Select content type
    recommended_type = bandit.select_content_type()
    best_type, best_value = bandit.get_best_content_type()
    
    return {
        "student_id": current_student.id,
        "recommended_content_type": recommended_type,
        "best_known_type": best_type,
        "expected_reward": round(best_value, 3),
        "arm_values": bandit.get_arm_values(),
        "arm_pulls": bandit.get_pull_counts(),
        "total_pulls": bandit.total_pulls,
        "epsilon": bandit.epsilon,
        "exploration_probability": bandit.epsilon
    }


@router.post("/content-type/feedback")
async def update_content_type_performance(
    content_type: str,
    is_correct: bool,
    time_spent: float,
    engagement_score: Optional[float] = None,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Update bandit state after content interaction
    
    Body:
        content_type: Type of content (video, text, interactive, quiz)
        is_correct: Whether student answered correctly
        time_spent: Time spent in seconds
        engagement_score: Optional engagement metric (0-1)
    """
    # Validate content type
    if content_type not in ContentBandit.CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type. Must be one of: {ContentBandit.CONTENT_TYPES}"
        )
    
    # Get or create bandit state
    bandit_state = db.query(BanditState).filter(
        BanditState.student_id == current_student.id
    ).first()
    
    if not bandit_state:
        bandit_state = BanditState(student_id=current_student.id)
        db.add(bandit_state)
    
    # Calculate reward
    reward = calculate_content_reward(is_correct, time_spent, engagement_score)
    
    # Update bandit
    bandit = ContentBandit(epsilon=bandit_state.epsilon)
    bandit.load_state(bandit_state)
    bandit.update(content_type, reward)
    bandit.save_state(bandit_state)
    
    db.commit()
    db.refresh(bandit_state)
    
    return {
        "message": "Bandit updated successfully",
        "content_type": content_type,
        "reward": round(reward, 3),
        "new_arm_value": round(bandit.arm_values[content_type], 3),
        "pulls": bandit.arm_pulls[content_type],
        "best_content_type": bandit.get_best_content_type()[0]
    }


@router.get("/bandit-stats")
async def get_bandit_statistics(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get detailed statistics about content type preferences"""
    bandit_state = db.query(BanditState).filter(
        BanditState.student_id == current_student.id
    ).first()
    
    if not bandit_state:
        return {
            "message": "No bandit data yet",
            "initialized": False
        }
    
    bandit = ContentBandit()
    bandit.load_state(bandit_state)
    stats = bandit.get_statistics()
    
    # Add percentage breakdown
    if stats['total_pulls'] > 0:
        pull_percentages = {
            ct: round((pulls / stats['total_pulls']) * 100, 1)
            for ct, pulls in stats['arm_pulls'].items()
        }
    else:
        pull_percentages = {ct: 0 for ct in ContentBandit.CONTENT_TYPES}
    
    return {
        "student_id": current_student.id,
        "initialized": True,
        **stats,
        "pull_percentages": pull_percentages,
        "last_updated": bandit_state.last_updated.isoformat()
    }


# ============================================================================
# COLLABORATIVE FILTERING ENDPOINTS
# ============================================================================

@router.post("/interactions")
async def record_content_interaction(
    content_id: int,
    interaction_type: str,
    rating: Optional[float] = None,
    time_spent: Optional[int] = None,
    completed: bool = False,
    score: Optional[float] = None,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Record a content interaction for collaborative filtering
    
    Body:
        content_id: ID of content
        interaction_type: 'view', 'complete', 'like', 'skip'
        rating: Optional explicit rating (0-5)
        time_spent: Time spent in seconds
        completed: Whether content was completed
        score: Performance score if applicable
    """
    # Calculate implicit rating if explicit not provided
    implicit_rating = None
    if rating is None and completed:
        # Base implicit rating on completion and score
        implicit_rating = 3.0  # Baseline
        if score is not None:
            if score >= 0.8:
                implicit_rating = 5.0
            elif score >= 0.6:
                implicit_rating = 4.0
            elif score >= 0.4:
                implicit_rating = 3.0
            else:
                implicit_rating = 2.0
    
    # Create interaction record
    interaction = UserInteraction(
        student_id=current_student.id,
        content_id=content_id,
        interaction_type=interaction_type,
        rating=rating,
        implicit_rating=implicit_rating,
        time_spent_seconds=time_spent,
        completed=completed,
        score=score
    )
    
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    
    return {
        "message": "Interaction recorded",
        "interaction_id": interaction.id,
        "implicit_rating": implicit_rating
    }


@router.get("/peer-recommendations")
async def get_peer_based_recommendations(
    top_k: int = 5,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Get content recommendations based on similar students
    
    Uses collaborative filtering to find what similar students liked
    """
    # Initialize collaborative filtering
    cf = CollaborativeFiltering(db)
    cf.build_interaction_matrix()
    
    # Get recommendations
    recommendations = cf.recommend_content(
        student_id=current_student.id,
        top_k=top_k,
        exclude_seen=True
    )
    
    if not recommendations:
        return {
            "message": "No peer recommendations available yet",
            "recommendations": []
        }
    
    # Fetch content details
    content_ids = [rec[0] for rec in recommendations]
    content_items = db.query(Content).filter(Content.id.in_(content_ids)).all()
    content_map = {c.id: c for c in content_items}
    
    result = []
    for content_id, predicted_rating in recommendations:
        if content_id in content_map:
            content = content_map[content_id]
            result.append({
                "content_id": content.id,
                "title": content.title,
                "topic": content.topic,
                "difficulty": content.difficulty,
                "content_type": content.content_type,
                "predicted_rating": round(predicted_rating, 2),
                "recommended_by": "Similar students"
            })
    
    return {
        "student_id": current_student.id,
        "recommendations": result,
        "recommendation_method": "Collaborative Filtering"
    }


@router.get("/similar-students")
async def find_similar_students(
    top_k: int = 5,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Find students with similar learning patterns"""
    # Initialize collaborative filtering
    cf = CollaborativeFiltering(db)
    cf.build_interaction_matrix()
    
    # Find similar students
    similar_students = cf.find_similar_students(
        student_id=current_student.id,
        top_k=top_k
    )
    
    if not similar_students:
        return {
            "message": "No similar students found yet",
            "similar_students": []
        }
    
    # Get student details
    student_ids = [s[0] for s in similar_students]
    students = db.query(Student).filter(Student.id.in_(student_ids)).all()
    student_map = {s.id: s for s in students}
    
    result = []
    for student_id, similarity_score in similar_students:
        if student_id in student_map:
            student = student_map[student_id]
            result.append({
                "student_id": student.id,
                "username": student.username[:10] + "***",  # Anonymize
                "similarity_score": round(similarity_score, 3)
            })
    
    return {
        "student_id": current_student.id,
        "similar_students": result
    }


@router.get("/peer-insights")
async def get_peer_learning_insights(
    top_k: int = 5,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Get insights from similar students
    Shows what content similar students struggled with or excelled at
    """
    # Initialize collaborative filtering
    cf = CollaborativeFiltering(db)
    cf.build_interaction_matrix()
    
    # Get insights
    insights = cf.get_peer_insights(
        student_id=current_student.id,
        top_k=top_k
    )
    
    if not insights:
        return {
            "message": "No peer insights available yet",
            "struggled_with": [],
            "excelled_at": []
        }
    
    # Separate into struggled vs excelled
    struggled = [i for i in insights if i['struggled']]
    excelled = [i for i in insights if i['excelled']]
    
    # Get content details
    all_content_ids = list(set([i['content_id'] for i in insights]))
    content_items = db.query(Content).filter(Content.id.in_(all_content_ids)).all()
    content_map = {c.id: c for c in content_items}
    
    def format_insight(insight):
        content = content_map.get(insight['content_id'])
        if content:
            return {
                "content_id": content.id,
                "title": content.title,
                "topic": content.topic,
                "difficulty": content.difficulty,
                "rating": round(insight['rating'], 2),
                "peer_similarity": round(insight['similarity'], 2)
            }
        return None
    
    struggled_list = [format_insight(i) for i in struggled[:top_k] if format_insight(i)]
    excelled_list = [format_insight(i) for i in excelled[:top_k] if format_insight(i)]
    
    return {
        "student_id": current_student.id,
        "struggled_with": struggled_list,
        "excelled_at": excelled_list,
        "message": f"Insights from {len(set([i['peer_id'] for i in insights]))} similar students"
    }


# ============================================================================
# SPACED REPETITION SYSTEM (SRS) ENDPOINTS
# ============================================================================

class ReviewRequest(BaseModel):
    quality: int  # 0-5 scale (SM-2 algorithm)

class FlashcardCreateRequest(BaseModel):
    concept_name: str
    question: str
    answer: str
    concept_id: Optional[int] = None
    difficulty: int = 3
    tags: List[str] = []

@router.post("/flashcards/create")
async def create_flashcard(
    request: FlashcardCreateRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Create a new flashcard for spaced repetition"""
    flashcard = FlashCard(
        student_id=current_student.id,
        concept_id=request.concept_id,
        concept_name=request.concept_name,
        question=request.question,
        answer=request.answer,
        difficulty=request.difficulty,
        tags=request.tags
    )
    
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    
    return {
        "message": "Flashcard created",
        "flashcard_id": flashcard.id,
        "next_review_date": flashcard.next_review_date.isoformat()
    }


@router.get("/flashcards/due")
async def get_due_flashcards(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all flashcards due for review"""
    now = datetime.utcnow()
    
    due_cards = db.query(FlashCard).filter(
        and_(
            FlashCard.student_id == current_student.id,
            FlashCard.next_review_date <= now
        )
    ).order_by(FlashCard.next_review_date).all()
    
    return {
        "student_id": current_student.id,
        "due_count": len(due_cards),
        "flashcards": [
            {
                "id": card.id,
                "concept_name": card.concept_name,
                "question": card.question,
                "answer": card.answer,
                "difficulty": card.difficulty,
                "interval": card.interval,
                "repetitions": card.repetitions,
                "ease_factor": round(card.ease_factor, 2),
                "streak": card.streak,
                "retention_rate": round(card.get_retention_rate(), 1),
                "next_review_date": card.next_review_date.isoformat(),
                "overdue_days": (now - card.next_review_date).days if now > card.next_review_date else 0
            }
            for card in due_cards
        ]
    }


@router.post("/flashcards/{flashcard_id}/review")
async def review_flashcard(
    flashcard_id: int,
    review: ReviewRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Review a flashcard and update SM-2 scheduling
    
    Body:
        quality: 0-5 scale
          - 0: Complete blackout
          - 1: Incorrect, but familiar
          - 2: Incorrect, but easy to recall correct answer
          - 3: Correct with difficulty
          - 4: Correct with hesitation
          - 5: Perfect response
    """
    # Get flashcard
    flashcard = db.query(FlashCard).filter(
        and_(
            FlashCard.id == flashcard_id,
            FlashCard.student_id == current_student.id
        )
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    # Validate quality
    if not 0 <= review.quality <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quality must be between 0 and 5"
        )
    
    # Update using SM-2 algorithm
    old_interval = flashcard.interval
    old_ease = flashcard.ease_factor
    
    next_review = flashcard.calculate_sm2_next_review(review.quality)
    
    db.commit()
    db.refresh(flashcard)
    
    return {
        "message": "Review recorded",
        "flashcard_id": flashcard.id,
        "quality": review.quality,
        "old_interval": old_interval,
        "new_interval": flashcard.interval,
        "old_ease_factor": round(old_ease, 2),
        "new_ease_factor": round(flashcard.ease_factor, 2),
        "next_review_date": next_review.isoformat(),
        "days_until_next_review": flashcard.interval,
        "retention_rate": round(flashcard.get_retention_rate(), 1),
        "streak": flashcard.streak
    }


@router.get("/flashcards/upcoming")
async def get_upcoming_reviews(
    days: int = 7,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get upcoming flashcard reviews for next N days"""
    now = datetime.utcnow()
    future = now + timedelta(days=days)
    
    upcoming = db.query(FlashCard).filter(
        and_(
            FlashCard.student_id == current_student.id,
            FlashCard.next_review_date > now,
            FlashCard.next_review_date <= future
        )
    ).order_by(FlashCard.next_review_date).all()
    
    # Group by day
    reviews_by_day = {}
    for card in upcoming:
        day_key = card.next_review_date.date().isoformat()
        if day_key not in reviews_by_day:
            reviews_by_day[day_key] = []
        reviews_by_day[day_key].append({
            "id": card.id,
            "concept_name": card.concept_name,
            "difficulty": card.difficulty,
            "interval": card.interval
        })
    
    return {
        "student_id": current_student.id,
        "days_ahead": days,
        "total_upcoming": len(upcoming),
        "reviews_by_day": reviews_by_day
    }


@router.get("/flashcards/stats")
async def get_flashcard_statistics(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get overall flashcard statistics"""
    # Get all flashcards
    cards = db.query(FlashCard).filter(
        FlashCard.student_id == current_student.id
    ).all()
    
    if not cards:
        return {
            "message": "No flashcards yet",
            "total_cards": 0
        }
    
    now = datetime.utcnow()
    
    # Calculate statistics
    total_cards = len(cards)
    due_cards = sum(1 for card in cards if card.is_due())
    total_reviews = sum(card.total_reviews for card in cards)
    total_correct = sum(card.correct_reviews for card in cards)
    avg_retention = sum(card.get_retention_rate() for card in cards) / total_cards if total_cards > 0 else 0
    longest_streak = max((card.streak for card in cards), default=0)
    avg_ease = sum(card.ease_factor for card in cards) / total_cards if total_cards > 0 else 2.5
    
    # Cards by interval
    intervals = [card.interval for card in cards]
    avg_interval = sum(intervals) / len(intervals) if intervals else 0
    
    return {
        "student_id": current_student.id,
        "total_cards": total_cards,
        "due_cards": due_cards,
        "upcoming_cards": total_cards - due_cards,
        "total_reviews": total_reviews,
        "total_correct": total_correct,
        "overall_accuracy": round((total_correct / total_reviews * 100) if total_reviews > 0 else 0, 1),
        "average_retention_rate": round(avg_retention, 1),
        "longest_streak": longest_streak,
        "average_ease_factor": round(avg_ease, 2),
        "average_interval_days": round(avg_interval, 1),
        "mastered_cards": sum(1 for card in cards if card.ease_factor >= 2.5 and card.repetitions >= 5)
    }


@router.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(
    flashcard_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Delete a flashcard"""
    flashcard = db.query(FlashCard).filter(
        and_(
            FlashCard.id == flashcard_id,
            FlashCard.student_id == current_student.id
        )
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    db.delete(flashcard)
    db.commit()
    
    return {"message": "Flashcard deleted"}
