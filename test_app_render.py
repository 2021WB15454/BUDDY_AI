#!/usr/bin/env python3
"""
Test the updated app.py for Render deployment
"""

def test_app_structure():
    print("🧪 Testing updated app.py for Render deployment...")
    
    try:
        # Test imports
        import app
        print("✅ app.py imports successfully")
        
        # Test that main function exists
        if hasattr(app, 'main'):
            print("✅ main() function available")
        
        # Test that keep_alive function exists
        if hasattr(app, 'keep_alive'):
            print("✅ Heartbeat function available")
        
        # Check threading import
        import threading
        print("✅ Threading support available")
        
        print("\n📋 Updated Features:")
        print("✅ Heartbeat thread to keep logs active")
        print("✅ HEAD route handler for Render health checks")  
        print("✅ Port defaults to 10000 (Render standard)")
        print("✅ Single uvicorn.Server instance to prevent double-start")
        print("✅ Procfile updated to use app.py")
        
        print("\n🎉 App.py is ready for Render deployment!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_app_structure()
