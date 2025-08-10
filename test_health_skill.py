#!/usr/bin/env python3
"""
Test script for the enhanced health skill
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills.health_skill import HealthSkill

async def test_health_skill():
    """Test the health skill with various queries"""
    
    health_skill = HealthSkill()
    
    test_queries = [
        "What is dengue?",
        "symptoms of dengue",
        "dengue fever information",
        "what are the symptoms of malaria?",
        "diabetes information",
        "high blood pressure symptoms",
        "I have a headache",
        "what causes fever?",
        "general health question"
    ]
    
    print("🧪 Testing Enhanced Health Skill\n")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing Query: '{query}'")
        print("-" * 40)
        
        try:
            response = await health_skill.handle_health_query(query, {})
            
            # Show first few lines of response
            lines = response.split('\n')
            preview_lines = lines[:8]  # Show first 8 lines
            
            for line in preview_lines:
                print(line)
            
            if len(lines) > 8:
                print("... (response continues)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Health skill testing completed!")

if __name__ == "__main__":
    asyncio.run(test_health_skill())
