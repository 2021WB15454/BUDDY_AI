#!/usr/bin/env python3
"""
Test script for personal assistant modules
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills.personal_assistant_skill import PersonalAssistantSkill
from core.nlp_processor import NLPProcessor
from utils.config import Config

async def test_personal_assistant():
    """Test the personal assistant functionality"""
    
    # Initialize components
    config = Config()
    nlp_processor = NLPProcessor(config)
    personal_assistant_skill = PersonalAssistantSkill()
    
    test_queries = [
        "what is BITS",
        "Personal assistant",
        "tell me about personal assistant",
        "BITS Pilani information",
        "virtual assistant capabilities",
        "AI assistant features",
        "chatbot information",
        "how can personal assistant help"
    ]
    
    print("🧪 Testing Personal Assistant Integration\n")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing Query: '{query}'")
        print("-" * 40)
        
        try:
            # Test NLP processing
            nlp_result = await nlp_processor.process(query, {})
            intent = nlp_result.get('intent', 'unknown')
            print(f"🔍 Intent detected: {intent}")
            
            # Test personal assistant response if intent matches
            if intent == "personal_assistant":
                response = await personal_assistant_skill.handle_personal_assistant_query(query, {})
                
                # Show first few lines of response
                lines = response.split('\n')
                preview_lines = lines[:6]  # Show first 6 lines
                
                for line in preview_lines:
                    print(line)
                
                if len(lines) > 6:
                    print("... (response continues)")
            else:
                print(f"⚠️ Query routed to '{intent}' instead of 'personal_assistant'")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Personal assistant testing completed!")

if __name__ == "__main__":
    asyncio.run(test_personal_assistant())
