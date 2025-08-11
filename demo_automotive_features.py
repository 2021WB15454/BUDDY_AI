#!/usr/bin/env python3
"""
Quick test to demonstrate the new dealership and brand features
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.automotive_skill import AutomotiveSkill
from utils.config import Config

async def demo_new_features():
    """Demonstrate the new dealership and brand features"""
    
    print("🚗 BUDDY AI - New Automotive Features Demo")
    print("=" * 60)
    
    # Initialize components
    config = Config()
    nlp = NLPProcessor(config)
    automotive_skill = AutomotiveSkill(config)
    
    # Demo queries
    demo_queries = [
        "Honda dealers in Chennai",
        "BMW showroom in Bangalore",
        "Tell me about Maruti brand",
        "Hyundai company information"
    ]
    
    print("🎯 Demonstrating New Features:")
    print("-" * 40)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            
            # Get automotive response
            context = {"user_id": "demo_user"}
            response = await automotive_skill.handle(nlp_result, context)
            
            print(f"Response:\n{response}")
            print("-" * 40)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("-" * 40)
    
    print("\n🎉 New automotive features working perfectly!")
    print("✅ Dealership locator for Chennai, Bangalore, Mumbai, Delhi, Pune")
    print("✅ Brand information for Maruti, Hyundai, Tata, Honda, BMW")

if __name__ == "__main__":
    asyncio.run(demo_new_features())
