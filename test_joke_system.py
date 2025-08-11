#!/usr/bin/env python3
"""
Test joke functionality with the full BUDDY AI system
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.assistant import BuddyAssistant
from utils.config import Config

async def test_joke_system():
    """Test the joke functionality with the full BUDDY AI system"""
    
    print("🎭 Testing BUDDY AI Joke System (Full Integration)")
    print("=" * 60)
    
    # Initialize BUDDY AI
    try:
        config = Config()
        buddy = BuddyAssistant(config)
        await buddy.initialize()
        print("✅ BUDDY AI initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize BUDDY AI: {e}")
        return
    
    # Test joke queries
    joke_queries = [
        "tell me a joke",
        "I want to hear a joke",
        "make me laugh"
    ]
    
    print("\n🎪 Testing Joke Responses:")
    print("-" * 40)
    
    for i, query in enumerate(joke_queries, 1):
        try:
            print(f"\n{i}. Query: '{query}'")
            
            # Process through full BUDDY system
            result = await buddy.process_input(query)
            
            # Check response
            if result.get("success", False):
                response = result.get("response", "No response")
                print(f"   Response: {response}")
                print("   ✅ SUCCESS")
            else:
                print(f"   ❌ FAILED - {result}")
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Full system joke test complete!")

if __name__ == "__main__":
    asyncio.run(test_joke_system())
