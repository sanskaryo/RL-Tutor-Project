"""
Test script to verify backend API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("🔍 Testing user registration...")
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "test123",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Token received: {result['access_token'][:20]}...\n")
        return result['access_token']
    else:
        print(f"⚠️  Response: {response.text}\n")
        return None

def test_login():
    """Test user login"""
    print("🔍 Testing user login...")
    data = {
        "username": "testuser",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Token received: {result['access_token'][:20]}...\n")
        return result['access_token']
    else:
        print(f"❌ Response: {response.text}\n")
        return None

def test_start_session(username):
    """Test starting a learning session"""
    print("🔍 Testing start learning session...")
    data = {"topic": "algebra"}
    params = {"username": username}
    response = requests.post(
        f"{BASE_URL}/api/v1/session/start",
        json=data,
        params=params
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Got content: {result['title']}")
        print(f"   Question: {result['question_text']}")
        print(f"   Difficulty: {result['difficulty']}\n")
        return result
    else:
        print(f"❌ Response: {response.text}\n")
        return None

def test_submit_answer(username, content_id):
    """Test submitting an answer"""
    print("🔍 Testing submit answer...")
    data = {
        "session_id": content_id,
        "student_answer": "4",
        "time_spent": 25.5
    }
    params = {"username": username}
    response = requests.post(
        f"{BASE_URL}/api/v1/session/answer",
        json=data,
        params=params
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Answer submitted")
        print(f"   Correct: {result['is_correct']}")
        print(f"   Reward: {result['reward']}")
        print(f"   Explanation: {result['explanation']}\n")
        return result
    else:
        print(f"❌ Response: {response.text}\n")
        return None

def test_dashboard(username):
    """Test dashboard endpoint"""
    print("🔍 Testing dashboard analytics...")
    params = {"username": username}
    response = requests.get(
        f"{BASE_URL}/api/v1/analytics/dashboard",
        params=params
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Dashboard data received")
        print(f"   Student: {result['student']['username']}")
        print(f"   Total Attempts: {result['progress']['total_attempts']}")
        print(f"   Accuracy: {result['progress']['accuracy_rate']:.2%}\n")
        return result
    else:
        print(f"❌ Response: {response.text}\n")
        return None

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 TESTING BACKEND API")
    print("=" * 60 + "\n")
    
    # Test 1: Health check
    if not test_health():
        print("❌ Health check failed. Is the server running?")
        return
    
    # Test 2: Register (might fail if user exists)
    token = test_register()
    
    # Test 3: Login
    token = test_login()
    if not token:
        print("❌ Login failed. Cannot continue tests.")
        return
    
    # Test 4: Start session
    content = test_start_session("testuser")
    if not content:
        print("❌ Session start failed")
        return
    
    # Test 5: Submit answer
    test_submit_answer("testuser", content['id'])
    
    # Test 6: Dashboard
    test_dashboard("testuser")
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
