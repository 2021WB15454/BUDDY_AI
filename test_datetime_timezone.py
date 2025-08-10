#!/usr/bin/env python3
"""
Test timezone functionality for datetime skill
"""
import asyncio
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

async def test_datetime_timezone():
    """Test that datetime skill uses correct timezone"""
    print("🧪 Testing DateTime Timezone Functionality...")
    
    try:
        # Test with different timezone settings
        os.environ['TIMEZONE'] = 'Asia/Kolkata'  # Indian timezone
        
        from skills.datetime_skill import DateTimeSkill
        
        # Initialize datetime skill
        skill = DateTimeSkill()
        print(f"✅ DateTimeSkill initialized with timezone: {skill.default_timezone}")
        
        # Test time query
        response = await skill.handle_datetime_query("what is the time", {})
        print(f"\n🕐 Time Query Response:")
        print(response)
        
        # Test with different timezone
        print(f"\n🌍 Testing timezone conversion...")
        current_time = skill._get_current_datetime()
        print(f"Current time object: {current_time}")
        print(f"Timezone: {current_time.tzinfo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Timezone test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_datetime_timezone())
    if success:
        print("\n🎉 Timezone functionality working correctly!")
    else:
        print("\n💥 Timezone test failed.")
        sys.exit(1)
