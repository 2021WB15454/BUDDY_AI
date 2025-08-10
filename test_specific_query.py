#!/usr/bin/env python3
"""Quick test for the specific query 'whoch language you are using'"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor

async def test_specific_query():
    """Test the specific query that failed"""
    
    # Initialize NLP processor with minimal config
    from utils.config import Config
    config = Config()
    nlp = NLPProcessor(config)
    
    # Test the specific query
    query = "whoch language you are using"
    print(f"🧪 Testing: '{query}'")
    
    result = await nlp.process(query)
    intent = result["intent"]
    
    print(f"Result: {intent}")
    
    if intent == "identity":
        print("✅ SUCCESS: Query correctly routed to identity skill")
    else:
        print(f"❌ FAILED: Query routed to '{intent}' instead of 'identity'")
        
    # Test a few more variations
    test_queries = [
        "whoch language you are using",
        "what language you using", 
        "which language you are using",
        "what programming language",
        "language you use",
        "what can you do for me",
        "what can u do",
        "what are your capabilities",
        "how can you help",
        "what do you do"
    ]
    
    print("\n🔍 Testing multiple language query variations:")
    for query in test_queries:
        result = await nlp.process(query)
        intent = result["intent"]
        status = "✅" if intent == "identity" else "❌"
        print(f"{status} '{query}' → {intent}")

if __name__ == "__main__":
    asyncio.run(test_specific_query())
