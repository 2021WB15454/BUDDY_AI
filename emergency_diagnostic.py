#!/usr/bin/env python3
"""
Emergency diagnostic script to test hosted server responses
"""

import requests
import json
import time

def test_hosted_server():
    """Test specific functionality on hosted server"""
    
    print("🚨 EMERGENCY DIAGNOSTIC - BUDDY AI Server Issues")
    print("=" * 60)
    
    base_url = "https://buddy-ai-0t6c.onrender.com"
    
    # Test cases that should work
    test_cases = [
        {
            "query": "Give me an inspirational quote",
            "expected_intent": "quote",
            "description": "Quote request test"
        },
        {
            "query": "Tell me a joke", 
            "expected_intent": "joke",
            "description": "Joke request test"
        },
        {
            "query": "What can you do?",
            "expected_intent": "identity", 
            "description": "Identity/capabilities test"
        },
        {
            "query": "Honda City price",
            "expected_intent": "automotive",
            "description": "Automotive query test"
        }
    ]
    
    print(f"🌐 Testing server: {base_url}")
    print(f"⏰ Test time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for i, test in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: {test['description']}")
        print(f"   Query: '{test['query']}'")
        
        try:
            # Test the correct endpoint
            response = requests.post(
                f"{base_url}/api/ask",
                json={"message": test['query']},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', 'No reply')
                
                print(f"   Status: ✅ {response.status_code}")
                print(f"   Response: {reply[:100]}...")
                
                # Check if response makes sense
                query_lower = test['query'].lower()
                reply_lower = reply.lower()
                
                if test['expected_intent'] == 'quote' and ('quote' in reply_lower or 'inspiration' in reply_lower):
                    print(f"   Result: ✅ WORKING - Quote detected")
                elif test['expected_intent'] == 'joke' and ('joke' in reply_lower or any(word in reply_lower for word in ['funny', 'laugh', 'humor'])):
                    print(f"   Result: ✅ WORKING - Joke detected")
                elif test['expected_intent'] == 'identity' and ('buddy' in reply_lower or 'assistant' in reply_lower or 'help' in reply_lower):
                    print(f"   Result: ✅ WORKING - Identity response")
                elif test['expected_intent'] == 'automotive' and ('car' in reply_lower or 'honda' in reply_lower or 'price' in reply_lower):
                    print(f"   Result: ✅ WORKING - Automotive response")
                else:
                    print(f"   Result: ❌ BROKEN - Unexpected response")
                    print(f"           Expected: {test['expected_intent']} related response")
                    
            else:
                print(f"   Status: ❌ {response.status_code}")
                print(f"   Error: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print(f"   Status: ❌ TIMEOUT (>30s)")
        except Exception as e:
            print(f"   Status: ❌ ERROR - {str(e)}")
            
        print()
    
    print("🔍 DIAGNOSIS COMPLETE")
    print("=" * 30)
    print("If most tests are failing, the server likely needs:")
    print("1. 🔄 Manual redeploy from Render dashboard")
    print("2. 📦 Check if latest code is actually deployed")
    print("3. 🐛 Check Render logs for runtime errors")
    print("4. ⚙️ Verify environment variables are set correctly")

if __name__ == "__main__":
    test_hosted_server()
