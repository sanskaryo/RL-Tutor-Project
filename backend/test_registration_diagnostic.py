"""
Quick diagnostic script to test registration
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/../health")
        print(f"✅ Backend is running")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend is NOT running: {e}")
        return False

def test_registration():
    """Test registration endpoint"""
    # Use timestamp to ensure unique username
    timestamp = datetime.now().strftime("%H%M%S")
    
    data = {
        "email": f"test{timestamp}@example.com",
        "username": f"testuser{timestamp}",
        "password": "test123",
        "full_name": "Test User"
    }
    
    print(f"\n📤 Attempting registration...")
    print(f"   Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Registration SUCCESSFUL!")
            print(f"   Access Token: {result.get('access_token', 'N/A')[:50]}...")
            print(f"   Token Type: {result.get('token_type', 'N/A')}")
            return True
        else:
            print(f"\n❌ Registration FAILED")
            try:
                error = response.json()
                print(f"   Error: {error}")
            except:
                print(f"   Raw Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Request FAILED with exception")
        print(f"   Error: {e}")
        return False

def main():
    print("=" * 60)
    print("REGISTRATION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n[Test 1] Checking backend health...")
    if not test_health():
        print("\n⚠️  Backend is not running!")
        print("   Please start the backend server first:")
        print("   cd backend && venv\\Scripts\\python -m uvicorn main:app --reload")
        return
    
    # Test 2: Registration
    print("\n[Test 2] Testing registration endpoint...")
    test_registration()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
