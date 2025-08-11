#!/usr/bin/env python3
"""
Test joke functionality to debug the hosted server issue
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.skill_manager import SkillManager
from utils.config import Config

async def test_joke_functionality():
    """Test the joke functionality end-to-end"""
    
    print("🎭 Testing BUDDY AI Joke Functionality")
    print("=" * 50)
    
    # Initialize components
    config = Config()
    nlp = NLPProcessor(config)
    skill_manager = SkillManager(config)
    
    # Test queries
    joke_queries = [
        "tell me a joke",
        "Tell me a joke",
        "joke",
        "make me laugh",
        "funny joke",
        "I want to hear a joke"
    ]
    
    print("🧠 Testing NLP Classification:")
    print("-" * 30)
    
    for i, query in enumerate(joke_queries, 1):
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            intent = nlp_result.get("intent", "unknown")
            
            print(f"{i}. Query: '{query}'")
            print(f"   Intent: {intent}")
            
            if intent == "joke":
                print("   ✅ CORRECT INTENT")
            else:
                print(f"   ❌ WRONG INTENT - Expected: joke, Got: {intent}")
            
            print()
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            print()
    
    print("🎪 Testing Skill Response:")
    print("-" * 30)
    
    for i, query in enumerate(joke_queries[:3], 1):  # Test first 3
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            
            # Get skill response
            context = {"user_id": "test_user"}
            intent = nlp_result.get("intent", "unknown")
            response = await skill_manager.handle_skill(intent, nlp_result, context)
            
            print(f"{i}. Query: '{query}'")
            print(f"   Response: {response}")
            print()
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            print()
    
    print("=" * 50)
    print("🎉 Joke functionality test complete!")

if __name__ == "__main__":
    asyncio.run(test_joke_functionality())
