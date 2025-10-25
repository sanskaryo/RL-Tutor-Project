"""
Students API endpoints
Provides student-specific routes such as /me
"""
from fastapi import APIRouter, Depends
from app.api.deps import get_current_student
from app.models.models import Student
from app.models.schemas import StudentResponse

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/me", response_model=StudentResponse)
def read_current_student_profile(current_student: Student = Depends(get_current_student)):
    """Return the profile of the currently authenticated student"""
    return current_student
