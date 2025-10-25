"""
Mastery-Based Progression API
Handles skills, badges, and study plans.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.api.deps import get_current_student
from app.models.models import Student
from app.models.mastery import MasterySkill, StudentMastery, Badge, StudentBadge, StudyPlan
from app.services.mastery_service import MasteryService, BadgeService, StudyPlanService


router = APIRouter(prefix="/mastery", tags=["mastery"])


# ============================================================================
# Pydantic Schemas
# ============================================================================

class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: str = "beginner"
    estimated_hours: float = 1.0
    prerequisite_ids: List[int] = []


class SkillAssessment(BaseModel):
    correct: bool
    time_spent: int = 0


class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str = "achievement"
    tier: str = "bronze"
    icon: Optional[str] = None
    color: Optional[str] = None
    criteria: dict
    points: int = 10


class StudyPlanCreate(BaseModel):
    goal_type: str
    target_skills: List[int]
    target_date: datetime
    daily_minutes: int = 30
    title: Optional[str] = None
    description: Optional[str] = None


class StudyPlanAdjust(BaseModel):
    performance_data: dict


# ============================================================================
# PHASE 13.1: SKILL TREE & COMPETENCY-BASED LEARNING PATHS
# ============================================================================

@router.get("/skills/tree")
def get_skill_tree(
    include_progress: bool = True,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get complete skill tree with student progress.
    Returns nodes (skills) and edges (prerequisites).
    """
    service = MasteryService(db)
    
    student_id = current_student.id if include_progress else None
    tree = service.get_skill_tree(student_id)
    
    return {
        "tree": tree,
        "student_id": student_id
    }


@router.post("/skills/create", status_code=status.HTTP_201_CREATED)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Create a new skill in the tree.
    Admin/teacher endpoint (for demo, any user can create).
    """
    # Check for duplicate name
    existing = db.query(MasterySkill).filter(MasterySkill.name == skill_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Skill with name '{skill_data.name}' already exists"
        )
    
    # Create skill
    skill = Skill(
        name=skill_data.name,
        description=skill_data.description,
        category=skill_data.category,
        difficulty=skill_data.difficulty,
        estimated_hours=skill_data.estimated_hours
    )
    
    # Add prerequisites
    if skill_data.prerequisite_ids:
        prerequisites = db.query(MasterySkill).filter(
            Skill.id.in_(skill_data.prerequisite_ids)
        ).all()
        skill.prerequisites = prerequisites
    
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return {
        "skill": skill.to_dict(include_prerequisites=True),
        "message": "Skill created successfully"
    }


@router.get("/skills/{skill_id}")
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get details for a specific skill including student progress.
    """
    skill = db.query(MasterySkill).filter(MasterySkill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill {skill_id} not found"
        )
    
    # Get student mastery
    mastery = db.query(StudentMastery).filter(
        StudentMastery.student_id == current_student.id,
        StudentMastery.skill_id == skill_id
    ).first()
    
    # Check if unlocked
    is_unlocked = skill.is_unlocked_for_student(current_student.id, db)
    
    return {
        "skill": skill.to_dict(include_prerequisites=True),
        "mastery": mastery.to_dict() if mastery else None,
        "is_unlocked": is_unlocked,
        "unlocks": [{"id": s.id, "name": s.name} for s in skill.unlocks]
    }


@router.post("/skills/{skill_id}/assess")
def assess_skill(
    skill_id: int,
    assessment: SkillAssessment,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Assess student performance on a skill and update mastery level.
    Unlocks new skills if prerequisites are met.
    """
    service = MasteryService(db)
    
    try:
        result = service.assess_skill(
            student_id=current_student.id,
            skill_id=skill_id,
            correct=assessment.correct,
            time_spent=assessment.time_spent
        )
        
        # Check for new badges
        badge_service = BadgeService(db)
        new_badges = badge_service.check_and_award_badges(current_student.id)
        
        return {
            **result,
            "new_badges": new_badges
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/students/mastery")
def get_student_mastery(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get comprehensive mastery overview for current student.
    Shows total progress, skills by category, recent achievements.
    """
    service = MasteryService(db)
    overview = service.get_student_mastery_overview(current_student.id)
    
    return overview


@router.get("/students/recommendations")
def get_recommended_skills(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get recommended next skills to work on.
    Considers: unlocked status, progress, foundational importance.
    """
    service = MasteryService(db)
    recommendations = service.get_recommended_next_skills(current_student.id, limit)
    
    return {
        "recommendations": recommendations,
        "count": len(recommendations)
    }


@router.get("/skills/{skill_id}/path")
def get_learning_path(
    skill_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get optimal learning path to reach a target skill.
    Shows all prerequisites in order with time estimates.
    """
    service = MasteryService(db)
    
    try:
        path = service.get_learning_path(current_student.id, skill_id)
        return path
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ============================================================================
# PHASE 13.2: BADGES & MICRO-CREDENTIALS
# ============================================================================

@router.get("/badges")
def get_all_badges(
    category: Optional[str] = None,
    tier: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all available badges.
    Optionally filter by category or tier.
    """
    query = db.query(Badge).filter(Badge.is_active == True)
    
    if category:
        query = query.filter(Badge.category == category)
    if tier:
        query = query.filter(Badge.tier == tier)
    
    badges = query.all()
    
    return {
        "badges": [badge.to_dict() for badge in badges],
        "total": len(badges)
    }


@router.post("/badges/create", status_code=status.HTTP_201_CREATED)
def create_badge(
    badge_data: BadgeCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Create a new badge.
    Admin/teacher endpoint (for demo, any user can create).
    """
    # Check for duplicate
    existing = db.query(Badge).filter(Badge.name == badge_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Badge '{badge_data.name}' already exists"
        )
    
    badge = Badge(
        name=badge_data.name,
        description=badge_data.description,
        category=badge_data.category,
        tier=badge_data.tier,
        icon=badge_data.icon,
        color=badge_data.color,
        criteria=badge_data.criteria,
        points=badge_data.points
    )
    
    db.add(badge)
    db.commit()
    db.refresh(badge)
    
    return {
        "badge": badge.to_dict(),
        "message": "Badge created successfully"
    }


@router.get("/students/badges")
def get_student_badges(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get all badges earned by current student.
    Includes total points and breakdown by tier.
    """
    service = BadgeService(db)
    result = service.get_student_badges(current_student.id)
    
    return result


@router.post("/students/badges/check")
def check_badge_eligibility(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Check all badge criteria and award newly earned badges.
    Returns list of newly awarded badges.
    """
    service = BadgeService(db)
    new_badges = service.check_and_award_badges(current_student.id)
    
    return {
        "newly_earned": new_badges,
        "count": len(new_badges),
        "message": f"Earned {len(new_badges)} new badges!" if new_badges else "No new badges earned"
    }


@router.get("/badges/{badge_id}/verify/{verification_code}")
def verify_badge(
    badge_id: int,
    verification_code: str,
    db: Session = Depends(get_db)
):
    """
    Verify a badge certificate using verification code.
    Public endpoint for credential verification.
    """
    student_badge = db.query(StudentBadge).filter(
        StudentBadge.badge_id == badge_id,
        StudentBadge.verification_code == verification_code
    ).first()
    
    if not student_badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid verification code"
        )
    
    return {
        "valid": True,
        "student_badge": student_badge.to_dict(include_badge=True),
        "earned_at": student_badge.earned_at.isoformat() if student_badge.earned_at else None,
        "evidence": student_badge.evidence
    }


# ============================================================================
# PHASE 13.3: PERSONALIZED STUDY PLANS
# ============================================================================

@router.post("/study-plans/generate", status_code=status.HTTP_201_CREATED)
def generate_study_plan(
    plan_data: StudyPlanCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Generate AI-powered personalized study plan.
    Considers goals, time constraints, and skill dependencies.
    """
    service = StudyPlanService(db)
    
    try:
        result = service.generate_plan(
            student_id=current_student.id,
            goal_type=plan_data.goal_type,
            target_skills=plan_data.target_skills,
            target_date=plan_data.target_date,
            daily_minutes=plan_data.daily_minutes
        )
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/study-plans")
def get_student_study_plans(
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get all study plans for current student.
    """
    query = db.query(StudyPlan).filter(
        StudyPlan.student_id == current_student.id
    )
    
    if active_only:
        query = query.filter(StudyPlan.is_active == True)
    
    plans = query.all()
    
    return {
        "plans": [plan.to_dict() for plan in plans],
        "total": len(plans)
    }


@router.get("/study-plans/{plan_id}")
def get_study_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get detailed study plan with schedule.
    """
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.student_id == current_student.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study plan {plan_id} not found"
        )
    
    # Update progress
    plan.calculate_progress(db)
    db.commit()
    
    return {
        "plan": plan.to_dict(),
        "expected_progress": plan.expected_progress(),
        "performance_trend": plan.performance_trend
    }


@router.put("/study-plans/{plan_id}/adjust")
def adjust_study_plan(
    plan_id: int,
    adjustment: StudyPlanAdjust,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Adjust study plan based on performance.
    Automatically adapts schedule if student is ahead/behind.
    """
    # Verify ownership
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.student_id == current_student.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study plan {plan_id} not found"
        )
    
    service = StudyPlanService(db)
    
    try:
        result = service.adjust_plan(plan_id, adjustment.performance_data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/study-plans/today/tasks")
def get_today_tasks(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get today's study tasks from all active plans.
    Shows what student should work on today.
    """
    service = StudyPlanService(db)
    tasks = service.get_today_tasks(current_student.id)
    
    return tasks


@router.delete("/study-plans/{plan_id}")
def delete_study_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Delete or deactivate a study plan.
    """
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.student_id == current_student.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study plan {plan_id} not found"
        )
    
    # Soft delete - just deactivate
    plan.is_active = False
    plan.status = "abandoned"
    db.commit()
    
    return {
        "message": "Study plan deactivated",
        "plan_id": plan_id
    }


@router.put("/study-plans/{plan_id}/complete")
def complete_study_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Mark a study plan as completed.
    """
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.student_id == current_student.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study plan {plan_id} not found"
        )
    
    plan.status = "completed"
    plan.completed_at = datetime.now()
    plan.is_active = False
    db.commit()
    
    # Check for completion badges
    badge_service = BadgeService(db)
    new_badges = badge_service.check_and_award_badges(current_student.id)
    
    return {
        "message": "Study plan completed! 🎉",
        "plan_id": plan_id,
        "completed_at": plan.completed_at.isoformat(),
        "new_badges": new_badges
    }


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get("/stats")
def get_mastery_stats(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Get comprehensive mastery statistics for student dashboard.
    Combines skills, badges, and study plan progress.
    """
    mastery_service = MasteryService(db)
    badge_service = BadgeService(db)
    study_plan_service = StudyPlanService(db)
    
    mastery_overview = mastery_service.get_student_mastery_overview(current_student.id)
    badges = badge_service.get_student_badges(current_student.id)
    today_tasks = study_plan_service.get_today_tasks(current_student.id)
    
    return {
        "mastery": mastery_overview,
        "badges": badges,
        "today_tasks": today_tasks,
        "student_id": current_student.id,
        "username": current_student.username
    }
