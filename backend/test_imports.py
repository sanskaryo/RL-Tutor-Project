#!/usr/bin/env python3
"""Test script to check API imports"""

try:
    from app.api import doubt_solver
    print("✅ doubt_solver import works")
except Exception as e:
    print(f"❌ doubt_solver import error: {e}")

try:
    from app.api import mindmap
    print("✅ mindmap import works")
except Exception as e:
    print(f"❌ mindmap import error: {e}")

try:
    from app.core.config import settings
    print("✅ config import works")
    print(f"GEMINI_API_KEY configured: {getattr(settings, 'GEMINI_API_KEY', None) is not None}")
except Exception as e:
    print(f"❌ config import error: {e}")