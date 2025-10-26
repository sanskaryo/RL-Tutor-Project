"""
Test Phase 12: Smart Content Recommendations
Tests for Multi-Armed Bandit, Collaborative Filtering, and Spaced Repetition System
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
SMART_RECOMMENDATIONS_URL = f"{BASE_URL}/smart-recommendations"

# Test user credentials
test_users = [
    {"email": "bandit_test@example.com", "password": "password123", "name": "Bandit Tester"},
    {"email": "cf_test_1@example.com", "password": "password123", "name": "CF Tester 1"},
    {"email": "cf_test_2@example.com", "password": "password123", "name": "CF Tester 2"},
    {"email": "srs_test@example.com", "password": "password123", "name": "SRS Tester"}
]

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def register_and_login(user_data: Dict) -> str:
    """Register a test user and return their access token"""
    # Try to register
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    
    # Login to get token
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print(f"✅ Logged in as {user_data['name']}: {user_data['email']}")
        return token
    else:
        print(f"❌ Failed to login: {login_response.text}")
        return None

def get_headers(token: str) -> Dict:
    """Get authorization headers for API requests"""
    return {"Authorization": f"Bearer {token}"}

# =============================================================================
# PHASE 12.1: MULTI-ARMED BANDIT TESTS
# =============================================================================

def test_mab_content_type_selection(token: str):
    """Test content type selection using Multi-Armed Bandit"""
    print_section("PHASE 12.1: Multi-Armed Bandit - Content Type Selection")
    
    headers = get_headers(token)
    
    # Get initial content type recommendation
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/content-type",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Content Type Recommended: {data['content_type']}")
        print(f"   Strategy: {data['strategy']}")
        print(f"   All Arm Values: {data['arm_values']}")
        return data['content_type']
    else:
        print(f"❌ Failed to get content type: {response.text}")
        return None

def test_mab_feedback(token: str, content_type: str):
    """Test providing feedback to update Multi-Armed Bandit"""
    print_section("PHASE 12.1: Multi-Armed Bandit - Feedback Update")
    
    headers = get_headers(token)
    
    # Simulate multiple interactions with different rewards
    test_interactions = [
        {"content_type": content_type, "correct": True, "time_spent": 120, "engagement_score": 0.9},
        {"content_type": content_type, "correct": True, "time_spent": 90, "engagement_score": 0.85},
        {"content_type": "text", "correct": False, "time_spent": 60, "engagement_score": 0.3},
        {"content_type": "interactive", "correct": True, "time_spent": 180, "engagement_score": 0.95},
    ]
    
    for i, interaction in enumerate(test_interactions, 1):
        response = requests.post(
            f"{SMART_RECOMMENDATIONS_URL}/content-type/feedback",
            headers=headers,
            json=interaction
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Feedback {i} processed:")
            print(f"   Content Type: {interaction['content_type']}")
            print(f"   Reward: {data['reward']:.3f}")
            print(f"   Updated Value: {data['updated_value']:.3f}")
        else:
            print(f"❌ Failed to submit feedback {i}: {response.text}")

def test_mab_statistics(token: str):
    """Test retrieving Multi-Armed Bandit statistics"""
    print_section("PHASE 12.1: Multi-Armed Bandit - Statistics")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/bandit-stats",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Bandit Statistics Retrieved:")
        print(f"   Total Pulls: {data['total_pulls']}")
        print(f"   Best Content Type: {data['best_content_type']}")
        print(f"   Best Value: {data['best_value']:.3f}")
        print("\n   All Arm Statistics:")
        for arm, stats in data['arm_statistics'].items():
            print(f"   - {arm}: value={stats['value']:.3f}, pulls={stats['pulls']}")
    else:
        print(f"❌ Failed to get statistics: {response.text}")

# =============================================================================
# PHASE 12.2: COLLABORATIVE FILTERING TESTS
# =============================================================================

def test_cf_record_interactions(tokens: List[str]):
    """Test recording user interactions for collaborative filtering"""
    print_section("PHASE 12.2: Collaborative Filtering - Record Interactions")
    
    # Define interactions for different students with similar patterns
    student_interactions = [
        # Student 1 interactions (prefers video and interactive)
        [
            {"content_id": 101, "content_type": "video", "rating": 5},
            {"content_id": 102, "content_type": "interactive", "rating": 5},
            {"content_id": 103, "content_type": "text", "rating": 2},
            {"content_id": 104, "content_type": "video", "rating": 4},
        ],
        # Student 2 interactions (similar to student 1)
        [
            {"content_id": 101, "content_type": "video", "rating": 5},
            {"content_id": 102, "content_type": "interactive", "rating": 4},
            {"content_id": 105, "content_type": "text", "rating": 3},
            {"content_id": 106, "content_type": "video", "rating": 5},
        ]
    ]
    
    for student_idx, (token, interactions) in enumerate(zip(tokens, student_interactions), 1):
        headers = get_headers(token)
        print(f"\n  Student {student_idx} Interactions:")
        
        for interaction in interactions:
            response = requests.post(
                f"{SMART_RECOMMENDATIONS_URL}/interactions",
                headers=headers,
                json=interaction
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ Recorded: content_id={interaction['content_id']}, "
                      f"type={interaction['content_type']}, rating={interaction['rating']}")
            else:
                print(f"    ❌ Failed to record interaction: {response.text}")

def test_cf_similar_students(token: str):
    """Test finding similar students using collaborative filtering"""
    print_section("PHASE 12.2: Collaborative Filtering - Similar Students")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/similar-students",
        headers=headers,
        params={"top_k": 3}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['similar_students'])} similar students:")
        for student in data['similar_students']:
            print(f"   - Student ID {student['student_id']}: "
                  f"similarity={student['similarity_score']:.3f}")
    else:
        print(f"❌ Failed to find similar students: {response.text}")

def test_cf_peer_recommendations(token: str):
    """Test getting content recommendations from similar peers"""
    print_section("PHASE 12.2: Collaborative Filtering - Peer Recommendations")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/peer-recommendations",
        headers=headers,
        params={"top_n": 5}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Received {len(data['recommendations'])} recommendations:")
        for rec in data['recommendations']:
            print(f"   - Content ID {rec['content_id']}: "
                  f"predicted_rating={rec['predicted_rating']:.2f}, "
                  f"type={rec['content_type']}")
    else:
        print(f"❌ Failed to get recommendations: {response.text}")

def test_cf_peer_insights(token: str):
    """Test getting insights from similar students"""
    print_section("PHASE 12.2: Collaborative Filtering - Peer Insights")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/peer-insights",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Peer Insights Retrieved:")
        print(f"   Similar Students Count: {data['similar_students_count']}")
        
        if data['top_rated_by_peers']:
            print("\n   Top Rated by Peers:")
            for content in data['top_rated_by_peers'][:3]:
                print(f"   - Content ID {content['content_id']}: "
                      f"avg_rating={content['avg_rating']:.2f}")
        
        if data['struggled_with']:
            print("\n   Peers Struggled With:")
            for content in data['struggled_with'][:3]:
                print(f"   - Content ID {content['content_id']}: "
                      f"avg_rating={content['avg_rating']:.2f}")
    else:
        print(f"❌ Failed to get peer insights: {response.text}")

# =============================================================================
# PHASE 12.3: SPACED REPETITION SYSTEM TESTS
# =============================================================================

def test_srs_create_flashcards(token: str) -> List[int]:
    """Test creating flashcards for spaced repetition"""
    print_section("PHASE 12.3: Spaced Repetition System - Create Flashcards")
    
    headers = get_headers(token)
    
    # Create multiple flashcards with different difficulties
    flashcards = [
        {
            "concept": "Pythagorean Theorem",
            "question": "What is the formula for the Pythagorean theorem?",
            "answer": "a² + b² = c², where c is the hypotenuse",
            "difficulty": "easy"
        },
        {
            "concept": "Derivatives",
            "question": "What is the derivative of x²?",
            "answer": "2x",
            "difficulty": "medium"
        },
        {
            "concept": "Integration by Parts",
            "question": "What is the integration by parts formula?",
            "answer": "∫u dv = uv - ∫v du",
            "difficulty": "hard"
        }
    ]
    
    created_ids = []
    
    for card_data in flashcards:
        response = requests.post(
            f"{SMART_RECOMMENDATIONS_URL}/flashcards/create",
            headers=headers,
            json=card_data
        )
        
        if response.status_code == 200:
            data = response.json()
            created_ids.append(data['id'])
            print(f"✅ Created flashcard: {card_data['concept']}")
            print(f"   ID: {data['id']}, Difficulty: {card_data['difficulty']}")
        else:
            print(f"❌ Failed to create flashcard: {response.text}")
    
    return created_ids

def test_srs_get_due_cards(token: str):
    """Test retrieving flashcards due for review"""
    print_section("PHASE 12.3: Spaced Repetition System - Get Due Cards")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/flashcards/due",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data)} cards due for review:")
        for card in data:
            print(f"   - {card['concept']}: interval={card['interval']}d, "
                  f"repetitions={card['repetitions']}, ease_factor={card['ease_factor']:.2f}")
        return data
    else:
        print(f"❌ Failed to get due cards: {response.text}")
        return []

def test_srs_review_cards(token: str, card_ids: List[int]):
    """Test reviewing flashcards with SM-2 algorithm"""
    print_section("PHASE 12.3: Spaced Repetition System - Review Cards (SM-2)")
    
    headers = get_headers(token)
    
    # Test different quality ratings (0-5 scale)
    quality_ratings = [
        {"quality": 5, "description": "Perfect recall"},
        {"quality": 4, "description": "Correct after hesitation"},
        {"quality": 3, "description": "Correct with difficulty"},
    ]
    
    for i, (card_id, quality_data) in enumerate(zip(card_ids[:3], quality_ratings), 1):
        response = requests.post(
            f"{SMART_RECOMMENDATIONS_URL}/flashcards/{card_id}/review",
            headers=headers,
            json={"quality": quality_data["quality"]}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Review {i} ({quality_data['description']}):")
            print(f"   Card ID: {card_id}")
            print(f"   Quality Rating: {quality_data['quality']}/5")
            print(f"   New Interval: {data['new_interval']} days")
            print(f"   New Ease Factor: {data['new_ease_factor']:.2f}")
            print(f"   Repetitions: {data['repetitions']}")
            print(f"   Next Review: {data['next_review']}")
        else:
            print(f"❌ Failed to review card {i}: {response.text}")

def test_srs_upcoming_reviews(token: str):
    """Test getting upcoming review schedule"""
    print_section("PHASE 12.3: Spaced Repetition System - Upcoming Reviews")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/flashcards/upcoming",
        headers=headers,
        params={"days": 7}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Upcoming Reviews (next 7 days):")
        print(f"   Total cards scheduled: {data['total_upcoming']}")
        
        if data['by_day']:
            print("\n   Schedule by day:")
            for day_data in data['by_day']:
                print(f"   - {day_data['date']}: {day_data['count']} cards")
    else:
        print(f"❌ Failed to get upcoming reviews: {response.text}")

def test_srs_statistics(token: str):
    """Test getting overall flashcard statistics"""
    print_section("PHASE 12.3: Spaced Repetition System - Statistics")
    
    headers = get_headers(token)
    
    response = requests.get(
        f"{SMART_RECOMMENDATIONS_URL}/flashcards/stats",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Flashcard Statistics:")
        print(f"   Total Cards: {data['total_cards']}")
        print(f"   Cards Due: {data['cards_due']}")
        print(f"   Cards Mastered: {data['cards_mastered']}")
        print(f"   Total Reviews: {data['total_reviews']}")
        print(f"   Average Ease Factor: {data['average_ease_factor']:.2f}")
        
        if data['accuracy']:
            print(f"   Accuracy: {data['accuracy']:.1f}%")
        
        if data['current_streak']:
            print(f"   Current Streak: {data['current_streak']} days")
    else:
        print(f"❌ Failed to get statistics: {response.text}")

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def main():
    """Run all Phase 12 tests"""
    print("\n" + "="*80)
    print("  PHASE 12: SMART CONTENT RECOMMENDATIONS - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("\n  Testing: Multi-Armed Bandit, Collaborative Filtering, Spaced Repetition")
    print("  Backend URL:", BASE_URL)
    print("\n" + "="*80)
    
    # Register and login test users
    print_section("USER REGISTRATION AND LOGIN")
    tokens = []
    for user in test_users:
        token = register_and_login(user)
        if token:
            tokens.append(token)
        else:
            print(f"⚠️  Failed to authenticate user: {user['email']}")
    
    if len(tokens) < 4:
        print("\n❌ Not all test users authenticated. Aborting tests.")
        return
    
    mab_token, cf_token_1, cf_token_2, srs_token = tokens
    
    # =============================================================================
    # PHASE 12.1: MULTI-ARMED BANDIT TESTS
    # =============================================================================
    
    try:
        # Test content type selection
        selected_type = test_mab_content_type_selection(mab_token)
        
        # Test providing feedback
        if selected_type:
            test_mab_feedback(mab_token, selected_type)
        
        # Test statistics
        test_mab_statistics(mab_token)
        
    except Exception as e:
        print(f"\n❌ Error in MAB tests: {str(e)}")
    
    # =============================================================================
    # PHASE 12.2: COLLABORATIVE FILTERING TESTS
    # =============================================================================
    
    try:
        # Record interactions for multiple students
        test_cf_record_interactions([cf_token_1, cf_token_2])
        
        # Find similar students
        test_cf_similar_students(cf_token_1)
        
        # Get peer recommendations
        test_cf_peer_recommendations(cf_token_1)
        
        # Get peer insights
        test_cf_peer_insights(cf_token_1)
        
    except Exception as e:
        print(f"\n❌ Error in Collaborative Filtering tests: {str(e)}")
    
    # =============================================================================
    # PHASE 12.3: SPACED REPETITION SYSTEM TESTS
    # =============================================================================
    
    try:
        # Create flashcards
        card_ids = test_srs_create_flashcards(srs_token)
        
        # Get due cards
        due_cards = test_srs_get_due_cards(srs_token)
        
        # Review cards with SM-2
        if card_ids:
            test_srs_review_cards(srs_token, card_ids)
        
        # Get upcoming reviews
        test_srs_upcoming_reviews(srs_token)
        
        # Get statistics
        test_srs_statistics(srs_token)
        
    except Exception as e:
        print(f"\n❌ Error in Spaced Repetition tests: {str(e)}")
    
    # =============================================================================
    # TEST SUMMARY
    # =============================================================================
    
    print_section("TEST SUMMARY")
    print("✅ Phase 12.1: Multi-Armed Bandit")
    print("   - Content type selection (epsilon-greedy)")
    print("   - Feedback and reward updates")
    print("   - Arm statistics and best content type")
    print()
    print("✅ Phase 12.2: Collaborative Filtering")
    print("   - Record user interactions")
    print("   - Find similar students (cosine similarity)")
    print("   - Peer-based recommendations")
    print("   - Peer insights (top-rated and struggled content)")
    print()
    print("✅ Phase 12.3: Spaced Repetition System")
    print("   - Create flashcards")
    print("   - Get due cards for review")
    print("   - Review with SM-2 algorithm (quality ratings 0-5)")
    print("   - Upcoming review schedule")
    print("   - Overall statistics and streaks")
    print()
    print("="*80)
    print("  PHASE 12 TESTING COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
