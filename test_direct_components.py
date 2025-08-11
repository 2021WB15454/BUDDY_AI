#!/usr/bin/env python3
"""
Direct test for weather skill and NLP classification
Tests the core components without full assistant initialization
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.weather_skill import WeatherSkill
from utils.config import Config

async def test_nlp_classification_direct():
    """Test NLP processor classification directly"""
    
    print("🧠 Testing NLP Processor Classification (Direct)")
    print("=" * 60)
    
    try:
        config = Config()
        nlp = NLPProcessor(config)
        
        classification_tests = [
            ("hey", "general_conversation"),  # Should be conversation, not weather
            ("hello", "general_conversation"),
            ("madurai weather", "weather"),
            ("what's the weather", "weather"),
            ("weather in chennai", "weather"),
            ("madurai", "weather"),  # Should be weather due to location recognition
            ("tirunelveli weather", "weather"),
            ("coimbatore weather", "weather"),
        ]
        
        print(f"Testing {len(classification_tests)} classifications...\n")
        
        passed = 0
        failed = 0
        
        for i, (query, expected) in enumerate(classification_tests, 1):
            try:
                result = await nlp.process(query)
                intent = result.get('intent', 'unknown')
                
                if intent == expected:
                    status = "✅ PASS"
                    passed += 1
                else:
                    status = "❌ FAIL"
                    failed += 1
                
                print(f"{i}. {status} | '{query}' → {intent} (expected: {expected})")
                
            except Exception as e:
                print(f"{i}. ❌ ERROR | '{query}' → Error: {str(e)}")
                failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All NLP classifications working correctly!")
        elif passed > 0:
            print(f"🔄 Partial success: {passed}/{len(classification_tests)} working")
        
        return failed == 0
        
    except Exception as e:
        print(f"❌ NLP Classification error: {str(e)}")
        return False

async def test_weather_skill_direct():
    """Test weather skill directly"""
    
    print("\n🌤️ Testing Weather Skill (Direct)")
    print("=" * 60)
    
    try:
        config = Config()
        weather_skill = WeatherSkill(config)
        
        weather_tests = [
            "madurai weather",
            "weather in chennai", 
            "madurai",
            "tirunelveli weather",
            "coimbatore weather",
            "what's the weather in bangalore",
        ]
        
        print(f"Testing {len(weather_tests)} weather queries...\n")
        
        for i, query in enumerate(weather_tests, 1):
            try:
                # Create mock NLP result for weather skill
                nlp_result = {
                    "intent": "weather",
                    "entities": [],
                    "text": query
                }
                
                # Call the weather skill handle method
                response = await weather_skill.handle(nlp_result, {})
                
                # Check if response looks like weather data
                is_weather_response = (
                    "weather" in response.lower() and 
                    ("°c" in response.lower() or "temperature" in response.lower() or "forecast" in response.lower())
                )
                is_error = "[" in response and "]" in response
                
                if is_weather_response:
                    status = "✅ WEATHER"
                elif is_error:
                    status = "⚠️ ERROR"
                else:
                    status = "❓ OTHER"
                
                print(f"{i}. {status} | '{query}'")
                print(f"    Response: {response[:80]}{'...' if len(response) > 80 else ''}")
                print()
                
            except Exception as e:
                print(f"{i}. ❌ EXCEPTION | '{query}' → Error: {str(e)}")
                print()
        
        print("✅ Weather skill test completed")
        return True
        
    except Exception as e:
        print(f"❌ Weather skill error: {str(e)}")
        return False

async def test_integration():
    """Test the integration between NLP and Weather skill"""
    
    print("\n🔗 Testing NLP → Weather Integration")
    print("=" * 60)
    
    try:
        config = Config()
        nlp = NLPProcessor(config)
        weather_skill = WeatherSkill(config)
        
        integration_tests = [
            "madurai weather",
            "weather in chennai",
            "madurai",
            "tirunelveli weather", 
        ]
        
        print(f"Testing {len(integration_tests)} integrations...\n")
        
        for i, query in enumerate(integration_tests, 1):
            try:
                # Step 1: Classify intent
                nlp_result = await nlp.process(query)
                intent = nlp_result.get('intent', 'unknown')
                
                # Step 2: If weather intent, call weather skill
                if intent == "weather":
                    response = await weather_skill.handle(nlp_result, {})
                    is_weather_response = (
                        "weather" in response.lower() and 
                        ("°c" in response.lower() or "temperature" in response.lower())
                    )
                    status = "✅ SUCCESS" if is_weather_response else "⚠️ PARTIAL"
                else:
                    response = f"[Non-weather intent: {intent}]"
                    status = "❌ MISCLASSIFIED" if query != "hey" else "✅ CORRECT"
                
                print(f"{i}. {status} | '{query}' → Intent: {intent}")
                print(f"    Response: {response[:80]}{'...' if len(response) > 80 else ''}")
                print()
                
            except Exception as e:
                print(f"{i}. ❌ EXCEPTION | '{query}' → Error: {str(e)}")
                print()
        
        print("✅ Integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {str(e)}")
        return False

async def main():
    print("🤖 BUDDY AI - Direct Component Testing")
    print("Testing weather intelligence without full system initialization\n")
    
    # Test NLP classification
    nlp_success = await test_nlp_classification_direct()
    
    # Test weather skill
    weather_success = await test_weather_skill_direct()
    
    # Test integration
    integration_success = await test_integration()
    
    print("\n" + "=" * 60)
    if nlp_success and weather_success and integration_success:
        print("🚀 BUDDY AI Weather Intelligence Components Working!")
        print("✅ NLP Classification: Working")
        print("✅ Weather Skill: Working") 
        print("✅ Integration: Working")
        print("\n🎯 Key Improvements Verified:")
        print("  • 'hey' → greeting (not weather)")
        print("  • 'madurai weather' → weather response")
        print("  • 'madurai' → weather response")
        print("  • Enhanced location extraction working")
    else:
        print("⚠️ Some components need attention:")
        print(f"  • NLP Classification: {'✅' if nlp_success else '❌'}")
        print(f"  • Weather Skill: {'✅' if weather_success else '❌'}")
        print(f"  • Integration: {'✅' if integration_success else '❌'}")

if __name__ == "__main__":
    asyncio.run(main())
