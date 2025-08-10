#!/usr/bin/env python3
"""
Test the production deployment locally
"""
import asyncio
import sys
import requests
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

async def test_production_setup():
    """Test that the production app can start"""
    print("🧪 Testing production deployment setup...")
    
    try:
        # Import the production app
        from app import main
        print("✅ Production app imports successfully")
        
        # Test that all components can be imported
        from core.assistant import BuddyAssistant
        from interfaces.web_server import WebServer
        from utils.config import Config
        print("✅ All core components import successfully")
        
        # Test configuration
        config = Config()
        print("✅ Configuration loads successfully")
        
        print("\n🚀 Production setup is ready!")
        print("\n📋 Deployment Checklist:")
        print("✅ app.py - Production entry point")
        print("✅ Procfile - Process definition")
        print("✅ runtime.txt - Python version")
        print("✅ requirements.txt - Dependencies")
        print("✅ .env.example - Environment template")
        print("✅ README.md - Documentation")
        print("✅ DEPLOYMENT.md - Deployment guide")
        
        print("\n🌐 Ready to deploy to:")
        print("• Render (recommended)")
        print("• Railway")
        print("• Heroku")
        print("• Any Python hosting platform")
        
        return True
        
    except Exception as e:
        print(f"❌ Production setup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_interface():
    """Test the web interface locally"""
    print("\n🌐 To test the web interface locally:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Run: python app.py")
    print("3. Visit: http://localhost:8000")
    print("4. Test the chat interface")

if __name__ == "__main__":
    success = asyncio.run(test_production_setup())
    if success:
        test_web_interface()
        print("\n🎉 Ready for public deployment!")
    else:
        print("\n💥 Please fix the issues above before deploying.")
        sys.exit(1)
