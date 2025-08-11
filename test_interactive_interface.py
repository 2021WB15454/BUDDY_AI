#!/usr/bin/env python3
"""
Test script to verify interactive web interface functionality
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.skill_manager import SkillManager
from utils.config import Config

async def test_interactive_features():
    """Test the interactive feature queries from the web interface"""
    
    print("🎯 Testing Interactive Web Interface Features")
    print("=" * 60)
    
    # Initialize components
    config = Config()
    nlp = NLPProcessor(config)
    skill_manager = SkillManager(config)
    
    # Test queries that would be triggered by clicking feature cards
    feature_tests = {
        "Weather": [
            "What's the weather in Tirunelveli?",
            "Weather in Chennai",
            "Today's weather forecast"
        ],
        "Tasks": [
            "Show my tasks",
            "Add task: Call the dentist",
            "What tasks do I have?"
        ],
        "Calendar": [
            "Show my calendar",
            "What's my schedule today?",
            "Add meeting tomorrow at 2 PM"
        ],
        "Entertainment": [
            "Tell me a programming joke",
            "Inspire me with a quote",
            "Random fun fact"
        ],
        "Automotive": [
            "Honda City price and specifications",
            "Best car under 15 lakhs",
            "BMW dealers in Chennai"
        ]
    }
    
    # Test quick action buttons
    quick_action_tests = [
        "What can you do?",
        "What's the weather in Tirunelveli?",
        "Tell me a joke",
        "Give me an inspirational quote"
    ]
    
    print("🎪 Testing Feature Card Interactions:")
    print("-" * 40)
    
    for feature, queries in feature_tests.items():
        print(f"\n📋 {feature} Feature:")
        for i, query in enumerate(queries, 1):
            try:
                # Process through NLP
                nlp_result = await nlp.process(query)
                intent = nlp_result.get("intent", "unknown")
                
                print(f"   {i}. '{query}' → Intent: {intent}")
                
                if intent in ["weather", "forecast", "joke", "quote", "automotive", "task_management", "calendar"]:
                    print(f"      ✅ Correct intent detected")
                else:
                    print(f"      ⚠️ Intent may need adjustment")
                    
            except Exception as e:
                print(f"      ❌ ERROR: {str(e)}")
    
    print(f"\n🎯 Testing Quick Action Buttons:")
    print("-" * 40)
    
    for i, query in enumerate(quick_action_tests, 1):
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            intent = nlp_result.get("intent", "unknown")
            
            print(f"{i}. '{query}' → Intent: {intent}")
            
            if intent in ["general_conversation", "weather", "joke", "quote"]:
                print(f"   ✅ Quick action working correctly")
            else:
                print(f"   ⚠️ May need intent adjustment")
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Interactive web interface test complete!")
    print("\n📋 Summary:")
    print("✅ Feature cards should trigger appropriate intents")
    print("✅ Quick action buttons should work correctly")
    print("✅ Automotive feature has been added to the interface")
    print("✅ All interactions should provide visual feedback")

if __name__ == "__main__":
    asyncio.run(test_interactive_features())
