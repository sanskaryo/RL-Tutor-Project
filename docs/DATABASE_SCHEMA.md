# Database Schema Documentation
**RL-Based Personalized Educational Tutor**

## Overview
This document describes the complete database schema for the RL-Based Educational Tutor system. The application uses **SQLite** for development and **PostgreSQL** for production.

---

## Core Models

### 1. **Student** (User/Profile)
Primary user entity storing authentication and profile information.

```sql
Table: students
├── id: INTEGER PRIMARY KEY
├── username: VARCHAR(50) UNIQUE NOT NULL
├── email: VARCHAR(100) UNIQUE NOT NULL
├── hashed_password: VARCHAR(255) NOT NULL
├── full_name: VARCHAR(100)
├── created_at: TIMESTAMP DEFAULT NOW()
├── last_login: TIMESTAMP
├── is_active: BOOLEAN DEFAULT TRUE
└── preferred_difficulty: INTEGER DEFAULT 3

Relationships:
├── sessions (1:M) → LearningSession
├── knowledge (1:1) → StudentKnowledge
├── learning_style_profile (1:1) → LearningStyleProfile
├── skill_gaps (1:M) → SkillGap
├── learning_pace (1:1) → LearningPace
├── bandit_state (1:1) → BanditState
├── skill_mastery (1:M) → StudentMastery
├── badges (1:M) → StudentBadge
└── study_plans (1:M) → StudyPlan
```

---

### 2. **Content** (Educational Material)
Stores questions, exercises, and learning materials.

```sql
Table: content
├── id: INTEGER PRIMARY KEY
├── topic: VARCHAR(100) NOT NULL
├── subtopic: VARCHAR(100)
├── difficulty: INTEGER NOT NULL (1-5)
├── content_type: VARCHAR(20) DEFAULT 'question'
├── question_text: TEXT
├── correct_answer: VARCHAR(255)
├── explanation: TEXT
├── tags: JSON  -- Array of skill tags
├── estimated_time: INTEGER  -- Minutes
├── points: INTEGER DEFAULT 10
└── created_at: TIMESTAMP DEFAULT NOW()

Indexes:
├── idx_content_topic (topic)
├── idx_content_difficulty (difficulty)
└── idx_content_type (content_type)
```

---

### 3. **LearningSession** (Study Sessions)
Tracks individual learning sessions and student interactions.

```sql
Table: learning_sessions
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── content_id: INTEGER FK → content.id
├── start_time: TIMESTAMP DEFAULT NOW()
├── end_time: TIMESTAMP
├── answer_given: VARCHAR(255)
├── is_correct: BOOLEAN
├── time_spent: INTEGER  -- Seconds
├── difficulty: INTEGER
├── reward: FLOAT DEFAULT 0.0
├── rl_state: JSON  -- Agent state snapshot
├── rl_action: JSON  -- Agent action taken
└── feedback_text: TEXT

Relationships:
├── student: M:1 → Student
└── content: M:1 → Content

Indexes:
├── idx_session_student (student_id)
├── idx_session_content (content_id)
└── idx_session_time (start_time)
```

---

### 4. **StudentKnowledge** (Knowledge State)
Tracks student mastery levels across different topics.

```sql
Table: student_knowledge
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id UNIQUE NOT NULL
├── algebra_score: FLOAT DEFAULT 0.0
├── calculus_score: FLOAT DEFAULT 0.0
├── geometry_score: FLOAT DEFAULT 0.0
├── statistics_score: FLOAT DEFAULT 0.0
├── physics_score: FLOAT DEFAULT 0.0
├── programming_score: FLOAT DEFAULT 0.0
├── total_questions_answered: INTEGER DEFAULT 0
├── correct_answers: INTEGER DEFAULT 0
├── accuracy_rate: FLOAT DEFAULT 0.0
├── preferred_difficulty: INTEGER DEFAULT 3
├── learning_style: VARCHAR(50) DEFAULT 'balanced'
└── last_updated: TIMESTAMP DEFAULT NOW()

Relationships:
└── student: 1:1 → Student

Indexes:
└── idx_knowledge_student (student_id)
```

---

### 5. **PerformanceMetrics** (Analytics)
Aggregated performance metrics for analytics dashboard.

```sql
Table: performance_metrics
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── metric_date: DATE DEFAULT TODAY
├── total_attempts: INTEGER DEFAULT 0
├── correct_attempts: INTEGER DEFAULT 0
├── accuracy_rate: FLOAT DEFAULT 0.0
├── time_spent_minutes: INTEGER DEFAULT 0
├── topics_studied: JSON  -- Array of topics
├── avg_difficulty: FLOAT DEFAULT 0.0
├── current_streak: INTEGER DEFAULT 0
├── longest_streak: INTEGER DEFAULT 0
├── points_earned: INTEGER DEFAULT 0
└── created_at: TIMESTAMP DEFAULT NOW()

Relationships:
└── student: M:1 → Student

Indexes:
├── idx_metrics_student (student_id)
└── idx_metrics_date (metric_date)
```

---

## Phase 11: Student Profiling Models

### 6. **LearningStyleProfile** (VARK Assessment)
Stores VARK learning style preferences.

```sql
Table: learning_style_profiles
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id UNIQUE NOT NULL
├── visual_score: FLOAT NOT NULL
├── auditory_score: FLOAT NOT NULL
├── reading_score: FLOAT NOT NULL
├── kinesthetic_score: FLOAT NOT NULL
├── dominant_style: VARCHAR(20) NOT NULL  -- V/A/R/K
├── secondary_style: VARCHAR(20)
├── quiz_completed_at: TIMESTAMP DEFAULT NOW()
├── preferences: JSON  -- Custom preferences
└── last_updated: TIMESTAMP DEFAULT NOW()

Relationships:
└── student: 1:1 → Student

Indexes:
└── idx_style_student (student_id)
```

---

### 7. **SkillGap** (Gap Analysis)
Identifies and tracks knowledge gaps.

```sql
Table: skill_gaps
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── skill_id: INTEGER FK → skills.id NOT NULL
├── gap_type: VARCHAR(50) NOT NULL  -- 'prerequisite', 'weakness', 'forgotten'
├── severity: VARCHAR(20) NOT NULL  -- 'critical', 'high', 'medium', 'low'
├── current_level: FLOAT DEFAULT 0.0  -- 0-1 mastery
├── target_level: FLOAT DEFAULT 0.8
├── priority_score: INTEGER NOT NULL  -- 1-10 scale
├── estimated_hours: FLOAT
├── recommendation: TEXT
├── detected_at: TIMESTAMP DEFAULT NOW()
├── last_practiced: TIMESTAMP
├── practice_count: INTEGER DEFAULT 0
├── progress_percentage: FLOAT DEFAULT 0.0
└── status: VARCHAR(20) DEFAULT 'active'  -- 'active', 'in_progress', 'resolved'

Relationships:
├── student: M:1 → Student
└── skill: M:1 → Skill

Indexes:
├── idx_gap_student (student_id)
├── idx_gap_severity (severity)
└── idx_gap_status (status)
```

---

### 8. **Skill** (Master Skill Tree)
Hierarchical skill taxonomy for gap analysis.

```sql
Table: skills
├── id: INTEGER PRIMARY KEY
├── name: VARCHAR(100) UNIQUE NOT NULL
├── display_name: VARCHAR(100) NOT NULL
├── description: TEXT
├── category: VARCHAR(50)  -- 'mathematics', 'science', etc.
├── parent_skill_id: INTEGER FK → skills.id
├── prerequisite_skill_ids: JSON  -- Array of required skill IDs
├── difficulty_level: INTEGER  -- 1-5
├── estimated_time_hours: FLOAT
├── related_content_ids: JSON  -- Content that teaches this skill
└── created_at: TIMESTAMP DEFAULT NOW()

Relationships:
├── parent: M:1 → Skill (self-reference)
├── skill_gaps: 1:M → SkillGap
└── pre_assessment_results: 1:M → PreAssessmentResult

Indexes:
├── idx_skill_category (category)
└── idx_skill_parent (parent_skill_id)
```

---

### 9. **PreAssessmentResult** (Initial Assessment)
Stores pre-assessment test results for gap detection.

```sql
Table: pre_assessment_results
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── skill_id: INTEGER FK → skills.id NOT NULL
├── score: FLOAT NOT NULL  -- 0.0 to 1.0
├── questions_answered: INTEGER
├── time_spent_minutes: INTEGER
├── taken_at: TIMESTAMP DEFAULT NOW()
└── notes: TEXT

Relationships:
├── student: M:1 → Student
└── skill: M:1 → Skill

Indexes:
├── idx_assessment_student (student_id)
└── idx_assessment_skill (skill_id)
```

---

### 10. **LearningPace** (Pace Tracking)
Tracks student learning speed and difficulty adjustments.

```sql
Table: learning_pace
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id UNIQUE NOT NULL
├── current_pace: VARCHAR(20) NOT NULL  -- 'slow', 'normal', 'fast'
├── avg_time_per_question: FLOAT  -- Minutes
├── avg_completion_rate: FLOAT  -- 0-1
├── optimal_difficulty: INTEGER  -- 1-5
├── pace_adjustments: JSON  -- History of adjustments
├── calculated_at: TIMESTAMP DEFAULT NOW()
└── last_updated: TIMESTAMP DEFAULT NOW()

Relationships:
└── student: 1:1 → Student

Indexes:
└── idx_pace_student (student_id)
```

---

### 11. **ConceptTimeLog** (Time Tracking)
Detailed time-on-task tracking per concept.

```sql
Table: concept_time_logs
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── concept: VARCHAR(100) NOT NULL
├── time_spent_seconds: INTEGER NOT NULL
├── questions_attempted: INTEGER DEFAULT 0
├── success_rate: FLOAT DEFAULT 0.0
├── difficulty_level: INTEGER
├── logged_at: TIMESTAMP DEFAULT NOW()
└── session_id: INTEGER FK → learning_sessions.id

Relationships:
├── student: M:1 → Student
└── session: M:1 → LearningSession

Indexes:
├── idx_time_student (student_id)
├── idx_time_concept (concept)
└── idx_time_session (session_id)
```

---

## Phase 12: Smart Recommendations Models

### 12. **BanditState** (Multi-Armed Bandit)
Tracks epsilon-greedy bandit algorithm state.

```sql
Table: bandit_states
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id UNIQUE NOT NULL
├── topic: VARCHAR(100) NOT NULL
├── arm_rewards: JSON  -- Dict of {content_id: total_reward}
├── arm_counts: JSON  -- Dict of {content_id: pull_count}
├── epsilon: FLOAT DEFAULT 0.1
├── total_pulls: INTEGER DEFAULT 0
├── best_arm: INTEGER  -- content_id with highest avg reward
└── last_updated: TIMESTAMP DEFAULT NOW()

Relationships:
└── student: 1:1 → Student

Indexes:
└── idx_bandit_student (student_id)
```

---

### 13. **UserInteraction** (Collaborative Filtering)
Stores all user-content interactions for CF recommendations.

```sql
Table: user_interactions
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── content_id: INTEGER FK → content.id NOT NULL
├── interaction_type: VARCHAR(20) NOT NULL  -- 'view', 'attempt', 'complete'
├── rating: FLOAT  -- 1-5 stars
├── time_spent_seconds: INTEGER
├── success: BOOLEAN
├── timestamp: TIMESTAMP DEFAULT NOW()
└── context: JSON  -- Additional metadata

Relationships:
├── student: M:1 → Student
└── content: M:1 → Content

Indexes:
├── idx_interaction_student (student_id)
├── idx_interaction_content (content_id)
└── idx_interaction_time (timestamp)
```

---

### 14. **SimilarStudent** (Collaborative Filtering)
Stores cosine similarity scores between students.

```sql
Table: similar_students
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── similar_student_id: INTEGER FK → students.id NOT NULL
├── similarity_score: FLOAT NOT NULL  -- 0-1 cosine similarity
├── calculated_at: TIMESTAMP DEFAULT NOW()
└── last_updated: TIMESTAMP DEFAULT NOW()

Relationships:
├── student: M:1 → Student
└── similar_student: M:1 → Student

Indexes:
├── idx_similar_student (student_id)
└── idx_similar_score (similarity_score DESC)

Constraints:
└── UNIQUE(student_id, similar_student_id)
```

---

### 15. **FlashCard** (Spaced Repetition)
Stores flashcards for SM-2 algorithm.

```sql
Table: flashcards
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── content_id: INTEGER FK → content.id NOT NULL
├── front_text: TEXT NOT NULL
├── back_text: TEXT NOT NULL
├── easiness_factor: FLOAT DEFAULT 2.5  -- SM-2 parameter
├── interval: INTEGER DEFAULT 1  -- Days until next review
├── repetitions: INTEGER DEFAULT 0
├── next_review_date: DATE NOT NULL
├── last_reviewed: TIMESTAMP
├── times_reviewed: INTEGER DEFAULT 0
├── average_rating: FLOAT DEFAULT 0.0
└── created_at: TIMESTAMP DEFAULT NOW()

Relationships:
├── student: M:1 → Student
├── content: M:1 → Content
└── review_sessions: 1:M → ReviewSession

Indexes:
├── idx_flashcard_student (student_id)
├── idx_flashcard_next_review (next_review_date)
└── idx_flashcard_content (content_id)
```

---

### 16. **ReviewSession** (SRS Session Tracking)
Tracks individual flashcard review sessions.

```sql
Table: review_sessions
├── id: INTEGER PRIMARY KEY
├── flashcard_id: INTEGER FK → flashcards.id NOT NULL
├── student_id: INTEGER FK → students.id NOT NULL
├── quality: INTEGER NOT NULL  -- 0-5 SM-2 quality rating
├── time_spent_seconds: INTEGER
├── reviewed_at: TIMESTAMP DEFAULT NOW()
└── notes: TEXT

Relationships:
├── flashcard: M:1 → FlashCard
└── student: M:1 → Student

Indexes:
├── idx_review_flashcard (flashcard_id)
├── idx_review_student (student_id)
└── idx_review_time (reviewed_at)
```

---

## Phase 13: Mastery-Based Progression Models

### 17. **MasterySkill** (Skill Tree Nodes)
Directed Acyclic Graph (DAG) of skills with prerequisites.

```sql
Table: mastery_skills
├── id: INTEGER PRIMARY KEY
├── name: VARCHAR(100) UNIQUE NOT NULL
├── description: TEXT
├── category: VARCHAR(50)  -- 'Fundamentals', 'Algebra', 'Calculus', etc.
├── difficulty: VARCHAR(20) NOT NULL  -- 'beginner', 'intermediate', 'advanced', 'expert'
├── estimated_hours: FLOAT DEFAULT 1.0
├── icon: VARCHAR(50)  -- Icon name for UI
├── created_at: TIMESTAMP DEFAULT NOW()
└── updated_at: TIMESTAMP DEFAULT NOW()

Relationships:
├── prerequisites: M:M → MasterySkill (via skill_prerequisites)
├── unlocks: M:M → MasterySkill (reverse of prerequisites)
└── student_mastery: 1:M → StudentMastery

Association Table: skill_prerequisites
├── skill_id: INTEGER FK → mastery_skills.id
└── prerequisite_id: INTEGER FK → mastery_skills.id
```

---

### 18. **StudentMastery** (Skill Progress Tracking)
Tracks student mastery level for each skill (0-5 scale).

```sql
Table: student_mastery
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── skill_id: INTEGER FK → mastery_skills.id NOT NULL
├── mastery_level: INTEGER DEFAULT 0  -- 0=Not Started, 1=Beginner, 2=Developing, 3=Proficient, 4=Advanced, 5=Master
├── progress_percentage: FLOAT DEFAULT 0.0  -- 0-100
├── total_practice_time: INTEGER DEFAULT 0  -- Minutes
├── correct_attempts: INTEGER DEFAULT 0
├── total_attempts: INTEGER DEFAULT 0
├── accuracy: FLOAT DEFAULT 0.0  -- Percentage
├── last_assessed_at: TIMESTAMP
├── first_practiced_at: TIMESTAMP
├── mastered_at: TIMESTAMP  -- When reached level 5
├── created_at: TIMESTAMP DEFAULT NOW()
└── updated_at: TIMESTAMP DEFAULT NOW()

Relationships:
├── student: M:1 → Student
└── skill: M:1 → MasterySkill

Indexes:
├── idx_mastery_student (student_id)
├── idx_mastery_skill (skill_id)
└── UNIQUE(student_id, skill_id)
```

---

### 19. **Badge** (Achievement System)
4-tier badge system (Bronze, Silver, Gold, Platinum).

```sql
Table: badges
├── id: INTEGER PRIMARY KEY
├── name: VARCHAR(100) UNIQUE NOT NULL
├── description: TEXT
├── category: VARCHAR(50) NOT NULL  -- 'mastery', 'streak', 'accuracy', 'practice', 'special'
├── tier: VARCHAR(20) NOT NULL  -- 'bronze', 'silver', 'gold', 'platinum'
├── icon: VARCHAR(50)
├── color: VARCHAR(50)  -- Hex color code
├── criteria: JSON NOT NULL  -- Requirements to earn badge
├── points: INTEGER DEFAULT 10
├── is_active: BOOLEAN DEFAULT TRUE
└── created_at: TIMESTAMP DEFAULT NOW()

Relationships:
└── student_badges: 1:M → StudentBadge

Indexes:
├── idx_badge_category (category)
└── idx_badge_tier (tier)
```

---

### 20. **StudentBadge** (Earned Badges)
Tracks badges earned by students with verification codes.

```sql
Table: student_badges
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── badge_id: INTEGER FK → badges.id NOT NULL
├── earned_at: TIMESTAMP DEFAULT NOW()
├── verification_code: VARCHAR(32) UNIQUE  -- For certificate validation
├── evidence: JSON  -- Proof of achievement
├── displayed: BOOLEAN DEFAULT TRUE
├── is_public: BOOLEAN DEFAULT TRUE
└── shared_count: INTEGER DEFAULT 0

Relationships:
├── student: M:1 → Student
└── badge: M:1 → Badge

Indexes:
├── idx_student_badge_student (student_id)
├── idx_student_badge_badge (badge_id)
├── idx_student_badge_verification (verification_code)
└── UNIQUE(student_id, badge_id)
```

---

### 21. **StudyPlan** (Personalized Study Plans)
AI-generated study plans with spaced repetition.

```sql
Table: study_plans
├── id: INTEGER PRIMARY KEY
├── student_id: INTEGER FK → students.id NOT NULL
├── title: VARCHAR(200) NOT NULL
├── description: TEXT
├── goal_type: VARCHAR(50) NOT NULL  -- 'mastery', 'exam_prep', 'review', 'custom'
├── target_skills: JSON NOT NULL  -- Array of skill IDs
├── target_date: DATE NOT NULL
├── daily_minutes: INTEGER DEFAULT 30
├── schedule: JSON NOT NULL  -- Daily breakdown with tasks
├── status: VARCHAR(20) DEFAULT 'active'  -- 'active', 'completed', 'abandoned'
├── progress_percentage: FLOAT DEFAULT 0.0
├── performance_trend: VARCHAR(20)  -- 'ahead', 'on_track', 'behind'
├── created_at: TIMESTAMP DEFAULT NOW()
├── updated_at: TIMESTAMP DEFAULT NOW()
└── completed_at: TIMESTAMP

Relationships:
└── student: M:1 → Student

Indexes:
├── idx_study_plan_student (student_id)
├── idx_study_plan_status (status)
└── idx_study_plan_target_date (target_date)
```

---

## Relationships Summary

### One-to-One Relationships:
- Student ↔ StudentKnowledge
- Student ↔ LearningStyleProfile
- Student ↔ LearningPace
- Student ↔ BanditState

### One-to-Many Relationships:
- Student → LearningSession
- Student → SkillGap
- Student → StudentMastery
- Student → StudentBadge
- Student → StudyPlan
- Student → FlashCard
- Student → ReviewSession
- Student → UserInteraction
- Content → LearningSession
- Skill → SkillGap
- MasterySkill → StudentMastery
- Badge → StudentBadge
- FlashCard → ReviewSession

### Many-to-Many Relationships:
- Student ↔ Student (via similar_students)
- MasterySkill ↔ MasterySkill (via skill_prerequisites)

---

## Indexes Strategy

### High-Traffic Queries:
- Student lookups: `username`, `email`
- Session queries: `student_id`, `start_time`
- Content selection: `topic`, `difficulty`
- Gap analysis: `student_id`, `severity`, `status`
- Flashcard reviews: `next_review_date`, `student_id`

### Composite Indexes:
```sql
CREATE INDEX idx_session_student_time ON learning_sessions(student_id, start_time);
CREATE INDEX idx_interaction_student_content ON user_interactions(student_id, content_id);
CREATE INDEX idx_flashcard_student_review ON flashcards(student_id, next_review_date);
CREATE INDEX idx_mastery_student_skill ON student_mastery(student_id, skill_id);
```

---

## Data Volumes (Estimated)

### Development Database:
- Students: ~100
- Content: ~500
- Sessions: ~5,000
- Skills: ~60
- Badges: ~25
- Flashcards: ~1,000

### Production Database (Year 1):
- Students: ~10,000
- Content: ~5,000
- Sessions: ~500,000
- Skills: ~200
- Badges: ~100
- Flashcards: ~100,000

---

## Migration Strategy

### Development → Production:
1. Export SQLite schema
2. Convert to PostgreSQL syntax
3. Add performance indexes
4. Setup connection pooling
5. Configure backups

### Schema Versioning:
- Use Alembic for migrations
- Track version in `alembic_version` table
- Maintain backward compatibility

---

## Security Considerations

### Sensitive Data:
- ✓ Passwords: bcrypt hashed
- ✓ JWT tokens: short-lived (30min)
- ✓ Email: validated format
- ✓ SQL injection: SQLAlchemy ORM

### Data Privacy:
- Student data: GDPR compliant
- Learning analytics: anonymized
- Performance metrics: aggregated

---

## Backup Strategy

### Frequency:
- Real-time: Transaction logs
- Hourly: Incremental backups
- Daily: Full database backup
- Weekly: Off-site storage

### Retention:
- Daily backups: 30 days
- Weekly backups: 6 months
- Yearly backups: 7 years

---

**Generated:** October 24, 2025  
**Version:** 1.0 (Phase 13 Complete)  
**Database:** SQLite (Dev) / PostgreSQL (Prod)
