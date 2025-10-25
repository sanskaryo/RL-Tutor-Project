"""
Skill Gap Analysis API Endpoints
Identifies learning gaps and provides targeted recommendations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.models import Student, StudentKnowledge, LearningSession
from app.models.skill_gap import SkillGap, Skill, PreAssessmentResult
from app.api.deps import get_current_student
from app.services.student_model import StudentModelService

router = APIRouter(prefix="/skill-gaps", tags=["skill-gaps"])


@router.get("/analyze")
def analyze_skill_gaps(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze student's skill gaps based on performance history
    """
    # Get student's knowledge state
    knowledge_state = StudentModelService.get_knowledge_state(db, current_student.id)
    
    # Get learning sessions to analyze performance patterns
    sessions = db.query(LearningSession).filter(
        LearningSession.student_id == current_student.id
    ).order_by(LearningSession.timestamp.desc()).limit(50).all()
    
    # Analyze gaps
    gaps = []
    
    # Check each topic
    topics = ['algebra', 'calculus', 'geometry', 'statistics']
    for topic in topics:
        score_key = f'{topic}_score'
        score = knowledge_state.get(score_key, 0.0)
        
        # Determine gap severity
        if score < 0.3:
            severity = "critical"
        elif score < 0.5:
            severity = "high"
        elif score < 0.7:
            severity = "medium"
        else:
            severity = "low"
        
        # Only report significant gaps
        if score < 0.7:
            # Check if gap already exists
            existing_gap = db.query(SkillGap).filter(
                SkillGap.student_id == current_student.id,
                SkillGap.topic == topic
            ).first()
            
            if existing_gap:
                # Update existing gap
                existing_gap.proficiency_level = score
                existing_gap.gap_severity = severity
            else:
                # Create new gap
                gap = SkillGap(
                    student_id=current_student.id,
                    topic=topic,
                    proficiency_level=score,
                    target_level=0.8,
                    gap_severity=severity,
                    assessment_method="session_analysis",
                    priority=_calculate_priority(severity, score),
                    estimated_time_hours=_estimate_time(score)
                )
                db.add(gap)
            
            gaps.append({
                "topic": topic.capitalize(),
                "current_level": score,
                "target_level": 0.8,
                "gap_percentage": (0.8 - score) * 100,
                "severity": severity,
                "estimated_hours": _estimate_time(score),
                "priority": _calculate_priority(severity, score)
            })
    
    db.commit()
    
    # Get all stored gaps for this student
    all_gaps = db.query(SkillGap).filter(
        SkillGap.student_id == current_student.id
    ).order_by(SkillGap.priority.desc()).all()
    
    return {
        "student_id": current_student.id,
        "analysis_date": "now",
        "total_gaps_identified": len(gaps),
        "critical_gaps": len([g for g in gaps if g["severity"] == "critical"]),
        "high_priority_gaps": len([g for g in gaps if g["severity"] == "high"]),
        "gaps": gaps,
        "recommendations": _generate_recommendations(gaps),
        "stored_gaps": [gap.to_dict() for gap in all_gaps]
    }


@router.get("/list")
def list_skill_gaps(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get all skill gaps for the current authenticated student"""
    
    gaps = db.query(SkillGap).filter(
        SkillGap.student_id == current_student.id
    ).order_by(SkillGap.priority.desc()).all()
    
    return [gap.to_dict() for gap in gaps]


@router.get("/students/{student_id}")
def get_student_gaps(
    student_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get all skill gaps for a student"""
    
    # Verify student owns this profile
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    
    gaps = db.query(SkillGap).filter(
        SkillGap.student_id == student_id
    ).order_by(SkillGap.priority.desc()).all()
    
    return [gap.to_dict() for gap in gaps]


@router.post("/students/{student_id}/gaps/{gap_id}/update-progress")
def update_gap_progress(
    student_id: int,
    gap_id: int,
    progress: float,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Update progress on addressing a skill gap"""
    
    if current_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    gap = db.query(SkillGap).filter(
        SkillGap.id == gap_id,
        SkillGap.student_id == student_id
    ).first()
    
    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill gap not found"
        )
    
    gap.progress_percentage = min(100.0, max(0.0, progress))
    gap.is_addressed = 1 if progress > 0 else 0
    
    db.commit()
    
    return {"success": True, "progress": gap.progress_percentage}


@router.get("/knowledge-graph")
def get_knowledge_graph(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get knowledge graph showing skills and their relationships
    """
    knowledge_state = StudentModelService.get_knowledge_state(db, current_student.id)
    
    # Build simplified knowledge graph
    nodes = []
    edges = []
    
    topics = [
        {"id": "algebra", "name": "Algebra", "score": knowledge_state.get("algebra_score", 0.0)},
        {"id": "calculus", "name": "Calculus", "score": knowledge_state.get("calculus_score", 0.0), "prereqs": ["algebra"]},
        {"id": "geometry", "name": "Geometry", "score": knowledge_state.get("geometry_score", 0.0)},
        {"id": "statistics", "name": "Statistics", "score": knowledge_state.get("statistics_score", 0.0), "prereqs": ["algebra"]},
    ]
    
    for topic in topics:
        nodes.append({
            "id": topic["id"],
            "name": topic["name"],
            "proficiency": topic["score"],
            "status": _get_status(topic["score"]),
            "color": _get_color(topic["score"])
        })
        
        # Add prerequisite edges
        if "prereqs" in topic:
            for prereq in topic["prereqs"]:
                edges.append({
                    "from": prereq,
                    "to": topic["id"],
                    "type": "prerequisite"
                })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "student_id": current_student.id
    }


# Helper functions
def _calculate_priority(severity: str, score: float) -> int:
    """Calculate priority (1-10) based on severity and score"""
    base_priority = {
        "critical": 10,
        "high": 8,
        "medium": 5,
        "low": 3
    }.get(severity, 5)
    
    # Adjust based on how far from target
    gap_size = 0.8 - score
    priority = base_priority + int(gap_size * 5)
    
    return min(10, max(1, priority))


def _estimate_time(current_score: float) -> float:
    """Estimate hours needed to close gap"""
    gap = 0.8 - current_score
    # Rough estimate: 10 hours per 0.1 gap
    return round(gap * 100, 1)


def _generate_recommendations(gaps: List[Dict]) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Sort by priority
    sorted_gaps = sorted(gaps, key=lambda x: x["priority"], reverse=True)
    
    if len(sorted_gaps) > 0:
        top_gap = sorted_gaps[0]
        recommendations.append(
            f"Focus on {top_gap['topic']} first - it's your highest priority gap"
        )
    
    critical = [g for g in gaps if g["severity"] == "critical"]
    if critical:
        recommendations.append(
            f"Address {len(critical)} critical gap(s) before moving to advanced topics"
        )
    
    if len(gaps) > 3:
        recommendations.append(
            "Consider a structured review plan to systematically address multiple gaps"
        )
    
    total_time = sum(g["estimated_hours"] for g in gaps)
    recommendations.append(
        f"Estimated {total_time:.1f} hours needed to reach target proficiency across all gaps"
    )
    
    return recommendations


def _get_status(score: float) -> str:
    """Get mastery status from score"""
    if score >= 0.9:
        return "mastered"
    elif score >= 0.7:
        return "proficient"
    elif score >= 0.5:
        return "developing"
    elif score >= 0.3:
        return "beginner"
    else:
        return "needs_foundation"


def _get_color(score: float) -> str:
    """Get color code for visualization"""
    if score >= 0.8:
        return "#22c55e"  # green
    elif score >= 0.6:
        return "#eab308"  # yellow
    elif score >= 0.4:
        return "#f97316"  # orange
    else:
        return "#ef4444"  # red
