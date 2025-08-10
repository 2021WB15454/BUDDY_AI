#!/usr/bin/env python3
"""Test script to verify identity intent detection is working correctly"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor

async def test_identity_intent():
    """Test that identity queries route to identity skill, not datetime"""
    
    # Initialize NLP processor with minimal config
    from utils.config import Config
    config = Config()
    nlp = NLPProcessor(config)
    
    # Test cases that should route to identity skill
    identity_test_cases = [
        "whats your language",
        "what is your language", 
        "what language are you coded in",
        "what is the code used for creating you",
        "who created you",
        "what are you",
        "tell me about yourself",
        "who made you",
        "what programming language",
        "your code",
        "programming details",
        "who built you",
        "what is buddy"
    ]
    
    # Test cases that should route to datetime skill
    datetime_test_cases = [
        "what time is it",
        "current time",
        "what's the time",
        "show me the time",
        "time now"
    ]
    
    print("🧪 Testing identity intent detection fix...\n")
    
    print("🔍 Testing Identity Queries (should route to 'identity'):")
    all_correct = True
    
    for query in identity_test_cases:
        result = await nlp.process(query)
        intent = result["intent"]
        
        if intent == "identity":
            print(f"✅ '{query}' → {intent}")
        else:
            print(f"❌ '{query}' → {intent} (should be 'identity')")
            all_correct = False
    
    print("\n🔍 Testing DateTime Queries (should route to 'datetime'):")
    
    for query in datetime_test_cases:
        result = await nlp.process(query)
        intent = result["intent"]
        
        if intent == "datetime":
            print(f"✅ '{query}' → {intent}")
        else:
            print(f"❌ '{query}' → {intent} (should be 'datetime')")
            all_correct = False
    
    print(f"\n{'🎉 All intent detections are correct!' if all_correct else '⚠️ Some intent detections need fixing'}")
    print("✅ Ready to deploy the fix!" if all_correct else "❌ Please check the intent detection logic")

if __name__ == "__main__":
    asyncio.run(test_identity_intent())
