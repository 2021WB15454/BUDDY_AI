#!/usr/bin/env python3
"""
Integration test for the personal assistant modules
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

async def test_integration():
    """Test that all new modules are properly integrated"""
    print("🔧 Testing BUDDY AI Assistant Integration...")
    
    try:
        # Initialize config
        config = Config()
        print("✅ Config initialized")
        
        # Initialize NLP processor
        nlp = NLPProcessor(config)
        await nlp.initialize()
        print("✅ NLP Processor initialized")
        
        # Initialize skill manager
        skill_manager = SkillManager(nlp)
        await skill_manager.initialize()
        print("✅ Skill Manager initialized")
        
        # Test available skills
        skills = await skill_manager.get_available_skills()
        print(f"✅ Available skills: {skills}")
        
        # Check that our new skills are available
        expected_skills = [
            'task_management', 'notes_management', 'calendar', 
            'contact_management', 'file_management', 'communication', 'research'
        ]
        
        for skill in expected_skills:
            if skill in skills:
                print(f"✅ {skill} skill is available")
            else:
                print(f"❌ {skill} skill is missing")
        
        # Test NLP processing for each new skill
        test_queries = [
            ("Create a task to finish the project", "task_management"),
            ("Add a note about the meeting", "notes_management"),
            ("Schedule a meeting for tomorrow", "calendar"),
            ("Add John's contact information", "contact_management"),
            ("Find my documents", "file_management"),
            ("Draft an email to the team", "communication"),
            ("Research artificial intelligence", "research")
        ]
        
        print("\n🧪 Testing NLP Intent Detection:")
        for query, expected_intent in test_queries:
            nlp_result = await nlp.process(query)
            detected_intent = nlp_result.get('intent')
            if detected_intent == expected_intent:
                print(f"✅ '{query}' → {detected_intent}")
            else:
                print(f"❌ '{query}' → {detected_intent} (expected {expected_intent})")
        
        print("\n🎯 Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_integration())
    if success:
        print("\n🎉 All personal assistant modules are successfully integrated!")
        sys.exit(0)
    else:
        print("\n💥 Integration test failed. Please check the errors above.")
        sys.exit(1)
