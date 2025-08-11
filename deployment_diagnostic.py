#!/usr/bin/env python3
"""
BUDDY AI Deployment Diagnostic Tool
Quick verification that conversation handling is working
"""

import requests
import json
import time
from datetime import datetime

def test_conversation_intelligence():
    """Test the conversation handling on hosted version"""
    
    # Your Render URL
    base_url = "https://buddy-ai-0t6c.onrender.com"
    
    print("🔍 BUDDY AI DEPLOYMENT DIAGNOSTIC")
    print("=" * 50)
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing URL: {base_url}")
    print()
    
    # Test cases for conversation intelligence
    test_cases = [
        {
            "input": "hey",
            "expected_type": "conversation",
            "should_not_contain": ["specify a location", "London", "chennai", "Tokyo"]
        },
        {
            "input": "hello",
            "expected_type": "conversation", 
            "should_not_contain": ["specify a location", "weather"]
        },
        {
            "input": "hi there",
            "expected_type": "conversation",
            "should_not_contain": ["specify a location", "weather"]
        },
        {
            "input": "weather in chennai",
            "expected_type": "weather",
            "should_contain": ["chennai", "weather", "temperature"]
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: '{test['input']}'")
        
        try:
            # Send request to hosted version
            response = requests.post(
                f"{base_url}/api/ask",
                json={"message": test["input"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").lower()
                
                # Check if response is correct type
                is_conversation = not any(word in response_text for word in test.get("should_not_contain", []))
                
                if test["expected_type"] == "conversation":
                    success = is_conversation
                    status = "✅ PASS" if success else "❌ FAIL"
                else:
                    success = any(word in response_text for word in test.get("should_contain", []))
                    status = "✅ PASS" if success else "❌ FAIL"
                
                print(f"   {status} - Response: {data.get('response', 'No response')[:100]}...")
                results.append({"test": test["input"], "success": success, "response": data.get("response", "")})
                
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({"test": test["input"], "success": False, "error": f"HTTP {response.status_code}"})
                
        except Exception as e:
            print(f"   ❌ Connection Error: {str(e)}")
            results.append({"test": test["input"], "success": False, "error": str(e)})
        
        print()
        time.sleep(1)  # Rate limiting
    
    # Summary
    passed = sum(1 for r in results if r.get("success", False))
    total = len(results)
    
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Conversation intelligence is working!")
    else:
        print("🚨 DEPLOYMENT ISSUE DETECTED - Conversation handling needs attention")
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Wait 5-10 minutes for Render deployment to complete")
        print("2. Check Render dashboard for deployment status")
        print("3. Clear browser cache and test again")
        print("4. Check Render logs for any errors")
    
    return results

if __name__ == "__main__":
    test_conversation_intelligence()
