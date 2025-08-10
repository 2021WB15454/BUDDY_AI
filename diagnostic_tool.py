#!/usr/bin/env python3
"""
Diagnostic tool to help debug intent routing issues on hosted platforms.
This can be used to check if the latest code changes are active.
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor

async def diagnostic_check():
    """Run diagnostic checks for intent detection"""
    
    print("🔧 BUDDY AI Diagnostic Tool")
    print("=" * 50)
    
    try:
        # Initialize NLP processor with minimal config
        from utils.config import Config
        config = Config()
        nlp = NLPProcessor(config)
        
        print("✅ NLP Processor initialized successfully")
        
        # Test critical identity queries
        critical_tests = [
            ("whoch language you are using", "identity"),
            ("what is your language", "identity"),
            ("who created you", "identity"),
            ("what are you", "identity"),
            ("what time is it", "datetime"),
            ("current time", "datetime"),
            ("hello", "general_conversation"),
            ("weather today", "weather")
        ]
        
        print("\n🧪 Testing Critical Intent Detection:")
        print("-" * 40)
        
        all_passed = True
        
        for query, expected_intent in critical_tests:
            result = await nlp.process(query)
            actual_intent = result["intent"]
            
            if actual_intent == expected_intent:
                print(f"✅ '{query}' → {actual_intent}")
            else:
                print(f"❌ '{query}' → {actual_intent} (expected: {expected_intent})")
                all_passed = False
        
        print(f"\n{'🎉 All tests passed!' if all_passed else '⚠️ Some tests failed'}")
        
        # Check for latest code deployment indicators
        print("\n🔍 Code Deployment Check:")
        print("-" * 30)
        
        # Check if latest identity keywords are present by reading the source file
        try:
            with open("core/nlp_processor.py", "r", encoding="utf-8") as f:
                source_code = f.read()
                
            if "whoch language" in source_code:
                print("✅ Latest identity keywords detected (includes 'whoch language')")
            else:
                print("❌ Latest identity keywords NOT detected - code may not be deployed")
                
            if "identity first (highest priority)" in source_code:
                print("✅ Latest intent priority logic detected")
            else:
                print("❌ Latest intent priority logic NOT detected")
        except Exception as e:
            print(f"⚠️ Could not verify source code: {e}")
            
        # Version info
        import datetime
        print(f"\n📅 Diagnostic run at: {datetime.datetime.now()}")
        print("💡 If hosted site still has issues, the platform may need time to deploy changes")
        
    except Exception as e:
        print(f"❌ Error during diagnostic: {e}")

if __name__ == "__main__":
    asyncio.run(diagnostic_check())
