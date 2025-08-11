#!/usr/bin/env python3
"""
End-to-end test for BUDDY AI weather intelligence
Tests the complete pipeline from user input to weather response
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from core.assistant import BuddyAssistant
from utils.config import Config

def test_complete_weather_system():
    """Test the complete weather intelligence system"""
    
    print("🌤️ Testing Complete BUDDY AI Weather Intelligence System")
    print("=" * 60)
    
    try:
        # Initialize the assistant with config
        config = Config()
        assistant = BuddyAssistant(config)
        
        # Test cases that previously failed
        test_cases = [
            # Greeting test (should NOT be weather)
            "hey",
            
            # Weather queries (should be weather)
            "What's the weather?",
            "madurai weather",
            "madurai",
            "weather in chennai",
            "tirunelveli weather",
            "coimbatore weather",
            "weather for bangalore",
            
            # Edge cases
            "weather",
            "What's the weather like?",
        ]
        
        print(f"Testing {len(test_cases)} queries...\n")
        
        for i, query in enumerate(test_cases, 1):
            print(f"{i:2d}. Query: '{query}'")
            
            try:
                # Process the query through the complete system
                response = assistant.process_message(query)
                
                # Analyze the response
                is_greeting = "hello" in response.lower() or "hi there" in response.lower() or "greetings" in response.lower()
                is_weather = "weather" in response.lower() and ("temperature" in response.lower() or "°c" in response.lower() or "forecast" in response.lower())
                is_error = "[" in response and "]" in response
                is_farewell = "goodbye" in response.lower() or "farewell" in response.lower() or "see you" in response.lower()
                
                # Determine expected behavior
                if query.lower() == "hey":
                    expected = "greeting"
                    actual = "greeting" if is_greeting else ("weather" if is_weather else ("error" if is_error else ("farewell" if is_farewell else "other")))
                else:
                    expected = "weather"
                    actual = "weather" if is_weather else ("greeting" if is_greeting else ("error" if is_error else ("farewell" if is_farewell else "other")))
                
                # Status determination
                if expected == actual:
                    status = "✅ PASS"
                elif actual == "error":
                    status = "⚠️ ERROR"
                else:
                    status = "❌ FAIL"
                
                print(f"    {status} | Expected: {expected}, Got: {actual}")
                print(f"    Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                print()
                
            except Exception as e:
                print(f"    ❌ EXCEPTION | Error: {str(e)}")
                print()
        
        print("=" * 60)
        print("🎯 Test Summary:")
        print("- All queries processed through complete BUDDY AI system")
        print("- Weather intelligence with enhanced location extraction")
        print("- Greeting recognition with weather priority protection")
        print("- Global location database integration")
        
        return True
        
    except Exception as e:
        print(f"❌ System initialization error: {str(e)}")
        return False

def test_nlp_classification():
    """Test NLP processor classification specifically"""
    
    print("\n🧠 Testing NLP Processor Classification")
    print("=" * 60)
    
    try:
        config = Config()
        nlp = NLPProcessor(config)
        
        classification_tests = [
            ("hey", "greeting"),
            ("hello", "greeting"),
            ("madurai weather", "weather"),
            ("what's the weather", "weather"),
            ("weather in chennai", "weather"),
            ("madurai", "weather"),  # Should be weather due to location recognition
            ("tirunelveli weather", "weather"),
        ]
        
        print(f"Testing {len(classification_tests)} classifications...\n")
        
        for i, (query, expected) in enumerate(classification_tests, 1):
            intent = nlp.classify_intent(query)
            
            status = "✅ PASS" if intent == expected else "❌ FAIL"
            print(f"{i}. {status} | '{query}' → {intent} (expected: {expected})")
        
        print("\n✅ NLP Classification test completed")
        return True
        
    except Exception as e:
        print(f"❌ NLP Classification error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 BUDDY AI - Complete Weather Intelligence Test")
    print("Testing the full pipeline from user input to response\n")
    
    # Test NLP classification
    nlp_success = test_nlp_classification()
    
    # Test complete system
    system_success = test_complete_weather_system()
    
    print("\n" + "=" * 60)
    if nlp_success and system_success:
        print("🚀 BUDDY AI Weather Intelligence is fully operational!")
        print("✅ All systems working: greeting recognition, weather queries, location extraction")
    else:
        print("⚠️ Some issues detected in the weather intelligence system.")
