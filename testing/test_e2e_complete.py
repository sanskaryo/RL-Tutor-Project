"""
End-to-End Test Suite for RL Educational Tutor
Tests complete user journey: Register → Login → Learning Style Quiz → Dashboard → Learning
"""
import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class E2ETestSuite:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        self.test_username = f"testuser{int(time.time())}"
        self.test_email = f"test_user_{int(time.time())}@example.com"
        self.test_password = "TestPassword123!"
        self.passed_tests = 0
        self.failed_tests = 0
        
    def print_test(self, test_name: str):
        """Print test header"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}TEST: {test_name}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}+ {message}{Colors.ENDC}")
        self.passed_tests += 1
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.FAIL}X {message}{Colors.ENDC}")
        self.failed_tests += 1
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.OKCYAN}i {message}{Colors.ENDC}")
    
    def test_1_registration(self) -> bool:
        """Test user registration"""
        self.print_test("1. User Registration")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": self.test_email,
                    "username": self.test_username,
                    "password": self.test_password,
                    "full_name": "E2E Test User"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                # Extract user ID from token - the sub field contains username, not ID
                # We'll need to fetch the user ID from the profile endpoint later
                self.print_success(f"User registered successfully")
                self.print_info(f"Username: {self.test_username}")
                self.print_info(f"Email: {self.test_email}")
                return True
            else:
                self.print_error(f"Registration failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Registration error: {str(e)}")
            return False
    
    def test_2_login(self) -> bool:
        """Test user login"""
        self.print_test("2. User Login & Get Profile")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "username": self.test_username,
                    "password": self.test_password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.print_success("Login successful")
                self.print_info(f"Access token: {self.access_token[:20]}...")
                
                # Get user profile to fetch user ID
                profile_response = requests.get(
                    f"{BASE_URL}/students/me",
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    self.user_id = profile_data.get("id")
                    self.print_success(f"Profile fetched (User ID: {self.user_id})")
                    return True
                else:
                    self.print_error(f"Failed to fetch profile: {profile_response.status_code}")
                    return False
            else:
                self.print_error(f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Login error: {str(e)}")
            return False
    
    def test_3_get_quiz(self) -> bool:
        """Test fetching learning style quiz"""
        self.print_test("3. Fetch Learning Style Quiz")
        
        try:
            response = requests.get(f"{BASE_URL}/quiz")
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get("questions", [])
                self.print_success(f"Quiz fetched successfully")
                self.print_info(f"Total questions: {len(questions)}")
                self.print_info(f"Quiz title: {data.get('quiz_title')}")
                return len(questions) == 20
            else:
                self.print_error(f"Failed to fetch quiz: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Quiz fetch error: {str(e)}")
            return False
    
    def test_4_submit_quiz(self) -> bool:
        """Test submitting learning style quiz"""
        self.print_test("4. Submit Learning Style Quiz")
        
        # Generate sample answers (mix of all learning styles)
        sample_answers = ["V", "A", "R", "K"] * 5  # 20 answers
        
        try:
            response = requests.post(
                f"{BASE_URL}/students/{self.user_id}/learning-style",
                json={"answers": sample_answers},
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Quiz submitted successfully")
                self.print_info(f"Visual Score: {data.get('visual_score')}%")
                self.print_info(f"Auditory Score: {data.get('auditory_score')}%")
                self.print_info(f"Reading Score: {data.get('reading_score')}%")
                self.print_info(f"Kinesthetic Score: {data.get('kinesthetic_score')}%")
                self.print_info(f"Dominant Style: {data.get('dominant_style')}")
                
                # Verify scores
                total = (data.get('visual_score', 0) + data.get('auditory_score', 0) + 
                        data.get('reading_score', 0) + data.get('kinesthetic_score', 0))
                if abs(total - 100) < 0.1:  # Allow for small floating point errors
                    self.print_success("Score calculation verified (total = 100%)")
                    return True
                else:
                    self.print_error(f"Score calculation error (total = {total}%)")
                    return False
            else:
                self.print_error(f"Quiz submission failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Quiz submission error: {str(e)}")
            return False
    
    def test_5_get_learning_style(self) -> bool:
        """Test retrieving learning style profile"""
        self.print_test("5. Retrieve Learning Style Profile")
        
        try:
            response = requests.get(
                f"{BASE_URL}/students/{self.user_id}/learning-style",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Learning style profile retrieved")
                self.print_info(f"Profile created: {data.get('assessed_at')}")
                self.print_info(f"Recommendations: {len(data.get('recommendations', []))} tips")
                return True
            else:
                self.print_error(f"Failed to retrieve profile: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Profile retrieval error: {str(e)}")
            return False
    
    def test_6_analytics_endpoint(self) -> bool:
        """Test analytics endpoint"""
        self.print_test("6. Test Analytics Endpoint")
        
        try:
            response = requests.get(
                f"{BASE_URL}/analytics/dashboard?username={self.test_username}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Analytics endpoint accessible")
                self.print_info(f"Data keys: {list(data.keys())}")
                return True
            else:
                self.print_error(f"Analytics endpoint failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Analytics error: {str(e)}")
            return False
    
    def test_7_session_endpoints(self) -> bool:
        """Test learning session endpoints"""
        self.print_test("7. Test Learning Session Endpoints")
        
        try:
            # Start a learning session using correct endpoint
            response = requests.post(
                f"{BASE_URL}/session/start?username={self.test_username}",
                json={
                    "topic": "algebra"
                },
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code in [200, 201]:
                content_data = response.json()
                content_id = content_data.get("id")
                self.print_success(f"Learning session started - got content ID: {content_id}")
                self.print_info(f"Question: {content_data.get('title', 'N/A')}")
                return True
            else:
                self.print_error(f"Session start failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Session error: {str(e)}")
            return False
    
    def test_8_cors_headers(self) -> bool:
        """Test CORS headers are properly set"""
        self.print_test("8. Test CORS Headers")
        
        try:
            response = requests.options(
                f"{BASE_URL}/auth/register",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST"
                }
            )
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
            }
            
            if cors_headers["Access-Control-Allow-Origin"]:
                self.print_success("CORS headers present")
                for header, value in cors_headers.items():
                    self.print_info(f"{header}: {value}")
                return True
            else:
                self.print_error("CORS headers missing")
                return False
                
        except Exception as e:
            self.print_error(f"CORS test error: {str(e)}")
            return False
    
    def test_9_frontend_accessibility(self) -> bool:
        """Test frontend pages are accessible"""
        self.print_test("9. Test Frontend Accessibility")
        
        pages = [
            "/",
            "/register",
            "/login",
            "/dashboard",
            "/learning-style-quiz",
            "/learn"
        ]
        
        accessible_pages = 0
        for page in pages:
            try:
                response = requests.get(f"{FRONTEND_URL}{page}", timeout=5)
                if response.status_code == 200:
                    self.print_success(f"Page accessible: {page}")
                    accessible_pages += 1
                else:
                    self.print_error(f"Page not accessible: {page} (Status: {response.status_code})")
            except Exception as e:
                self.print_error(f"Page error {page}: {str(e)}")
        
        return accessible_pages == len(pages)
    
    def run_all_tests(self):
        """Run complete E2E test suite"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("="*70)
        print("  RL EDUCATIONAL TUTOR - END-TO-END TEST SUITE")
        print("="*70)
        print(f"{Colors.ENDC}\n")
        
        start_time = time.time()
        
        # Run tests in sequence
        tests = [
            self.test_1_registration,
            self.test_2_login,
            self.test_3_get_quiz,
            self.test_4_submit_quiz,
            self.test_5_get_learning_style,
            self.test_6_analytics_endpoint,
            self.test_7_session_endpoints,
            self.test_8_cors_headers,
            self.test_9_frontend_accessibility
        ]
        
        for test in tests:
            test()
            time.sleep(0.5)  # Brief pause between tests
        
        # Print summary
        duration = time.time() - start_time
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Passed: {self.passed_tests}{Colors.ENDC}")
        print(f"{Colors.FAIL}Failed: {self.failed_tests}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Duration: {duration:.2f} seconds{Colors.ENDC}")
        
        success_rate = (self.passed_tests / (self.passed_tests + self.failed_tests)) * 100
        print(f"{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.ENDC}\n")
        
        if self.failed_tests == 0:
            print(f"{Colors.OKGREEN}{Colors.BOLD}*** ALL TESTS PASSED! ***{Colors.ENDC}\n")
        else:
            print(f"{Colors.WARNING}!!! Some tests failed. Please review the errors above.{Colors.ENDC}\n")

if __name__ == "__main__":
    suite = E2ETestSuite()
    suite.run_all_tests()
