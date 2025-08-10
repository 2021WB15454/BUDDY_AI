#!/usr/bin/env python3
"""
Test the intent detection fix for time queries
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

async def test_intent_detection():
    """Test that time queries route correctly"""
    print("🧪 Testing intent detection for time queries...")
    
    try:
        from core.nlp_processor import NLPProcessor
        from utils.config import Config
        
        # Initialize NLP processor
        config = Config()
        nlp = NLPProcessor(config)
        await nlp.initialize()
        
        # Test time-related queries
        test_queries = [
            ("what is the time", "datetime"),
            ("what time is it", "datetime"),
            ("current time", "datetime"),
            ("show time", "datetime"),
            ("what's the time", "datetime"),
            ("schedule a meeting", "calendar"),
            ("my calendar", "calendar"),
            ("book appointment", "calendar"),
            ("what date is today", "datetime"),
            ("today's date", "datetime"),
            ("what day is it", "datetime")
        ]
        
        print("\n🔍 Testing Intent Detection:")
        all_correct = True
        
        for query, expected_intent in test_queries:
            nlp_result = await nlp.process(query)
            detected_intent = nlp_result.get('intent')
            
            if detected_intent == expected_intent:
                print(f"✅ '{query}' → {detected_intent}")
            else:
                print(f"❌ '{query}' → {detected_intent} (expected {expected_intent})")
                # Debug: check which keywords are matching
                if query == "my calendar":
                    from core.nlp_processor import NLPProcessor
                    print(f"   Debug: Full NLP result = {nlp_result}")
                all_correct = False
        
        if all_correct:
            print("\n🎉 All intent detections are correct!")
            return True
        else:
            print("\n⚠️ Some intent detections need fixing")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_intent_detection())
    if success:
        print("\n✅ Ready to deploy the fix!")
    else:
        print("\n💥 Please fix the issues above.")
        sys.exit(1)
