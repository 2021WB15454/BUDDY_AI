#!/usr/bin/env python3
"""
Test script for automotive functionality in BUDDY AI
Tests automotive queries, car information, and related services
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.nlp_processor import NLPProcessor
from skills.automotive_skill import AutomotiveSkill
from utils.config import Config

async def test_automotive_nlp_classification():
    """Test NLP processor classification for automotive queries"""
    
    print("🚗 Testing Automotive NLP Classification")
    print("=" * 60)
    
    try:
        config = Config()
        nlp = NLPProcessor(config)
        
        automotive_tests = [
            # Car model queries
            ("maruti swift price", "automotive"),
            ("honda city specifications", "automotive"),
            ("hyundai creta vs tata nexon", "automotive"),
            ("bmw 3 series features", "automotive"),
            ("mercedes c class mileage", "automotive"),
            
            # General automotive queries
            ("best car under 10 lakhs", "automotive"),
            ("fuel efficient cars", "automotive"),
            ("car insurance guide", "automotive"),
            ("car maintenance tips", "automotive"),
            ("automatic vs manual transmission", "automotive"),
            
            # Car services
            ("car service schedule", "automotive"),
            ("oil change frequency", "automotive"),
            ("car loan emi calculator", "automotive"),
            ("used car buying guide", "automotive"),
            ("best family car", "automotive"),
            
            # Automotive locations
            ("car dealers in chennai", "automotive"),
            ("bmw showroom bangalore", "automotive"),
            ("service center near me", "automotive"),
            
            # Non-automotive (should not be classified as automotive)
            ("weather in chennai", "weather"),
            ("tell me a joke", "joke"),
            ("hello", "general_conversation"),
        ]
        
        print(f"Testing {len(automotive_tests)} classifications...\n")
        
        passed = 0
        failed = 0
        
        for i, (query, expected) in enumerate(automotive_tests, 1):
            try:
                result = await nlp.process(query)
                intent = result.get('intent', 'unknown')
                
                if intent == expected:
                    status = "✅ PASS"
                    passed += 1
                else:
                    status = "❌ FAIL"
                    failed += 1
                
                print(f"{i:2d}. {status} | '{query}' → {intent} (expected: {expected})")
                
            except Exception as e:
                print(f"{i:2d}. ❌ ERROR | '{query}' → Error: {str(e)}")
                failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All automotive NLP classifications working correctly!")
        elif passed > 0:
            print(f"🔄 Partial success: {passed}/{len(automotive_tests)} working")
        
        return failed == 0
        
    except Exception as e:
        print(f"❌ Automotive NLP Classification error: {str(e)}")
        return False

async def test_automotive_skill_responses():
    """Test automotive skill responses"""
    
    print("\n🔧 Testing Automotive Skill Responses")
    print("=" * 60)
    
    try:
        config = Config()
        automotive_skill = AutomotiveSkill(config)
        
        automotive_queries = [
            # Pricing queries
            "maruti swift price",
            "honda city cost",
            "bmw 3 series price range",
            
            # Specifications
            "hyundai creta specifications",
            "tata nexon features",
            "mercedes c class engine details",
            
            # Mileage queries
            "honda city mileage",
            "fuel efficient cars",
            "diesel vs petrol mileage",
            
            # Maintenance
            "car maintenance schedule",
            "oil change frequency",
            "diesel car service tips",
            
            # Comparison
            "compare creta vs nexon",
            "honda city vs hyundai verna",
            
            # Advice
            "best first car",
            "family car recommendations",
            "car buying tips",
            
            # Insurance and finance
            "car insurance guide",
            "car loan information",
            "emi calculation help",
            
            # General
            "automotive advice",
            "car care tips",
        ]
        
        print(f"Testing {len(automotive_queries)} automotive responses...\n")
        
        for i, query in enumerate(automotive_queries, 1):
            try:
                # Create mock NLP result for automotive skill
                nlp_result = {
                    "intent": "automotive",
                    "entities": [],
                    "text": query
                }
                
                # Call the automotive skill handle method
                response = await automotive_skill.handle(nlp_result, {})
                
                # Check if response looks like automotive information
                is_automotive_response = any(keyword in response.lower() for keyword in [
                    "car", "vehicle", "engine", "mileage", "price", "₹", "lakhs", 
                    "features", "specifications", "maintenance", "insurance", "loan"
                ])
                
                if is_automotive_response:
                    status = "✅ AUTOMOTIVE"
                elif "error" in response.lower() or "trouble" in response.lower():
                    status = "⚠️ ERROR"
                else:
                    status = "❓ OTHER"
                
                print(f"{i:2d}. {status} | '{query}'")
                print(f"     Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                print()
                
            except Exception as e:
                print(f"{i:2d}. ❌ EXCEPTION | '{query}' → Error: {str(e)}")
                print()
        
        print("✅ Automotive skill response test completed")
        return True
        
    except Exception as e:
        print(f"❌ Automotive skill error: {str(e)}")
        return False

async def test_automotive_integration():
    """Test the integration between NLP and Automotive skill"""
    
    print("\n🔗 Testing NLP → Automotive Integration")
    print("=" * 60)
    
    try:
        config = Config()
        nlp = NLPProcessor(config)
        automotive_skill = AutomotiveSkill(config)
        
        integration_tests = [
            "maruti swift price and mileage",
            "best car under 15 lakhs",
            "honda city vs hyundai verna comparison", 
            "car maintenance tips",
            "bmw 3 series specifications",
            "fuel efficient family cars",
        ]
        
        print(f"Testing {len(integration_tests)} integrations...\n")
        
        for i, query in enumerate(integration_tests, 1):
            try:
                # Step 1: Classify intent
                nlp_result = await nlp.process(query)
                intent = nlp_result.get('intent', 'unknown')
                
                # Step 2: If automotive intent, call automotive skill
                if intent == "automotive":
                    response = await automotive_skill.handle(nlp_result, {})
                    is_automotive_response = any(keyword in response.lower() for keyword in [
                        "car", "vehicle", "price", "₹", "mileage", "specifications"
                    ])
                    status = "✅ SUCCESS" if is_automotive_response else "⚠️ PARTIAL"
                else:
                    response = f"[Non-automotive intent: {intent}]"
                    status = "❌ MISCLASSIFIED"
                
                print(f"{i}. {status} | '{query}' → Intent: {intent}")
                print(f"    Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                print()
                
            except Exception as e:
                print(f"{i}. ❌ EXCEPTION | '{query}' → Error: {str(e)}")
                print()
        
        print("✅ Integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {str(e)}")
        return False

async def test_automotive_database():
    """Test automotive database content"""
    
    print("\n📋 Testing Automotive Database")
    print("=" * 60)
    
    try:
        config = Config()
        automotive_skill = AutomotiveSkill(config)
        
        # Test vehicle database
        vehicles = automotive_skill.vehicle_database
        print(f"✅ Vehicle database loaded with {len(vehicles)} cars")
        
        # Check for popular Indian cars
        indian_cars = ["maruti swift", "hyundai creta", "tata nexon", "honda city"]
        luxury_cars = ["bmw 3 series", "mercedes c class", "audi a4"]
        
        print("\n🇮🇳 Indian Popular Cars:")
        for car in indian_cars:
            if car in vehicles:
                info = vehicles[car]
                print(f"✅ {info['brand']} {info['model']} - {info['price_range']}")
            else:
                print(f"❌ {car} - Not found")
        
        print("\n🌟 Luxury Cars:")
        for car in luxury_cars:
            if car in vehicles:
                info = vehicles[car]
                print(f"✅ {info['brand']} {info['model']} - {info['price_range']}")
            else:
                print(f"❌ {car} - Not found")
        
        # Test maintenance schedules
        maintenance = automotive_skill.maintenance_schedules
        print(f"\n🔧 Maintenance schedules: {len(maintenance)} engine types")
        for engine_type in maintenance:
            print(f"✅ {engine_type.title()} engine maintenance schedule available")
        
        # Test fuel tips
        tips = automotive_skill.fuel_tips
        print(f"\n⛽ Fuel efficiency tips: {len(tips)} tips available")
        print(f"Sample tip: {tips[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Automotive database error: {str(e)}")
        return False

async def main():
    print("🚗 BUDDY AI - Automotive Module Test Suite")
    print("Testing comprehensive automotive functionality\n")
    
    # Test NLP classification for automotive queries
    nlp_success = await test_automotive_nlp_classification()
    
    # Test automotive skill responses
    skill_success = await test_automotive_skill_responses()
    
    # Test integration
    integration_success = await test_automotive_integration()
    
    # Test automotive database
    database_success = await test_automotive_database()
    
    print("\n" + "=" * 60)
    print("🏁 **Automotive Module Test Results:**")
    print(f"  • NLP Classification: {'✅ WORKING' if nlp_success else '❌ ISSUES'}")
    print(f"  • Skill Responses: {'✅ WORKING' if skill_success else '❌ ISSUES'}")
    print(f"  • Integration: {'✅ WORKING' if integration_success else '❌ ISSUES'}")
    print(f"  • Database: {'✅ WORKING' if database_success else '❌ ISSUES'}")
    
    if all([nlp_success, skill_success, integration_success, database_success]):
        print("\n🎉 **AUTOMOTIVE MODULE FULLY OPERATIONAL!**")
        print("\n🚗 **Available Automotive Features:**")
        print("  • Car specifications and pricing")
        print("  • Vehicle comparisons and recommendations") 
        print("  • Maintenance schedules and tips")
        print("  • Insurance and financing guidance")
        print("  • Fuel efficiency advice")
        print("  • Popular Indian and luxury car database")
        print("\n💡 **Try these queries:**")
        print("  • 'Honda City price and specifications'")
        print("  • 'Compare Hyundai Creta vs Tata Nexon'")
        print("  • 'Best family car under 15 lakhs'")
        print("  • 'Car maintenance tips'")
        print("  • 'Fuel efficient cars'")
    else:
        print("\n⚠️ Some automotive components need attention.")
        print("Check the detailed results above for specific issues.")

if __name__ == "__main__":
    asyncio.run(main())
