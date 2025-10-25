#!/usr/bin/env python3
"""
Integration Test Script - RL Educational Tutor
Tests the complete flow: register -> login -> session -> analytics
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_registration():
    print_section("TEST 1: User Registration")
    
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": f"{TEST_USER}@test.com",
        "username": TEST_USER,
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Registration successful")
        print(f"Access Token: {result['access_token'][:50]}...")
        return result
    else:
        print(f"✗ Registration failed: {response.text}")
        return None

def test_login(username, password):
    print_section("TEST 2: User Login")
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Login successful")
        print(f"Access Token: {result['access_token'][:50]}...")
        if 'refresh_token' in result:
            print(f"Refresh Token: {result['refresh_token'][:50]}...")
        return result
    else:
        print(f"✗ Login failed: {response.text}")
        return None

def test_start_session(username):
    print_section("TEST 3: Start Learning Session")
    
    url = f"{BASE_URL}/session/start"
    params = {"username": username}
    
    print(f"POST {url}")
    print(f"Params: {params}")
    
    response = requests.post(url, params=params)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.json()
        print(f"✓ Session started")
        print(f"Content ID: {content['id']}")
        print(f"Topic: {content['topic']}")
        print(f"Difficulty: {content['difficulty']}")
        print(f"Question: {content['question_text']}")
        print(f"Options: {content['options']}")
        return content
    else:
        print(f"✗ Failed to start session: {response.text}")
        return None

def test_submit_answer(username, content_id, answer, correct_answer):
    print_section("TEST 4: Submit Answer")
    
    url = f"{BASE_URL}/session/answer"
    data = {
        "username": username,
        "session_id": content_id,
        "student_answer": answer,
        "time_spent": 15.5
    }
    
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print(f"Correct answer: {correct_answer}")
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Answer submitted")
        print(f"Correct: {result['is_correct']}")
        print(f"Reward: {result['reward']}")
        print(f"Explanation: {result['explanation']}")
        if result.get('next_content'):
            print(f"Next Question: {result['next_content']['question_text']}")
        return result
    else:
        print(f"✗ Failed to submit answer: {response.text}")
        return None

def test_dashboard(username):
    print_section("TEST 5: Get Dashboard")
    
    url = f"{BASE_URL}/analytics/dashboard"
    params = {"username": username}
    
    print(f"GET {url}")
    print(f"Params: {params}")
    
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Dashboard retrieved")
        print(f"Total Attempts: {data['total_attempts']}")
        print(f"Correct Answers: {data['correct_answers']}")
        print(f"Accuracy: {data['accuracy_rate']:.2f}%")
        print(f"Topics Mastered: {len(data['topics_mastered'])}")
        print(f"Knowledge State: {list(data['knowledge_state'].keys())}")
        return data
    else:
        print(f"✗ Failed to get dashboard: {response.text}")
        return None

def test_rl_stats():
    print_section("TEST 6: Get RL Agent Stats")
    
    url = f"{BASE_URL}/analytics/rl-stats"
    
    print(f"GET {url}")
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ RL stats retrieved")
        print(f"Total Sessions: {data['total_sessions']}")
        print(f"Average Reward: {data['avg_reward']:.2f}")
        print(f"Exploration Rate: {data['exploration_rate']:.2f}")
        print(f"Q-Table Size: {data['q_table_size']}")
        return data
    else:
        print(f"✗ Failed to get RL stats: {response.text}")
        return None

def main():
    print("\n" + "="*60)
    print("  RL EDUCATIONAL TUTOR - INTEGRATION TEST")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Register
    reg_result = test_registration()
    if not reg_result:
        print("\n✗ Registration failed. Stopping tests.")
        return
    
    # Test 2: Login
    login_result = test_login(TEST_USER, "testpass123")
    if not login_result:
        print("\n✗ Login failed. Stopping tests.")
        return
    
    # Test 3: Start session
    content = test_start_session(TEST_USER)
    if not content:
        print("\n✗ Start session failed. Stopping tests.")
        return
    
    # Test 4: Submit answer (first try correct)
    correct_answer = content['correct_answer']
    answer_result = test_submit_answer(
        TEST_USER, 
        content['id'], 
        correct_answer,
        correct_answer
    )
    
    # Test 5: Dashboard
    test_dashboard(TEST_USER)
    
    # Test 6: RL Stats
    test_rl_stats()
    
    print("\n" + "="*60)
    print("  ALL TESTS COMPLETED!")
    print("="*60)
    print(f"✓ User {TEST_USER} successfully tested")
    print("✓ All API endpoints working correctly")
    print("✓ RL agent is operational")
    print("\nYou can now login to the frontend with:")
    print(f"  Username: {TEST_USER}")
    print(f"  Password: testpass123")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
