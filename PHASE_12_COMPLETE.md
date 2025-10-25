# Phase 12: Smart Content Recommendations - COMPLETE ✅

## Overview
Phase 12 implements advanced RL-powered content recommendation systems using three complementary techniques:
1. **Multi-Armed Bandit (MAB)** - Learns optimal content types for each student
2. **Collaborative Filtering (CF)** - Recommends content based on similar students
3. **Spaced Repetition System (SRS)** - Optimizes flashcard review timing

**Status:** ✅ 100% COMPLETE  
**Implementation Date:** January 2025  
**Files Created:** 6 new files, 4 modified  
**API Endpoints:** 15+ new endpoints  
**Database Models:** 5 new models

---

## Phase 12.1: Multi-Armed Bandit (MAB) ✅

### Purpose
Learn and optimize content type selection (video, text, interactive, quiz) for each student using reinforcement learning.

### Algorithm: Epsilon-Greedy MAB
- **Exploration (ε=0.1):** Try random content types to discover preferences
- **Exploitation (90%):** Show best-performing content type
- **Reward Calculation:** Based on correctness, time spent, engagement
- **Arm Updates:** Update arm values using average reward

### Database Models

#### BanditState
Tracks Multi-Armed Bandit state per student.

```python
class BanditState(Base):
    __tablename__ = "bandit_states"
    
    id: int (primary key)
    student_id: int (foreign key → students)
    video_value: float (default 0.0)
    text_value: float (default 0.0)
    interactive_value: float (default 0.0)
    quiz_value: float (default 0.0)
    video_pulls: int (default 0)
    text_pulls: int (default 0)
    interactive_pulls: int (default 0)
    quiz_pulls: int (default 0)
    total_pulls: int (default 0)
    created_at: datetime
    updated_at: datetime
```

**Key Features:**
- Tracks value (average reward) for each content type
- Counts pulls (selections) per arm
- One-to-one relationship with Student

### Backend Services

#### ContentBandit Class
**File:** `backend/app/services/content_bandit.py` (185 lines)

**Key Methods:**
- `select_content_type()`: Epsilon-greedy arm selection
- `update(content_type, reward)`: Update arm values after reward
- `get_best_content_type()`: Returns highest-value arm
- `load_state()` / `save_state()`: Database persistence
- `calculate_content_reward()`: Reward function (correctness + time + engagement)

**Reward Formula:**
```python
reward = (
    0.6 * correctness +        # 60% weight on correctness
    0.2 * time_factor +         # 20% weight on time efficiency
    0.2 * engagement_score      # 20% weight on engagement
)
```

### API Endpoints

#### 1. Get Recommended Content Type
```
GET /api/v1/smart-recommendations/content-type
```

**Description:** Get epsilon-greedy content type recommendation

**Response:**
```json
{
  "content_type": "video",
  "strategy": "exploitation",
  "arm_values": {
    "video": 0.85,
    "text": 0.62,
    "interactive": 0.78,
    "quiz": 0.71
  }
}
```

#### 2. Submit Content Feedback
```
POST /api/v1/smart-recommendations/content-type/feedback
```

**Request Body:**
```json
{
  "content_type": "video",
  "correct": true,
  "time_spent": 120,
  "engagement_score": 0.9
}
```

**Response:**
```json
{
  "reward": 0.867,
  "updated_value": 0.858,
  "pulls": 15
}
```

#### 3. Get Bandit Statistics
```
GET /api/v1/smart-recommendations/bandit-stats
```

**Response:**
```json
{
  "total_pulls": 42,
  "best_content_type": "video",
  "best_value": 0.85,
  "arm_statistics": {
    "video": {"value": 0.85, "pulls": 15},
    "text": {"value": 0.62, "pulls": 10},
    "interactive": {"value": 0.78, "pulls": 12},
    "quiz": {"value": 0.71, "pulls": 5}
  }
}
```

---

## Phase 12.2: Collaborative Filtering (CF) ✅

### Purpose
Recommend content based on similar students' preferences using user-based collaborative filtering.

### Algorithm: Cosine Similarity
- Build user-item interaction matrix
- Calculate cosine similarity between students
- Find top K similar students
- Recommend content highly rated by similar students

### Database Models

#### UserInteraction
Records student interactions with content.

```python
class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id: int (primary key)
    student_id: int (foreign key → students)
    content_id: int
    content_type: str
    rating: float (1.0 - 5.0)
    interaction_type: str (view, complete, review, skip)
    time_spent: int (seconds)
    created_at: datetime
```

#### SimilarStudent
Stores precomputed student similarity pairs.

```python
class SimilarStudent(Base):
    __tablename__ = "similar_students"
    
    id: int (primary key)
    student_id: int (foreign key → students)
    similar_to_id: int (foreign key → students)
    similarity_score: float (0.0 - 1.0, cosine similarity)
    created_at: datetime
    updated_at: datetime
```

### Backend Services

#### CollaborativeFiltering Class
**File:** `backend/app/services/collaborative_filtering.py` (265 lines)

**Key Methods:**
- `build_interaction_matrix()`: Create user-item matrix from interactions
- `calculate_cosine_similarity(student1, student2)`: Compute similarity
- `find_similar_students(k=5)`: Get top K similar students
- `recommend_content(n=10)`: Peer-based content recommendations
- `get_peer_insights()`: Analyze what similar students struggled with

**Cosine Similarity Formula:**
```
similarity = dot(A, B) / (norm(A) * norm(B))
```

Where A and B are interaction vectors for two students.

### API Endpoints

#### 1. Record User Interaction
```
POST /api/v1/smart-recommendations/interactions
```

**Request Body:**
```json
{
  "content_id": 101,
  "content_type": "video",
  "rating": 5.0,
  "interaction_type": "complete",
  "time_spent": 180
}
```

#### 2. Get Peer-Based Recommendations
```
GET /api/v1/smart-recommendations/peer-recommendations?top_n=10
```

**Response:**
```json
{
  "recommendations": [
    {
      "content_id": 205,
      "content_type": "interactive",
      "predicted_rating": 4.7,
      "similar_students_count": 3
    }
  ]
}
```

#### 3. Find Similar Students
```
GET /api/v1/smart-recommendations/similar-students?top_k=5
```

**Response:**
```json
{
  "similar_students": [
    {
      "student_id": 42,
      "similarity_score": 0.87
    }
  ]
}
```

#### 4. Get Peer Insights
```
GET /api/v1/smart-recommendations/peer-insights
```

**Response:**
```json
{
  "similar_students_count": 5,
  "top_rated_by_peers": [
    {"content_id": 101, "avg_rating": 4.8}
  ],
  "struggled_with": [
    {"content_id": 205, "avg_rating": 2.3}
  ]
}
```

---

## Phase 12.3: Spaced Repetition System (SRS) ✅

### Purpose
Implement flashcard system with SM-2 (SuperMemo 2) algorithm for optimal review scheduling.

### Algorithm: SM-2 (SuperMemo 2)
- **Quality Rating:** 0-5 scale (0=complete blackout, 5=perfect recall)
- **Interval:** Days between reviews (increases with successful recalls)
- **Ease Factor:** Difficulty adjustment (higher = easier to remember)
- **Repetitions:** Count of consecutive successful reviews

### SM-2 Algorithm Flow
```
1. Review flashcard
2. Rate quality (0-5)
3. If quality < 3: Reset repetitions, interval = 1 day
4. If quality >= 3: Increase repetitions, calculate new interval
5. Update ease factor based on quality
6. Schedule next review = today + interval
```

### Database Models

#### FlashCard
Represents a flashcard with SM-2 state.

```python
class FlashCard(Base):
    __tablename__ = "flashcards"
    
    id: int (primary key)
    student_id: int (foreign key → students)
    concept: str
    question: str
    answer: str
    difficulty: str (easy, medium, hard)
    interval: int (days between reviews, default 1)
    ease_factor: float (difficulty multiplier, default 2.5)
    repetitions: int (consecutive successes, default 0)
    next_review: datetime (default now)
    last_review: datetime
    created_at: datetime
    updated_at: datetime
```

**Key Methods:**
- `calculate_sm2_next_review(quality)`: Compute next review date
- `is_due()`: Check if card is due for review
- `get_retention_rate()`: Calculate success rate

#### ReviewSession
Tracks flashcard review history.

```python
class ReviewSession(Base):
    __tablename__ = "review_sessions"
    
    id: int (primary key)
    flashcard_id: int (foreign key → flashcards)
    quality: int (0-5)
    interval_before: int
    interval_after: int
    ease_factor_before: float
    ease_factor_after: float
    reviewed_at: datetime
```

### Backend Services

SM-2 algorithm implemented directly in FlashCard model's `calculate_sm2_next_review()` method.

**SM-2 Implementation:**
```python
def calculate_sm2_next_review(self, quality: int):
    """Calculate next review using SM-2 algorithm"""
    if quality < 3:
        # Failed recall
        self.repetitions = 0
        self.interval = 1
    else:
        # Successful recall
        if self.repetitions == 0:
            self.interval = 1
        elif self.repetitions == 1:
            self.interval = 6
        else:
            self.interval = int(self.interval * self.ease_factor)
        
        self.repetitions += 1
    
    # Update ease factor
    self.ease_factor = max(1.3, 
        self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )
    
    # Schedule next review
    self.next_review = datetime.now() + timedelta(days=self.interval)
    self.last_review = datetime.now()
```

### API Endpoints

#### 1. Create Flashcard
```
POST /api/v1/smart-recommendations/flashcards/create
```

**Request Body:**
```json
{
  "concept": "Pythagorean Theorem",
  "question": "What is the formula for Pythagorean theorem?",
  "answer": "a² + b² = c²",
  "difficulty": "easy"
}
```

#### 2. Get Due Flashcards
```
GET /api/v1/smart-recommendations/flashcards/due
```

**Response:**
```json
[
  {
    "id": 1,
    "concept": "Pythagorean Theorem",
    "question": "What is the formula?",
    "interval": 1,
    "ease_factor": 2.5,
    "repetitions": 0
  }
]
```

#### 3. Review Flashcard
```
POST /api/v1/smart-recommendations/flashcards/{id}/review
```

**Request Body:**
```json
{
  "quality": 4
}
```

**Response:**
```json
{
  "id": 1,
  "new_interval": 6,
  "new_ease_factor": 2.6,
  "repetitions": 1,
  "next_review": "2025-01-28T12:00:00"
}
```

**Quality Scale:**
- 5: Perfect recall
- 4: Correct after hesitation
- 3: Correct with difficulty
- 2: Incorrect but remembered
- 1: Incorrect, vaguely familiar
- 0: Complete blackout

#### 4. Get Upcoming Reviews
```
GET /api/v1/smart-recommendations/flashcards/upcoming?days=7
```

**Response:**
```json
{
  "total_upcoming": 15,
  "by_day": [
    {"date": "2025-01-23", "count": 5},
    {"date": "2025-01-24", "count": 3},
    {"date": "2025-01-25", "count": 7}
  ]
}
```

#### 5. Get Flashcard Statistics
```
GET /api/v1/smart-recommendations/flashcards/stats
```

**Response:**
```json
{
  "total_cards": 50,
  "cards_due": 5,
  "cards_mastered": 20,
  "total_reviews": 180,
  "average_ease_factor": 2.45,
  "accuracy": 82.5,
  "current_streak": 7
}
```

#### 6. Delete Flashcard
```
DELETE /api/v1/smart-recommendations/flashcards/{id}
```

---

## Frontend Implementation

### Flashcards Page
**File:** `app/flashcards/page.tsx` (460 lines)

**Features:**
- ✅ Create new flashcards (concept, question, answer, difficulty)
- ✅ Review due flashcards with show/hide answer
- ✅ SM-2 quality rating buttons (0-5 with labels)
- ✅ Statistics dashboard (due cards, accuracy, streak, mastered)
- ✅ Progress through review deck
- ✅ Empty states for no cards and all caught up
- ✅ Algorithm explanation section

**UI Components:**
```tsx
// Statistics Cards
<div className="grid grid-cols-4 gap-4">
  <StatCard title="Due Now" value={dueCards.length} />
  <StatCard title="Accuracy" value={accuracy} />
  <StatCard title="Streak" value={streak} />
  <StatCard title="Mastered" value={mastered} />
</div>

// Review Card
<Card>
  <Question>{currentCard.question}</Question>
  {showAnswer && <Answer>{currentCard.answer}</Answer>}
  <Button onClick={() => setShowAnswer(true)}>Show Answer</Button>
</Card>

// Quality Rating Buttons
<div className="quality-buttons">
  <Button quality={0}>Complete Blackout</Button>
  <Button quality={1}>Incorrect</Button>
  <Button quality={2}>Remembered</Button>
  <Button quality={3}>Correct (Hard)</Button>
  <Button quality={4}>Correct (Good)</Button>
  <Button quality={5}>Perfect</Button>
</div>
```

### Navigation Update
**File:** `app/components/Navigation.tsx`

Added Flashcards link:
```tsx
{ name: 'Flashcards', href: '/flashcards', icon: Layers }
```

---

## Integration & Architecture

### Database Schema Updates

#### Models Package
**File:** `backend/app/models/__init__.py`

Added exports:
```python
from .smart_recommendations import (
    BanditState,
    UserInteraction,
    SimilarStudent,
    FlashCard,
    ReviewSession
)

__all__ = [
    # ... existing exports
    "BanditState",
    "UserInteraction",
    "SimilarStudent",
    "FlashCard",
    "ReviewSession"
]
```

#### Student Model
**File:** `backend/app/models/models.py`

Added relationship:
```python
class Student(Base):
    # ... existing fields
    bandit_state = relationship("BanditState", back_populates="student", uselist=False)
```

### API Router Registration
**File:** `backend/main.py`

```python
from app.api import smart_recommendations

app.include_router(
    smart_recommendations.router,
    prefix=settings.API_V1_STR
)
```

---

## Testing

### Test File
**File:** `test_phase_12.py` (820 lines)

**Test Coverage:**

#### MAB Tests
- ✅ Content type selection (epsilon-greedy)
- ✅ Feedback submission with reward calculation
- ✅ Bandit statistics and arm values

#### Collaborative Filtering Tests
- ✅ Record user interactions
- ✅ Find similar students (cosine similarity)
- ✅ Peer-based recommendations
- ✅ Peer insights (top-rated, struggled content)

#### Spaced Repetition Tests
- ✅ Create flashcards
- ✅ Get due flashcards
- ✅ Review with SM-2 quality ratings (0-5)
- ✅ Upcoming review schedule
- ✅ Overall statistics and streaks

**Run Tests:**
```bash
cd mini_project
python test_phase_12.py
```

---

## Usage Examples

### Multi-Armed Bandit Flow
```python
# 1. Get recommended content type
response = await fetch('/api/v1/smart-recommendations/content-type')
# → { "content_type": "video", "strategy": "exploitation" }

# 2. Student interacts with video content
# ... student watches video, answers questions ...

# 3. Submit feedback to update bandit
await fetch('/api/v1/smart-recommendations/content-type/feedback', {
  method: 'POST',
  body: JSON.stringify({
    content_type: 'video',
    correct: true,
    time_spent: 180,
    engagement_score: 0.9
  })
})
# → { "reward": 0.867, "updated_value": 0.85 }
```

### Collaborative Filtering Flow
```python
# 1. Record interaction after completing content
await fetch('/api/v1/smart-recommendations/interactions', {
  method: 'POST',
  body: JSON.stringify({
    content_id: 101,
    content_type: 'video',
    rating: 5,
    interaction_type: 'complete',
    time_spent: 180
  })
})

# 2. Get recommendations based on similar students
response = await fetch('/api/v1/smart-recommendations/peer-recommendations?top_n=5')
# → { "recommendations": [{ content_id: 205, predicted_rating: 4.7 }] }

# 3. Get insights about what peers struggled with
response = await fetch('/api/v1/smart-recommendations/peer-insights')
# → Shows content highly rated by similar students and common struggles
```

### Spaced Repetition Flow
```python
# 1. Create flashcard
await fetch('/api/v1/smart-recommendations/flashcards/create', {
  method: 'POST',
  body: JSON.stringify({
    concept: 'Pythagorean Theorem',
    question: 'What is the formula?',
    answer: 'a² + b² = c²',
    difficulty: 'easy'
  })
})

# 2. Get cards due for review
response = await fetch('/api/v1/smart-recommendations/flashcards/due')
# → [{ id: 1, concept: 'Pythagorean Theorem', ... }]

# 3. Review card with quality rating
await fetch('/api/v1/smart-recommendations/flashcards/1/review', {
  method: 'POST',
  body: JSON.stringify({ quality: 4 })  // Correct after hesitation
})
# → { new_interval: 6, next_review: '2025-01-28', ... }

# 4. Check statistics
response = await fetch('/api/v1/smart-recommendations/flashcards/stats')
# → { total_cards: 10, cards_due: 3, accuracy: 85%, streak: 5 }
```

---

## Algorithm Explanations

### Epsilon-Greedy Strategy
```
ε = 0.1 (exploration rate)

If random(0,1) < ε:
    # Exploration: Try random content type
    selected = random_choice([video, text, interactive, quiz])
else:
    # Exploitation: Select best content type
    selected = argmax(arm_values)
```

**Benefits:**
- Balances exploration (discovering new preferences)
- Exploits known preferences (maximize reward)
- Adapts to changing student preferences over time

### Cosine Similarity
```
Given two students A and B with interaction vectors:
A = [rating_1, rating_2, ..., rating_n]
B = [rating_1, rating_2, ..., rating_n]

similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = sum of element-wise products
- ||A|| = sqrt(sum of squared elements)
- Result ranges from 0 (no similarity) to 1 (identical)
```

**Benefits:**
- Finds students with similar learning preferences
- Invariant to rating scale
- Works well with sparse data

### SM-2 Algorithm
```
Input: quality (0-5)

1. Update repetitions:
   If quality < 3:
       repetitions = 0
       interval = 1 day
   Else:
       repetitions += 1
       
2. Calculate interval:
   If repetitions = 1: interval = 1 day
   If repetitions = 2: interval = 6 days
   Else: interval = previous_interval × ease_factor

3. Update ease factor:
   ease_factor += 0.1 - (5-quality) × (0.08 + (5-quality) × 0.02)
   ease_factor = max(1.3, ease_factor)

4. Schedule next review:
   next_review = today + interval
```

**Benefits:**
- Adapts to individual card difficulty
- Optimizes long-term retention
- Efficient review scheduling

---

## Performance Considerations

### Multi-Armed Bandit
- **Database Queries:** 1 SELECT + 1 UPDATE per arm selection
- **Memory:** O(4) constant space per student (4 arms)
- **Scalability:** Independent per student, highly parallelizable

### Collaborative Filtering
- **Matrix Building:** O(U × I) where U=users, I=items
- **Similarity Calculation:** O(U²) worst case
- **Optimization:** Precompute similarity matrix, cache results
- **Refresh Strategy:** Recompute every N interactions or daily

### Spaced Repetition
- **Review Lookup:** Indexed by student_id and next_review
- **Update Complexity:** O(1) per review
- **Scalability:** Millions of flashcards per student

---

## Files Created/Modified Summary

### New Files (6)
1. `backend/app/models/smart_recommendations.py` (280 lines) - 5 database models
2. `backend/app/services/content_bandit.py` (185 lines) - MAB implementation
3. `backend/app/services/collaborative_filtering.py` (265 lines) - CF implementation
4. `backend/app/api/smart_recommendations.py` (675 lines) - 15+ API endpoints
5. `app/flashcards/page.tsx` (460 lines) - Flashcard review UI
6. `test_phase_12.py` (820 lines) - Comprehensive test suite

### Modified Files (4)
1. `backend/app/models/models.py` - Added bandit_state relationship
2. `backend/app/models/__init__.py` - Exported new models
3. `backend/main.py` - Registered smart_recommendations router
4. `app/components/Navigation.tsx` - Added Flashcards link

**Total Lines Added:** ~2,685 lines of production code + tests

---

## API Endpoints Summary

### Multi-Armed Bandit (3 endpoints)
- `GET /api/v1/smart-recommendations/content-type` - Get recommendation
- `POST /api/v1/smart-recommendations/content-type/feedback` - Submit feedback
- `GET /api/v1/smart-recommendations/bandit-stats` - Get statistics

### Collaborative Filtering (4 endpoints)
- `POST /api/v1/smart-recommendations/interactions` - Record interaction
- `GET /api/v1/smart-recommendations/peer-recommendations` - Get recommendations
- `GET /api/v1/smart-recommendations/similar-students` - Find similar students
- `GET /api/v1/smart-recommendations/peer-insights` - Get peer insights

### Spaced Repetition (8 endpoints)
- `POST /api/v1/smart-recommendations/flashcards/create` - Create flashcard
- `GET /api/v1/smart-recommendations/flashcards/due` - Get due cards
- `POST /api/v1/smart-recommendations/flashcards/{id}/review` - Review card
- `GET /api/v1/smart-recommendations/flashcards/upcoming` - Upcoming schedule
- `GET /api/v1/smart-recommendations/flashcards/stats` - Get statistics
- `DELETE /api/v1/smart-recommendations/flashcards/{id}` - Delete card
- `GET /api/v1/smart-recommendations/flashcards/{id}` - Get single card
- `GET /api/v1/smart-recommendations/flashcards/all` - Get all cards

**Total:** 15 API endpoints

---

## Key Achievements ✅

1. **Multi-Armed Bandit Implementation**
   - ✅ Epsilon-greedy algorithm working
   - ✅ Automatic content type optimization
   - ✅ Reward calculation from multiple signals
   - ✅ Arm value tracking and updates

2. **Collaborative Filtering**
   - ✅ User-item interaction matrix
   - ✅ Cosine similarity calculation
   - ✅ Top-K similar students
   - ✅ Peer-based recommendations
   - ✅ Insights into common struggles

3. **Spaced Repetition System**
   - ✅ SM-2 algorithm fully implemented
   - ✅ Quality rating scale (0-5)
   - ✅ Interval and ease factor calculation
   - ✅ Review scheduling
   - ✅ Statistics and streaks
   - ✅ Complete flashcard UI

4. **Integration**
   - ✅ All models integrated with existing schema
   - ✅ API router registered
   - ✅ Frontend navigation updated
   - ✅ Authentication working on all endpoints

5. **Testing**
   - ✅ Comprehensive test suite
   - ✅ Tests for all three sub-systems
   - ✅ API endpoint validation

---

## Next Steps (Phase 13: Mastery-Based Progression)

Phase 12 is complete! Ready to move to Phase 13:

1. **Competency-Based Learning Paths**
   - Skill tree structure (DAG)
   - Prerequisite tracking
   - Mastery criteria

2. **Micro-Credentials**
   - Badge system
   - Skill verification
   - Portfolio building

3. **Personalized Study Plans**
   - Goal setting
   - Time-based planning
   - Adaptive schedules

---

## Conclusion

Phase 12 successfully implements three complementary recommendation systems:
- **MAB** learns optimal content types through exploration and exploitation
- **CF** leverages peer data to discover relevant content
- **SRS** optimizes long-term retention with spaced repetition

All systems are production-ready with comprehensive testing, documentation, and integration with the existing RL tutor platform.

**Status:** ✅ Phase 12 COMPLETE - Ready for Phase 13! 🎉
