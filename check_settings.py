from app.core.config import settings

def check_api_key():
    try:
        api_key = settings.GEMINI_API_KEY
        if api_key:
            print(f"✅ GEMINI_API_KEY found: {api_key[:5]}...{api_key[-4:]}")
        else:
            print("❌ GEMINI_API_KEY not set")
    except Exception as e:
        print(f"❌ Error accessing settings: {e}")

if __name__ == "__main__":
    check_api_key()