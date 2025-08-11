#!/usr/bin/env python3
"""
Weather Intelligence Diagnostic Tool
Specific testing for weather query handling
"""

import requests
import json
import time
from datetime import datetime

def test_weather_intelligence():
    """Test weather handling specifically"""
    
    base_url = "https://buddy-ai-0t6c.onrender.com"
    
    print("🌤️ WEATHER INTELLIGENCE DIAGNOSTIC")
    print("=" * 50)
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing URL: {base_url}")
    print()
    
    # Weather test cases
    weather_tests = [
        "What's the weather?",
        "weather",
        "weather today",
        "how's the weather",
        "weather forecast",
        "weather in chennai",
        "weather in london",
        "weather in madurai",
        "temperature",
        "is it raining"
    ]
    
    results = []
    
    for i, query in enumerate(weather_tests, 1):
        print(f"🌡️ Test {i}: '{query}'")
        
        try:
            response = requests.post(
                f"{base_url}/api/ask",
                json={"message": query},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Check if it's a proper weather response
                weather_indicators = [
                    "location", "weather", "temperature", "forecast", 
                    "specify", "chennai", "london", "tokyo", "city"
                ]
                
                has_weather_response = any(word in response_text.lower() for word in weather_indicators)
                
                # Check for wrong responses
                wrong_responses = [
                    "goodbye", "see you", "farewell", "bye", "later",
                    "hello", "hi there", "greetings", "hey"
                ]
                
                has_wrong_response = any(word in response_text.lower() for word in wrong_responses)
                
                if has_weather_response and not has_wrong_response:
                    status = "✅ CORRECT"
                elif has_wrong_response:
                    status = "❌ WRONG TYPE"
                else:
                    status = "❓ UNCLEAR"
                
                print(f"   {status} - Response: {response_text[:150]}...")
                results.append({
                    "query": query,
                    "response": response_text,
                    "correct": has_weather_response and not has_wrong_response
                })
                
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({"query": query, "error": f"HTTP {response.status_code}", "correct": False})
                
        except Exception as e:
            print(f"   ❌ Connection Error: {str(e)}")
            results.append({"query": query, "error": str(e), "correct": False})
        
        print()
        time.sleep(1)
    
    # Summary
    correct = sum(1 for r in results if r.get("correct", False))
    total = len(results)
    
    print("📊 WEATHER DIAGNOSTIC SUMMARY")
    print("=" * 50)
    print(f"✅ Correct Weather Responses: {correct}/{total}")
    print(f"❌ Incorrect Responses: {total - correct}/{total}")
    
    if correct < total:
        print("\n🔧 ISSUES DETECTED:")
        for result in results:
            if not result.get("correct", False) and "response" in result:
                print(f"❌ '{result['query']}' → '{result['response'][:100]}...'")
    
    return results

if __name__ == "__main__":
    test_weather_intelligence()
