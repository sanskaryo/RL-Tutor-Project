"""
FINAL COMPREHENSIVE TEST SUITE
Tests all components of the RL-Based Educational Tutor
Phase 1-13 Complete Coverage
Date: October 24, 2025
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.core.database import Base, get_db
from app.models import (
    Student, Content, LearningSession, StudentKnowledge,
    LearningStyleProfile, SkillGap, Skill, PreAssessmentResult,
    LearningPace, ConceptTimeLog, BanditState, UserInteraction,
    SimilarStudent, FlashCard, ReviewSession
)
from app.models.mastery import MasterySkill, StudentMastery, Badge, StudentBadge, StudyPlan
from app.core.security import get_password_hash, verify_password, create_access_token

# Setup test database
TEST_DATABASE_URL = "sqlite:///./test_final.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

# Test data
TEST_USER = {
    "email": "test@example.com",
    "password": "TestPass123!",
    "name": "Test User"
}

TEST_USER_2 = {
    "email": "test2@example.com",
    "password": "TestPass456!",
    "name": "Test User 2"
}


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database before all tests"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed essential data
    db = TestingSessionLocal()
    try:
        # Create test content
        content_items = [
            Content(
                id=1,
                title="Basic Addition",
                topic="Algebra",
                difficulty=1,
                content_type="question",
                question_text="What is 2 + 2?",
                correct_answer="4"
            ),
            Content(
                id=2,
                title="Linear Equation",
                topic="Algebra",
                difficulty=2,
                content_type="question",
                question_text="Solve: x + 5 = 10",
                correct_answer="5"
            ),
            Content(
                id=3,
                title="Derivative",
                topic="Calculus",
                difficulty=3,
                content_type="question",
                question_text="Find derivative of x^2",
                correct_answer="2x"
            ),
        ]
        
        for item in content_items:
            existing = db.query(Content).filter_by(id=item.id).first()
            if not existing:
                db.add(item)
        
        # Create test skills
        skills = [
            Skill(id=1, name="basic_addition", display_name="Basic Addition", difficulty_level=1, category="mathematics"),
            Skill(id=2, name="algebra_basics", display_name="Algebra Basics", difficulty_level=2, category="mathematics"),
            Skill(id=3, name="calculus_fundamentals", display_name="Calculus Fundamentals", difficulty_level=3, category="mathematics"),
        ]
        
        for skill in skills:
            existing = db.query(Skill).filter_by(id=skill.id).first()
            if not existing:
                db.add(skill)
        
        # Create test mastery skills
        mastery_skills = [
            MasterySkill(
                id=1,
                name="Arithmetic Basics",
                category="Fundamentals",
                difficulty="beginner",
                description="Basic arithmetic operations"
            ),
            MasterySkill(
                id=2,
                name="Linear Equations",
                category="Algebra",
                difficulty="intermediate",
                description="Solving linear equations"
            ),
        ]
        
        for skill in mastery_skills:
            existing = db.query(MasterySkill).filter_by(id=skill.id).first()
            if not existing:
                db.add(skill)
        
        # Create test badges
        badges = [
            Badge(
                id=1,
                name="First Steps",
                description="Complete your first session",
                tier="bronze",
                category="practice",
                criteria={"sessions": 1}
            ),
            Badge(
                id=2,
                name="Dedicated Learner",
                description="Complete 10 sessions",
                tier="silver",
                category="practice",
                criteria={"sessions": 10}
            ),
        ]
        
        for badge in badges:
            existing = db.query(Badge).filter_by(id=badge.id).first()
            if not existing:
                db.add(badge)
        
        db.commit()
    finally:
        db.close()
    
    yield
    
    # Cleanup after all tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_token():
    """Create a test user and return auth token"""
    db = TestingSessionLocal()
    try:
        # Delete existing user if exists
        existing = db.query(Student).filter_by(email=TEST_USER["email"]).first()
        if existing:
            db.delete(existing)
            db.commit()
        
        # Create new user
        hashed_password = get_password_hash(TEST_USER["password"])
        user = Student(
            email=TEST_USER["email"],
            hashed_password=hashed_password,
            name=TEST_USER["name"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create token
        token = create_access_token(data={"sub": user.email})
        return token, user.id
    finally:
        db.close()


# ==============================================================================
# DATABASE TESTS
# ==============================================================================

class TestDatabase:
    """Test database structure and integrity"""
    
    def test_all_tables_created(self):
        """Verify all 21 tables exist"""
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'students', 'content', 'learning_sessions', 'student_knowledge',
            'performance_metrics', 'learning_style_profiles', 'skill_gaps',
            'skills', 'pre_assessment_results', 'learning_pace', 'concept_time_logs',
            'bandit_states', 'user_interactions', 'similar_students',
            'flashcards', 'review_sessions', 'mastery_skills', 'student_mastery',
            'badges', 'student_badges', 'study_plans'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
    
    def test_foreign_key_constraints(self):
        """Verify foreign key relationships"""
        inspector = inspect(engine)
        
        # Check learning_sessions has student_id FK
        fks = inspector.get_foreign_keys('learning_sessions')
        fk_columns = [fk['constrained_columns'][0] for fk in fks]
        assert 'student_id' in fk_columns
        assert 'content_id' in fk_columns
    
    def test_indexes_exist(self):
        """Verify critical indexes exist"""
        inspector = inspect(engine)
        
        # Check student_knowledge indexes
        indexes = inspector.get_indexes('student_knowledge')
        index_columns = [idx['column_names'] for idx in indexes]
        assert ['student_id'] in index_columns or any('student_id' in cols for cols in index_columns)


# ==============================================================================
# AUTHENTICATION TESTS
# ==============================================================================

class TestAuthentication:
    """Test user authentication and authorization"""
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = client.post("/api/students/register", json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "name": "New User"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["email"] == "newuser@example.com"
        assert "hashed_password" not in data
    
    def test_user_registration_duplicate_email(self, auth_token):
        """Test registration with existing email fails"""
        response = client.post("/api/students/register", json=TEST_USER)
        assert response.status_code == 400
    
    def test_login_success(self):
        """Test successful login"""
        response = client.post("/api/auth/login", data={
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self):
        """Test login with wrong password fails"""
        response = client.post("/api/auth/login", data={
            "username": TEST_USER["email"],
            "password": "WrongPassword"
        })
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user fails"""
        response = client.post("/api/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "AnyPassword123"
        })
        
        assert response.status_code == 401
    
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token fails"""
        response = client.get("/api/students/me")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token fails"""
        response = client.get("/api/students/me", headers={
            "Authorization": "Bearer invalid_token_xyz"
        })
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token(self, auth_token):
        """Test accessing protected endpoint with valid token succeeds"""
        token, user_id = auth_token
        response = client.get("/api/students/me", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TEST_USER["email"]
    
    def test_password_hashing(self):
        """Test password is properly hashed"""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("WrongPassword", hashed)


# ==============================================================================
# CONTENT & SESSION TESTS
# ==============================================================================

class TestContentAndSessions:
    """Test content delivery and learning sessions"""
    
    def test_get_content_list(self, auth_token):
        """Test retrieving content list"""
        token, _ = auth_token
        response = client.get("/api/content/", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_specific_content(self, auth_token):
        """Test retrieving specific content"""
        token, _ = auth_token
        response = client.get("/api/content/1", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "question_text" in data or "title" in data
    
    def test_create_learning_session(self, auth_token):
        """Test creating a learning session"""
        token, user_id = auth_token
        response = client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "content_id": 1,
            "is_correct": True,
            "time_spent": 120
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == user_id
        assert data["content_id"] == 1
        assert data["is_correct"] == True
    
    def test_get_student_sessions(self, auth_token):
        """Test retrieving student's sessions"""
        token, _ = auth_token
        response = client.get("/api/sessions/student", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_recommended_content(self, auth_token):
        """Test RL agent recommendation"""
        token, _ = auth_token
        response = client.get("/api/sessions/recommend", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "content_id" in data
        assert "difficulty_level" in data


# ==============================================================================
# PHASE 11 TESTS: STUDENT PROFILING
# ==============================================================================

class TestPhase11StudentProfiling:
    """Test Phase 11: Learning Styles, Skill Gaps, Learning Pace"""
    
    def test_create_learning_style_profile(self, auth_token):
        """Test creating learning style profile"""
        token, _ = auth_token
        response = client.post("/api/learning-style/profile", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "visual_score": 0.75,
            "auditory_score": 0.60,
            "reading_score": 0.80,
            "kinesthetic_score": 0.55
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "dominant_style" in data
        assert data["dominant_style"] in ["visual", "auditory", "reading", "kinesthetic"]
    
    def test_get_learning_style_profile(self, auth_token):
        """Test retrieving learning style profile"""
        token, _ = auth_token
        response = client.get("/api/learning-style/profile", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "visual_score" in data
    
    def test_analyze_skill_gaps(self, auth_token):
        """Test skill gap analysis"""
        token, user_id = auth_token
        
        # First create some sessions
        client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "content_id": 1,
            "is_correct": False,
            "time_spent": 180
        })
        
        # Analyze gaps
        response = client.post("/api/skill-gaps/analyze", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_skill_gaps(self, auth_token):
        """Test retrieving skill gaps"""
        token, _ = auth_token
        response = client.get("/api/skill-gaps/", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_track_learning_pace(self, auth_token):
        """Test learning pace tracking"""
        token, _ = auth_token
        response = client.post("/api/learning-pace/track", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "concept_name": "Linear Equations",
            "time_spent": 300
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "pace_classification" in data
    
    def test_get_learning_pace(self, auth_token):
        """Test retrieving learning pace"""
        token, _ = auth_token
        response = client.get("/api/learning-pace/", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


# ==============================================================================
# PHASE 12 TESTS: SMART RECOMMENDATIONS
# ==============================================================================

class TestPhase12SmartRecommendations:
    """Test Phase 12: Bandits, Collaborative Filtering, Spaced Repetition"""
    
    def test_bandit_recommendation(self, auth_token):
        """Test multi-armed bandit recommendation"""
        token, _ = auth_token
        response = client.get("/api/bandit/recommend/Algebra", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "content_id" in data
        assert "arm_id" in data
    
    def test_bandit_update_reward(self, auth_token):
        """Test updating bandit reward"""
        token, _ = auth_token
        
        # Get recommendation first
        rec = client.get("/api/bandit/recommend/Algebra", headers={
            "Authorization": f"Bearer {token}"
        }).json()
        
        # Update reward
        response = client.post(f"/api/bandit/update/{rec['arm_id']}", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "reward": 1.0
        })
        
        assert response.status_code == 200
    
    def test_collaborative_filtering_recommendations(self, auth_token):
        """Test collaborative filtering"""
        token, _ = auth_token
        response = client.get("/api/collaborative/recommendations", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_flashcard(self, auth_token):
        """Test creating flashcard"""
        token, _ = auth_token
        response = client.post("/api/flashcards/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "topic": "Algebra",
            "front_text": "What is the quadratic formula?",
            "back_text": "x = (-b ± √(b²-4ac)) / 2a",
            "difficulty": 3
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Algebra"
        assert "next_review_date" in data
    
    def test_get_flashcards_due(self, auth_token):
        """Test getting due flashcards"""
        token, _ = auth_token
        response = client.get("/api/flashcards/due", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_review_flashcard(self, auth_token):
        """Test reviewing flashcard with SM-2"""
        token, _ = auth_token
        
        # Create flashcard first
        card = client.post("/api/flashcards/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "topic": "Calculus",
            "front_text": "Derivative of sin(x)?",
            "back_text": "cos(x)",
            "difficulty": 2
        }).json()
        
        # Review it
        response = client.post(f"/api/flashcards/{card['id']}/review", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "quality": 4
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["repetition"] == 1
        assert "next_review_date" in data


# ==============================================================================
# PHASE 13 TESTS: MASTERY-BASED PROGRESSION
# ==============================================================================

class TestPhase13MasteryProgression:
    """Test Phase 13: Skill Tree, Badges, Study Plans"""
    
    def test_get_skill_tree(self, auth_token):
        """Test retrieving skill tree"""
        token, _ = auth_token
        response = client.get("/api/mastery/tree", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_mastery_skill(self, auth_token):
        """Test retrieving specific mastery skill"""
        token, _ = auth_token
        response = client.get("/api/mastery/1", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "category" in data
    
    def test_assess_skill(self, auth_token):
        """Test assessing a skill"""
        token, _ = auth_token
        response = client.post("/api/mastery/1/assess", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "assessment_score": 0.85,
            "time_spent": 600,
            "questions_attempted": 10,
            "questions_correct": 8
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "mastery_level" in data
        assert 0 <= data["mastery_level"] <= 5
    
    def test_get_student_mastery(self, auth_token):
        """Test retrieving student mastery levels"""
        token, _ = auth_token
        response = client.get("/api/mastery/mastery", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_skill_recommendations(self, auth_token):
        """Test getting skill recommendations"""
        token, _ = auth_token
        response = client.get("/api/mastery/recommendations", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_all_badges(self, auth_token):
        """Test retrieving all badges"""
        token, _ = auth_token
        response = client.get("/api/mastery/badges", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_student_badges(self, auth_token):
        """Test retrieving student's earned badges"""
        token, _ = auth_token
        response = client.get("/api/mastery/students/badges", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_check_badge_criteria(self, auth_token):
        """Test checking and auto-awarding badges"""
        token, user_id = auth_token
        
        # Create a session to trigger badge check
        client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "content_id": 1,
            "is_correct": True,
            "time_spent": 100
        })
        
        response = client.post("/api/mastery/badges/check", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "newly_awarded" in data
    
    def test_generate_study_plan(self, auth_token):
        """Test generating AI study plan"""
        token, _ = auth_token
        response = client.post("/api/mastery/study-plans/generate", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "goal": "mastery",
            "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "daily_minutes": 60,
            "target_skills": [1, 2]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["goal"] == "mastery"
    
    def test_get_study_plans(self, auth_token):
        """Test retrieving study plans"""
        token, _ = auth_token
        response = client.get("/api/mastery/study-plans/", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_today_tasks(self, auth_token):
        """Test getting today's study tasks"""
        token, _ = auth_token
        response = client.get("/api/mastery/study-plans/today/tasks", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


# ==============================================================================
# RL AGENT TESTS
# ==============================================================================

class TestRLAgent:
    """Test reinforcement learning agent"""
    
    def test_q_learning_initialization(self, auth_token):
        """Test Q-learning agent initializes correctly"""
        token, _ = auth_token
        
        # Make recommendation to trigger agent
        response = client.get("/api/sessions/recommend", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
    
    def test_epsilon_greedy_exploration(self, auth_token):
        """Test epsilon-greedy strategy"""
        token, _ = auth_token
        
        # Get multiple recommendations
        recommendations = []
        for _ in range(10):
            response = client.get("/api/sessions/recommend", headers={
                "Authorization": f"Bearer {token}"
            })
            recommendations.append(response.json())
        
        # Should have some variety (exploration)
        content_ids = [r["content_id"] for r in recommendations]
        assert len(set(content_ids)) > 1
    
    def test_q_value_update(self, auth_token):
        """Test Q-values update after session"""
        token, _ = auth_token
        
        # Get recommendation
        rec = client.get("/api/sessions/recommend", headers={
            "Authorization": f"Bearer {token}"
        }).json()
        
        # Complete session
        response = client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "content_id": rec["content_id"],
            "is_correct": True,
            "time_spent": 120
        })
        
        assert response.status_code == 200


# ==============================================================================
# ANALYTICS & PERFORMANCE TESTS
# ==============================================================================

class TestAnalyticsAndPerformance:
    """Test analytics and performance tracking"""
    
    def test_get_student_knowledge(self, auth_token):
        """Test retrieving student knowledge state"""
        token, user_id = auth_token
        db = TestingSessionLocal()
        try:
            # Ensure knowledge record exists
            knowledge = db.query(StudentKnowledge).filter_by(student_id=user_id).first()
            if not knowledge:
                knowledge = StudentKnowledge(
                    student_id=user_id,
                    algebra_score=0.5,
                    calculus_score=0.3,
                    geometry_score=0.6,
                    statistics_score=0.4,
                    physics_score=0.5,
                    programming_score=0.7
                )
                db.add(knowledge)
                db.commit()
        finally:
            db.close()
        
        response = client.get("/api/analytics/knowledge", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "algebra_score" in data
    
    def test_performance_trends(self, auth_token):
        """Test performance trend calculation"""
        token, user_id = auth_token
        
        # Create multiple sessions
        for i in range(5):
            client.post("/api/sessions/", headers={
                "Authorization": f"Bearer {token}"
            }, json={
                "content_id": 1,
                "is_correct": i % 2 == 0,
                "time_spent": 100 + i * 20
            })
        
        # Get sessions
        response = client.get("/api/sessions/student", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        sessions = response.json()
        assert len(sessions) >= 5


# ==============================================================================
# ERROR HANDLING TESTS
# ==============================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_content_id(self, auth_token):
        """Test accessing non-existent content"""
        token, _ = auth_token
        response = client.get("/api/content/99999", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 404
    
    def test_invalid_skill_id(self, auth_token):
        """Test accessing non-existent skill"""
        token, _ = auth_token
        response = client.get("/api/mastery/99999", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 404
    
    def test_invalid_assessment_data(self, auth_token):
        """Test invalid assessment data"""
        token, _ = auth_token
        response = client.post("/api/mastery/1/assess", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "assessment_score": 1.5,  # Invalid: > 1.0
            "time_spent": -100,  # Invalid: negative
            "questions_attempted": 10,
            "questions_correct": 15  # Invalid: more correct than attempted
        })
        
        assert response.status_code == 422
    
    def test_malformed_json(self, auth_token):
        """Test malformed JSON request"""
        token, _ = auth_token
        response = client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }, data="not valid json{}")
        
        assert response.status_code == 422


# ==============================================================================
# INTEGRATION TESTS
# ==============================================================================

class TestIntegration:
    """Test end-to-end workflows"""
    
    def test_complete_learning_workflow(self, auth_token):
        """Test complete learning workflow from start to finish"""
        token, user_id = auth_token
        
        # 1. Create learning style profile
        style_response = client.post("/api/learning-style/profile", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "visual_score": 0.8,
            "auditory_score": 0.6,
            "reading_score": 0.7,
            "kinesthetic_score": 0.5
        })
        assert style_response.status_code == 200
        
        # 2. Get recommended content
        rec_response = client.get("/api/sessions/recommend", headers={
            "Authorization": f"Bearer {token}"
        })
        assert rec_response.status_code == 200
        rec = rec_response.json()
        
        # 3. Complete learning session
        session_response = client.post("/api/sessions/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "content_id": rec["content_id"],
            "is_correct": True,
            "time_spent": 150
        })
        assert session_response.status_code == 200
        
        # 4. Analyze skill gaps
        gap_response = client.post("/api/skill-gaps/analyze", headers={
            "Authorization": f"Bearer {token}"
        })
        assert gap_response.status_code == 200
        
        # 5. Assess mastery skill
        mastery_response = client.post("/api/mastery/1/assess", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "assessment_score": 0.85,
            "time_spent": 300,
            "questions_attempted": 10,
            "questions_correct": 9
        })
        assert mastery_response.status_code == 200
        
        # 6. Check badges
        badge_response = client.post("/api/mastery/badges/check", headers={
            "Authorization": f"Bearer {token}"
        })
        assert badge_response.status_code == 200
        
        # 7. Create flashcard
        flashcard_response = client.post("/api/flashcards/", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "topic": "Algebra",
            "front_text": "Test question",
            "back_text": "Test answer",
            "difficulty": 2
        })
        assert flashcard_response.status_code == 200
        
        # 8. Generate study plan
        plan_response = client.post("/api/mastery/study-plans/generate", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "goal": "mastery",
            "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "daily_minutes": 60,
            "target_skills": [1]
        })
        assert plan_response.status_code == 200
    
    def test_multi_user_collaborative_filtering(self):
        """Test collaborative filtering with multiple users"""
        db = TestingSessionLocal()
        
        try:
            # Create two users
            users = []
            for i, user_data in enumerate([TEST_USER, TEST_USER_2]):
                # Clean up existing
                existing = db.query(Student).filter_by(email=user_data["email"]).first()
                if existing:
                    db.delete(existing)
                db.commit()
                
                # Create new
                hashed = get_password_hash(user_data["password"])
                user = Student(
                    email=user_data["email"],
                    hashed_password=hashed,
                    name=user_data["name"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                users.append(user)
            
            # Create similar interactions for both users
            for user in users:
                for content_id in [1, 2]:
                    interaction = UserInteraction(
                        student_id=user.id,
                        content_id=content_id,
                        interaction_type="view",
                        rating=5.0
                    )
                    db.add(interaction)
            db.commit()
            
            # Test collaborative filtering for user 1
            token = create_access_token(data={"sub": users[0].email})
            response = client.get("/api/collaborative/recommendations", headers={
                "Authorization": f"Bearer {token}"
            })
            
            assert response.status_code == 200
            
        finally:
            db.close()


# ==============================================================================
# PERFORMANCE TESTS
# ==============================================================================

class TestPerformance:
    """Test system performance and scalability"""
    
    def test_bulk_session_creation(self, auth_token):
        """Test creating multiple sessions quickly"""
        token, _ = auth_token
        
        import time
        start_time = time.time()
        
        for i in range(20):
            response = client.post("/api/sessions/", headers={
                "Authorization": f"Bearer {token}"
            }, json={
                "content_id": (i % 3) + 1,
                "is_correct": i % 2 == 0,
                "time_spent": 100
            })
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 20 sessions in under 5 seconds
        assert duration < 5.0
    
    def test_recommendation_speed(self, auth_token):
        """Test recommendation generation speed"""
        token, _ = auth_token
        
        import time
        start_time = time.time()
        
        for _ in range(10):
            response = client.get("/api/sessions/recommend", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 10 recommendations in under 2 seconds
        assert duration < 2.0


# ==============================================================================
# RUN ALL TESTS
# ==============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
