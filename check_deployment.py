#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if the hosted BUDDY AI server has the latest changes
"""

import requests
import json
from datetime import datetime

def check_deployment():
    """Check if the latest changes are deployed"""
    try:
        print("🔍 Checking deployment status...")
        
        # Test the hosted server
        url = "https://buddy-ai-0t6c.onrender.com/api/ask"
        
        # Test weather query to see if intent routing is fixed
        payload = {
            "message": "what's the weather?",
            "context": {}
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is responding")
            print(f"📝 Response: {data.get('response', 'No response')[:100]}...")
            
            # Check if it's going to weather skill (not datetime)
            if 'weather' in data.get('response', '').lower() and 'date' not in data.get('response', '').lower():
                print("✅ Intent routing appears to be working correctly")
            else:
                print("⚠️ Intent routing may still have issues")
                
        else:
            print(f"❌ Server error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def check_ui():
    """Check if the new UI is deployed"""
    try:
        print("\n🎨 Checking UI deployment...")
        
        response = requests.get("https://buddy-ai-0t6c.onrender.com", timeout=30)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Check for new UI elements
            if 'responsive.css' in html_content:
                print("✅ Responsive CSS is loaded")
            else:
                print("❌ Responsive CSS not found")
                
            if 'manifest.json' in html_content:
                print("✅ PWA manifest is loaded")
            else:
                print("❌ PWA manifest not found")
                
            if 'service-worker' in html_content or 'sw.js' in html_content:
                print("✅ Service Worker is loaded")
            else:
                print("❌ Service Worker not found")
                
        else:
            print(f"❌ UI check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ UI check error: {e}")

if __name__ == "__main__":
    print(f"🕐 Deployment Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    check_deployment()
    check_ui()
    
    print("\n" + "=" * 50)
    print("💡 If issues persist, try manual redeploy in Render dashboard")
