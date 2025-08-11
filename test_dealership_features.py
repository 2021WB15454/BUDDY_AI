#!/usr/bin/env python3
"""
Test script for dealership and brand query features in BUDDY AI Automotive Module
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.automotive_skill import AutomotiveSkill

async def test_dealership_features():
    """Test dealership and brand query features"""
    
    print("🏢 Testing BUDDY AI Dealership & Brand Features")
    print("=" * 60)
    
    # Initialize components
    from utils.config import Config
    config = Config()
    nlp = NLPProcessor(config)
    automotive_skill = AutomotiveSkill(config)
    
    # Test dealership queries
    dealership_tests = [
        "Honda dealers in Chennai",
        "BMW showroom in Bangalore", 
        "Maruti service center in Mumbai",
        "Car dealerships in Delhi",
        "Service centers near me in Pune",
        "Hyundai showroom locations"
    ]
    
    # Test brand queries
    brand_tests = [
        "Tell me about Honda brand",
        "Maruti company information",
        "BMW brand details",
        "Hyundai manufacturer info",
        "Tata Motors company profile"
    ]
    
    print("🏢 Testing Dealership Queries:")
    print("-" * 40)
    
    for i, query in enumerate(dealership_tests, 1):
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            intent = nlp_result.get("intent", "unknown")
            
            print(f"{i}. Query: '{query}'")
            print(f"   Intent: {intent}")
            
            if intent == "automotive":
                # Get automotive response
                context = {"user_id": "test_user"}
                response = await automotive_skill.handle(nlp_result, context)
                print(f"   Response: {response[:100]}...")
                print("   ✅ SUCCESS")
            else:
                print(f"   ❌ FAILED - Wrong intent: {intent}")
            
            print()
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            print()
    
    print("🏭 Testing Brand Queries:")
    print("-" * 40)
    
    for i, query in enumerate(brand_tests, 1):
        try:
            # Process through NLP
            nlp_result = await nlp.process(query)
            intent = nlp_result.get("intent", "unknown")
            
            print(f"{i}. Query: '{query}'")
            print(f"   Intent: {intent}")
            
            if intent == "automotive":
                # Get automotive response
                context = {"user_id": "test_user"}
                response = await automotive_skill.handle(nlp_result, context)
                print(f"   Response: {response[:100]}...")
                print("   ✅ SUCCESS")
            else:
                print(f"   ❌ FAILED - Wrong intent: {intent}")
            
            print()
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            print()
    
    print("=" * 60)
    print("🎉 Dealership & Brand Feature Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_dealership_features())
