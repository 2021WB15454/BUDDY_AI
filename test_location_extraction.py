#!/usr/bin/env python3
"""
Test script for enhanced location extraction functionality
Tests various query formats to ensure the location extraction works properly
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.weather import extract_location
from utils.global_location_database import global_location_db

def test_location_extraction():
    """Test different query formats for location extraction"""
    
    print("🧪 Testing Enhanced Location Extraction")
    print("=" * 50)
    
    # Test cases with expected locations
    test_cases = [
        # Original format tests
        ("What's the weather in Chennai?", "Chennai"),
        ("Tell me weather for Madurai", "Madurai"),
        ("Weather in Bangalore", "Bangalore"),
        
        # New format tests - location + weather
        ("madurai weather", "Madurai"),
        ("chennai weather", "Chennai"),
        ("bangalore weather", "Bangalore"),
        ("tirunelveli weather", "Tirunelveli"),
        ("coimbatore weather", "Coimbatore"),
        
        # Single location tests
        ("madurai", "Madurai"),
        ("chennai", "Chennai"),
        ("bangalore", "Bangalore"),
        ("tirunelveli", "Tirunelveli"),
        ("coimbatore", "Coimbatore"),
        
        # Spelling correction tests
        ("maduri weather", "Madurai"),
        ("thirunelveli", "Tirunelveli"),
        ("maduri", "Madurai"),
        
        # Edge cases
        ("What's the weather like?", None),  # No location
        ("hey", None),  # Greeting
        ("weather", None),  # No specific location
    ]
    
    print(f"Testing {len(test_cases)} cases...\n")
    
    passed = 0
    failed = 0
    
    for i, (query, expected) in enumerate(test_cases, 1):
        try:
            result = extract_location(query)
            
            if result == expected:
                status = "✅ PASS"
                passed += 1
            else:
                status = "❌ FAIL"
                failed += 1
            
            print(f"{i:2d}. {status} | Query: '{query}'")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            print()
            
        except Exception as e:
            print(f"{i:2d}. ❌ ERROR | Query: '{query}'")
            print(f"    Error: {str(e)}")
            print()
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Location extraction is working perfectly.")
    else:
        print(f"⚠️ {failed} tests failed. Please review the implementation.")
    
    return failed == 0

def test_database_integration():
    """Test the global location database integration"""
    
    print("\n🗄️ Testing Global Location Database Integration")
    print("=" * 50)
    
    # Test database access
    try:
        all_locations = global_location_db.locations
        print(f"✅ Database loaded with {len(all_locations)} locations")
        
        # Test specific Tamil Nadu cities
        tamil_cities = ["Madurai", "Chennai", "Tirunelveli", "Coimbatore"]
        
        for city in tamil_cities:
            location_data = global_location_db.get_location_info(city)
            if location_data:
                coords = location_data.get('data', {}).get('coordinates', {})
                lat = coords.get('lat', 'N/A')
                lon = coords.get('lon', 'N/A')
                print(f"✅ {city}: lat={lat}, lon={lon}")
            else:
                print(f"❌ {city}: Not found in database")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 BUDDY AI - Location Extraction Test Suite")
    print("Testing enhanced location extraction capabilities\n")
    
    # Test location extraction
    extraction_success = test_location_extraction()
    
    # Test database integration
    database_success = test_database_integration()
    
    print("\n" + "=" * 50)
    if extraction_success and database_success:
        print("🚀 All systems operational! Location extraction is ready.")
    else:
        print("⚠️ Some issues detected. Please review the results above.")
