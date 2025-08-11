#!/usr/bin/env python3
"""
Final test to confirm joke functionality is working properly
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.assistant import BuddyAssistant
from utils.config import Config

async def final_joke_test():
    """Final test to confirm jokes are working"""
    
    print("🎭 Final Joke Test - Confirming Fix")
    print("=" * 50)
    
    # Initialize BUDDY AI
    config = Config()
    buddy = BuddyAssistant(config)
    await buddy.initialize()
    
    # Test multiple joke requests
    for i in range(5):
        print(f"\n{i+1}. Testing: 'tell me a joke'")
        result = await buddy.process_input("tell me a joke")
        
        if result.get("success", False):
            response = result.get("response", "")
            print(f"   Response: {response}")
            
            # Check if it's an actual joke (not the generic response)
            if "Here's another one for you!" in response:
                print("   ❌ STILL GETTING GENERIC RESPONSE")
            elif len(response) > 20:  # Actual jokes are longer
                print("   ✅ GOT ACTUAL JOKE")
            else:
                print("   ⚠️ SHORT RESPONSE")
        else:
            print(f"   ❌ FAILED - {result}")
    
    print("\n" + "=" * 50)
    print("🎉 Final joke test complete!")

if __name__ == "__main__":
    asyncio.run(final_joke_test())
