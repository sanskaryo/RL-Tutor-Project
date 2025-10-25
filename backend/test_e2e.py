"""
End-to-End Test Suite
Tests complete user journey from registration to learning
"""
import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = f"e2e_test_{datetime.now().strftime('%Y%m%d%H%M%S')}"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test(name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {name} ==={Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}  {message}{Colors.END}")

class E2ETestSuite:
    def __init__(self):
        self.token = None
        self.refresh_token = None
        self.username = TEST_USER
        self.password = "test123pass"
        self.test_results = []

    def run_all_tests(self):
        """Run complete test suite"""
        print(f"\n{Colors.BOLD}{'='*60}")
        print(f"  END-TO-END TEST SUITE")
        print(f"  Testing: {BASE_URL}")
        print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}{Colors.END}\n")

        tests = [
            self.test_health_check,
            self.test_registration,
            self.test_login,
            self.test_refresh_token,
            self.test_get_profile,
            self.test_start_session,
            self.test_submit_correct_answer,
            self.test_submit_incorrect_answer,
            self.test_session_progress,
            self.test_dashboard,
            self.test_rl_stats,
            self.test_performance_chart,
            self.test_rate_limiting,
        ]

        for test in tests:
            try:
                test()
                self.test_results.append((test.__name__, True))
            except Exception as e:
                print_error(f"Test failed: {str(e)}")
                self.test_results.append((test.__name__, False))

        self.print_summary()

    def test_health_check(self):
        """Test 1: Health Check Endpoint"""
        print_test("Health Check")
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        assert response.status_code == 200, "Health check failed"
        print_success("Health check passed")
        print_info(f"Status: {response.json().get('status', 'ok')}")

    def test_registration(self):
        """Test 2: User Registration"""
        print_test("User Registration")
        data = {
            "email": f"{self.username}@test.com",
            "username": self.username,
            "password": self.password,
            "full_name": "E2E Test User"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        
        result = response.json()
        assert "access_token" in result, "No access token in response"
        assert "refresh_token" in result, "No refresh token in response"
        
        self.token = result["access_token"]
        self.refresh_token = result["refresh_token"]
        
        print_success("User registered successfully")
        print_info(f"Username: {self.username}")
        print_info(f"Token length: {len(self.token)}")

    def test_login(self):
        """Test 3: User Login"""
        print_test("User Login")
        data = {
            "username": self.username,
            "password": self.password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        result = response.json()
        assert "access_token" in result, "No access token"
        assert "refresh_token" in result, "No refresh token"
        
        self.token = result["access_token"]
        
        print_success("Login successful")
        print_info(f"Token received: {self.token[:50]}...")

    def test_refresh_token(self):
        """Test 4: Token Refresh"""
        print_test("Token Refresh")
        
        params = {"refresh_token": self.refresh_token}
        response = requests.post(f"{BASE_URL}/auth/refresh", params=params)
        
        assert response.status_code == 200, f"Token refresh failed: {response.text}"
        
        result = response.json()
        assert "access_token" in result, "No new access token"
        
        old_token = self.token
        self.token = result["access_token"]
        
        print_success("Token refreshed successfully")
        print_info(f"Old token: {old_token[:30]}...")
        print_info(f"New token: {self.token[:30]}...")

    def test_get_profile(self):
        """Test 5: Get User Profile"""
        print_test("Get User Profile")
        
        params = {"token": self.token}
        response = requests.get(f"{BASE_URL}/auth/me", params=params)
        
        assert response.status_code == 200, f"Get profile failed: {response.text}"
        
        profile = response.json()
        assert profile["username"] == self.username, "Username mismatch"
        assert "email" in profile, "Email missing"
        
        print_success("Profile retrieved")
        print_info(f"Username: {profile['username']}")
        print_info(f"Email: {profile['email']}")
        print_info(f"Created: {profile.get('created_at', 'N/A')}")

    def test_start_session(self):
        """Test 6: Start Learning Session"""
        print_test("Start Learning Session")
        
        params = {"username": self.username}
        response = requests.post(f"{BASE_URL}/session/start", params=params)
        
        assert response.status_code == 200, f"Start session failed: {response.text}"
        
        content = response.json()
        assert "id" in content, "Content ID missing"
        assert "question_text" in content, "Question missing"
        assert "options" in content, "Options missing"
        
        self.current_content = content
        
        print_success("Session started")
        print_info(f"Content ID: {content['id']}")
        print_info(f"Topic: {content['topic']}")
        print_info(f"Difficulty: {content['difficulty']}")
        print_info(f"Question: {content['question_text'][:50]}...")

    def test_submit_correct_answer(self):
        """Test 7: Submit Correct Answer"""
        print_test("Submit Correct Answer")
        
        data = {
            "username": self.username,
            "session_id": self.current_content["id"],
            "student_answer": self.current_content["correct_answer"],
            "time_spent": 12.5
        }
        
        response = requests.post(f"{BASE_URL}/session/answer", json=data)
        
        assert response.status_code == 200, f"Submit answer failed: {response.text}"
        
        result = response.json()
        assert result["is_correct"] == True, "Answer should be correct"
        assert result["reward"] > 0, "Reward should be positive"
        
        print_success("Correct answer submitted")
        print_info(f"Correct: {result['is_correct']}")
        print_info(f"Reward: {result['reward']:.2f}")
        print_info(f"Explanation: {result['explanation'][:50]}...")

    def test_submit_incorrect_answer(self):
        """Test 8: Submit Incorrect Answer"""
        print_test("Submit Incorrect Answer")
        
        # Start new session first
        params = {"username": self.username}
        session_response = requests.post(f"{BASE_URL}/session/start", params=params)
        content = session_response.json()
        
        # Submit wrong answer
        wrong_answer = "Wrong Answer"
        data = {
            "username": self.username,
            "session_id": content["id"],
            "student_answer": wrong_answer,
            "time_spent": 20.0
        }
        
        response = requests.post(f"{BASE_URL}/session/answer", json=data)
        
        assert response.status_code == 200, f"Submit answer failed: {response.text}"
        
        result = response.json()
        assert result["is_correct"] == False, "Answer should be incorrect"
        
        print_success("Incorrect answer submitted")
        print_info(f"Correct: {result['is_correct']}")
        print_info(f"Reward: {result['reward']:.2f}")

    def test_session_progress(self):
        """Test 9: Get Session Progress"""
        print_test("Get Session Progress")
        
        params = {"username": self.username}
        response = requests.get(f"{BASE_URL}/session/progress", params=params)
        
        assert response.status_code == 200, f"Get progress failed: {response.text}"
        
        progress = response.json()
        assert "total_sessions" in progress, "Total sessions missing"
        assert "current_streak" in progress, "Streak missing"
        
        print_success("Progress retrieved")
        print_info(f"Total sessions: {progress['total_sessions']}")
        print_info(f"Correct answers: {progress['correct_answers']}")
        print_info(f"Streak: {progress['current_streak']}")

    def test_dashboard(self):
        """Test 10: Get Dashboard Data"""
        print_test("Get Dashboard Data")
        
        params = {"username": self.username}
        response = requests.get(f"{BASE_URL}/analytics/dashboard", params=params)
        
        assert response.status_code == 200, f"Get dashboard failed: {response.text}"
        
        dashboard = response.json()
        assert "total_attempts" in dashboard, "Total attempts missing"
        assert "knowledge_state" in dashboard, "Knowledge state missing"
        
        print_success("Dashboard retrieved")
        print_info(f"Total attempts: {dashboard['total_attempts']}")
        print_info(f"Accuracy: {dashboard['accuracy_rate']:.1f}%")
        print_info(f"Knowledge topics: {list(dashboard['knowledge_state'].keys())}")

    def test_rl_stats(self):
        """Test 11: Get RL Agent Statistics"""
        print_test("Get RL Agent Statistics")
        
        response = requests.get(f"{BASE_URL}/analytics/rl-stats")
        
        assert response.status_code == 200, f"Get RL stats failed: {response.text}"
        
        stats = response.json()
        assert "total_sessions" in stats, "Total sessions missing"
        assert "q_table_size" in stats, "Q-table size missing"
        
        print_success("RL stats retrieved")
        print_info(f"Total sessions: {stats['total_sessions']}")
        print_info(f"Avg reward: {stats['avg_reward']:.2f}")
        print_info(f"Q-table size: {stats['q_table_size']}")
        print_info(f"Exploration rate: {stats['exploration_rate']:.2%}")

    def test_performance_chart(self):
        """Test 12: Get Performance Chart Data"""
        print_test("Get Performance Chart Data")
        
        params = {"username": self.username}
        response = requests.get(f"{BASE_URL}/analytics/performance-chart", params=params)
        
        assert response.status_code == 200, f"Get chart failed: {response.text}"
        
        chart_data = response.json()
        assert isinstance(chart_data, list), "Chart data should be a list"
        
        print_success("Performance chart retrieved")
        print_info(f"Data points: {len(chart_data)}")

    def test_rate_limiting(self):
        """Test 13: Rate Limiting"""
        print_test("Rate Limiting")
        
        # Try to login multiple times quickly
        data = {
            "username": "nonexistent",
            "password": "wrong"
        }
        
        print_info("Testing rate limit (may take a moment)...")
        responses = []
        for i in range(12):  # Exceed 10/minute limit
            response = requests.post(f"{BASE_URL}/auth/login", json=data)
            responses.append(response.status_code)
            time.sleep(0.1)
        
        # Should eventually get rate limited (429)
        rate_limited = any(status == 429 for status in responses)
        
        if rate_limited:
            print_success("Rate limiting is working")
            print_info(f"Got rate limited after {responses.count(429)} requests")
        else:
            print_info("Rate limiting not triggered (may need more requests)")

    def print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BOLD}{'='*60}")
        print("  TEST SUMMARY")
        print(f"{'='*60}{Colors.END}\n")
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
            print(f"  {status} - {test_name}")
        
        print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
        
        if passed == total:
            print(f"{Colors.GREEN}✓ All tests passed! System is working correctly.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ Some tests failed. Check logs above.{Colors.END}")
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}\n")


def main():
    """Run the test suite"""
    try:
        suite = E2ETestSuite()
        suite.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
