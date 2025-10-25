"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.database import get_db
from app.api.deps import get_current_student
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from app.models.models import Student
from app.models.schemas import StudentCreate, StudentLogin, Token, StudentResponse
from app.services.student_model import StudentModelService

router = APIRouter(prefix="/auth", tags=["authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=Token)
# @limiter.limit("100/hour")  # Temporarily disabled for testing
def register(request: Request, student_data: StudentCreate, db: Session = Depends(get_db)):
    """Register a new student"""
    
    # Check if email already exists
    existing_email = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(Student).filter(Student.username == student_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new student
    hashed_password = get_password_hash(student_data.password)
    new_student = Student(
        email=student_data.email,
        username=student_data.username,
        hashed_password=hashed_password,
        full_name=student_data.full_name
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    # Initialize knowledge state
    StudentModelService.initialize_knowledge(db, new_student.id)
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": student_data.username})
    refresh_token = create_refresh_token(data={"sub": student_data.username})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
@limiter.limit("100/minute")  # Increased for development/testing
def login(request: Request, credentials: StudentLogin, db: Session = Depends(get_db)):
    """Login student and return JWT token"""
    
    # Find student by username
    student = db.query(Student).filter(Student.username == credentials.username).first()
    
    if not student or not verify_password(credentials.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": student.username})
    refresh_token = create_refresh_token(data={"sub": student.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }


@router.get("/me", response_model=StudentResponse)
def get_current_student_profile(current_student: Student = Depends(get_current_student)):
    """Get current student profile (authenticated)"""
    return current_student


@router.post("/refresh", response_model=Token)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify student still exists
    student = db.query(Student).filter(Student.username == username).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Create new access token
    new_access_token = create_access_token(data={"sub": username})
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,  # Return same refresh token
        "token_type": "bearer"
    }
