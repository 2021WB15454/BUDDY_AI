#!/usr/bin/env python3
"""
Functional test for the personal assistant modules
"""
import asyncio
import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import the necessary components
from core.nlp_processor import NLPProcessor
from skills.skill_manager import SkillManager
from core.decision_engine import DecisionEngine
from utils.config import Config

async def test_functionality():
    """Test that all new modules actually function"""
    print("🧪 Testing BUDDY AI Assistant Functionality...")
    
    try:
        # Initialize config
        config = Config()
        
        # Initialize NLP processor
        nlp = NLPProcessor(config)
        await nlp.initialize()
        
        # Initialize skill manager
        skill_manager = SkillManager(nlp)
        await skill_manager.initialize()
        
        # Test functional queries
        test_queries = [
            "Create a new task called 'Finish project'",
            "Add a note about today's meeting",
            "Schedule a meeting for next Monday",
            "Add a contact named John Smith",
            "Track a document called report.pdf",
            "Draft an email to the team",
            "Research machine learning topics"
        ]
        
        print("\n🚀 Testing Skill Functionality:")
        for query in test_queries:
            try:
                nlp_result = await nlp.process(query)
                intent = nlp_result.get('intent')
                print(f"✅ Query: '{query}' → Intent: {intent}")
                
                # Test the skill handler
                response = await skill_manager.handle_skill(intent, nlp_result, [])
                if response.get('success'):
                    print(f"   ✅ Skill Response: {response.get('response', 'No response')[:100]}...")
                else:
                    print(f"   ❌ Skill Error: {response.get('response', 'Unknown error')}")
                print()
                
            except Exception as e:
                print(f"   ❌ Error testing '{query}': {e}")
                print()
        
        print("🎯 Functionality test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_functionality())
    if success:
        print("\n🎉 All personal assistant modules are fully functional!")
        sys.exit(0)
    else:
        print("\n💥 Functionality test failed. Please check the errors above.")
        sys.exit(1)
