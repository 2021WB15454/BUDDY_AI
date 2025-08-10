#!/usr/bin/env python3
"""
Simple test for datetime timezone
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# Set timezone
os.environ['TIMEZONE'] = 'Asia/Kolkata'

try:
    from skills.datetime_skill import DateTimeSkill
    
    print("🧪 Testing DateTime Timezone...")
    skill = DateTimeSkill()
    print(f"✅ Timezone: {skill.default_timezone}")
    
    current_time = skill._get_current_datetime()
    print(f"✅ Current time: {current_time}")
    print(f"✅ Timezone info: {current_time.tzinfo}")
    
    print("🎉 Timezone test successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
