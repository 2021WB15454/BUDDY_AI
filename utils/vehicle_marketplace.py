"""
Vehicle Marketplace and Dealership Locator for BUDDY AI
Provides information about car dealerships, showrooms, and automotive services
"""

import logging
from typing import Dict, List, Optional

class VehicleMarketplace:
    """
    Vehicle marketplace for finding dealerships, showrooms, and automotive services
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Dealership database by city
        self.dealerships = {
            "chennai": {
                "maruti": [
                    {"name": "Maruti Suzuki Arena Velachery", "address": "Velachery Main Road", "phone": "044-2266-8888", "services": ["Sales", "Service", "Spare Parts"]},
                    {"name": "Maruti Suzuki Nexa Anna Nagar", "address": "Anna Nagar East", "phone": "044-2615-5555", "services": ["Premium Sales", "Service"]},
                    {"name": "Maruti Suzuki Arena OMR", "address": "Old Mahabalipuram Road", "phone": "044-4477-9999", "services": ["Sales", "Service", "Insurance"]}
                ],
                "hyundai": [
                    {"name": "Hyundai Showroom T Nagar", "address": "T Nagar", "phone": "044-2834-7777", "services": ["Sales", "Service", "BlueLink"]},
                    {"name": "Hyundai Service Center Porur", "address": "Porur", "phone": "044-2480-6666", "services": ["Service", "Spare Parts", "Body Shop"]}
                ],
                "honda": [
                    {"name": "Honda Cars Nungambakkam", "address": "Nungambakkam High Road", "phone": "044-2833-5555", "services": ["Sales", "Service", "Honda Sensing"]},
                    {"name": "Honda Service Center Chromepet", "address": "Chromepet", "phone": "044-2235-4444", "services": ["Service", "Genuine Parts"]}
                ],
                "bmw": [
                    {"name": "BMW Showroom Chennai", "address": "Cathedral Road", "phone": "044-2811-2222", "services": ["Sales", "Service", "BMW Excellence Club"]},
                    {"name": "BMW Service Center OMR", "address": "Thoraipakkam", "phone": "044-2496-1111", "services": ["Service", "BMW Motorrad", "Spare Parts"]}
                ]
            },
            "bangalore": {
                "maruti": [
                    {"name": "Maruti Suzuki Arena Electronic City", "address": "Electronic City Phase 1", "phone": "080-2852-7777", "services": ["Sales", "Service", "Exchange"]},
                    {"name": "Maruti Suzuki Nexa Koramangala", "address": "Koramangala 5th Block", "phone": "080-4112-8888", "services": ["Premium Sales", "Service"]}
                ],
                "tata": [
                    {"name": "Tata Motors Showroom Whitefield", "address": "Whitefield Main Road", "phone": "080-2845-6666", "services": ["Sales", "Service", "Connected Vehicle"]},
                    {"name": "Tata Service Center Hebbal", "address": "Hebbal", "phone": "080-2341-5555", "services": ["Service", "Genuine Parts", "24x7 Roadside"]}
                ],
                "bmw": [
                    {"name": "BMW Showroom Bangalore", "address": "Residency Road", "phone": "080-2559-3333", "services": ["Sales", "Service", "BMW i"]},
                    {"name": "BMW Service Center Sarjapur", "address": "Sarjapur Road", "phone": "080-2844-4444", "services": ["Service", "BMW ConnectedDrive"]}
                ]
            },
            "mumbai": {
                "maruti": [
                    {"name": "Maruti Suzuki Arena Andheri", "address": "Andheri West", "phone": "022-2673-9999", "services": ["Sales", "Service", "Insurance"]},
                    {"name": "Maruti Suzuki Nexa Bandra", "address": "Bandra Kurla Complex", "phone": "022-2652-7777", "services": ["Premium Sales", "Service"]}
                ],
                "hyundai": [
                    {"name": "Hyundai Showroom Powai", "address": "Powai", "phone": "022-2570-8888", "services": ["Sales", "Service", "Blue Link"]},
                    {"name": "Hyundai Service Center Goregaon", "address": "Goregaon East", "phone": "022-2840-6666", "services": ["Service", "Spare Parts"]}
                ],
                "mercedes": [
                    {"name": "Mercedes-Benz Showroom Mumbai", "address": "Worli", "phone": "022-2496-5555", "services": ["Sales", "Service", "AMG Performance"]},
                    {"name": "Mercedes-Benz Service Center Thane", "address": "Thane West", "phone": "022-2534-4444", "services": ["Service", "Genuine Parts", "Express Service"]}
                ]
            },
            "delhi": {
                "maruti": [
                    {"name": "Maruti Suzuki Arena Connaught Place", "address": "Connaught Place", "phone": "011-2341-8888", "services": ["Sales", "Service", "Corporate"]},
                    {"name": "Maruti Suzuki Nexa Gurgaon", "address": "Sector 14, Gurgaon", "phone": "0124-456-7777", "services": ["Premium Sales", "Service"]}
                ],
                "honda": [
                    {"name": "Honda Cars Delhi", "address": "Rajouri Garden", "phone": "011-2545-6666", "services": ["Sales", "Service", "Honda Connect"]},
                    {"name": "Honda Service Center Noida", "address": "Sector 63, Noida", "phone": "0120-234-5555", "services": ["Service", "Genuine Parts"]}
                ],
                "audi": [
                    {"name": "Audi Delhi Showroom", "address": "Mathura Road", "phone": "011-2634-3333", "services": ["Sales", "Service", "Audi Sport"]},
                    {"name": "Audi Service Center Gurgaon", "address": "DLF Phase 2", "phone": "0124-456-2222", "services": ["Service", "Audi Genuine Parts", "quattro Service"]}
                ]
            },
            "pune": {
                "tata": [
                    {"name": "Tata Motors Showroom Pune", "address": "FC Road", "phone": "020-2553-7777", "services": ["Sales", "Service", "Commercial Vehicles"]},
                    {"name": "Tata Service Center Hadapsar", "address": "Hadapsar", "phone": "020-2693-6666", "services": ["Service", "Fleet Solutions"]}
                ],
                "mahindra": [
                    {"name": "Mahindra Showroom Baner", "address": "Baner Road", "phone": "020-2729-5555", "services": ["Sales", "Service", "Farm Equipment"]},
                    {"name": "Mahindra Service Center Katraj", "address": "Katraj", "phone": "020-2422-4444", "services": ["Service", "Genuine Parts", "4WD Service"]}
                ]
            }
        }
        
        # Automotive services by type
        self.automotive_services = {
            "insurance": {
                "companies": ["HDFC ERGO", "ICICI Lombard", "Bajaj Allianz", "Reliance General", "New India Assurance", "Oriental Insurance"],
                "types": ["Third Party", "Comprehensive", "Zero Depreciation", "Engine Protection", "Return to Invoice"],
                "features": ["Cashless Claims", "24x7 Support", "Online Renewal", "No Claim Bonus", "Add-on Covers"]
            },
            "financing": {
                "banks": ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra", "Bank of Baroda"],
                "nbfcs": ["Mahindra Finance", "Tata Capital", "L&T Finance", "Bajaj Finance", "Cholamandalam"],
                "features": ["Competitive Rates", "Quick Approval", "Minimal Documentation", "Pre-approved Loans", "Flexible EMI"]
            },
            "maintenance": {
                "multi_brand": ["Bosch Car Service", "3M Car Care", "GoMechanic", "Carnation Auto", "Royal Sundaram"],
                "specialized": ["German Auto Experts", "JCB Service", "TVS Service", "Hero Service", "Royal Enfield"],
                "services": ["Periodic Service", "AC Service", "Brake Service", "Engine Overhaul", "Paint & Body"]
            }
        }
    
    def find_dealerships(self, brand: str, city: str) -> List[Dict]:
        """Find dealerships for a brand in a city"""
        city_lower = city.lower()
        brand_lower = brand.lower()
        
        if city_lower in self.dealerships:
            if brand_lower in self.dealerships[city_lower]:
                return self.dealerships[city_lower][brand_lower]
        
        return []
    
    def get_automotive_services(self, service_type: str, city: str = None) -> Dict:
        """Get automotive services information"""
        service_lower = service_type.lower()
        
        if service_lower in self.automotive_services:
            return self.automotive_services[service_lower]
        
        return {}
    
    def search_nearby_services(self, location: str, service_type: str = "all") -> str:
        """Search for nearby automotive services"""
        location_lower = location.lower()
        
        # Check if location is in our database
        if location_lower in self.dealerships:
            response = f"🏪 **Automotive Services in {location.title()}:**\n\n"
            
            for brand, dealerships in self.dealerships[location_lower].items():
                response += f"**{brand.title()} ({len(dealerships)} locations):**\n"
                for dealer in dealerships[:2]:  # Show top 2
                    response += f"• {dealer['name']} - {dealer['address']}\n"
                    response += f"  📞 {dealer['phone']} | Services: {', '.join(dealer['services'])}\n"
                response += "\n"
            
            response += "🔧 **Other Services Available:**\n"
            response += "• Multi-brand service centers\n"
            response += "• Insurance providers\n" 
            response += "• Financing options\n"
            response += "• Spare parts dealers\n"
            
            return response
        else:
            return f"🔍 **Automotive Services Search:**\n\n" \
                   f"I don't have detailed information for {location}, but here are general options:\n\n" \
                   f"**Dealership Networks:**\n" \
                   f"• Maruti Suzuki (Arena & Nexa)\n" \
                   f"• Hyundai Motors\n" \
                   f"• Tata Motors\n" \
                   f"• Honda Cars\n" \
                   f"• Mahindra & Mahindra\n\n" \
                   f"**Service Centers:**\n" \
                   f"• Bosch Car Service\n" \
                   f"• 3M Car Care\n" \
                   f"• GoMechanic\n\n" \
                   f"💡 *Try searching for specific cities like Chennai, Bangalore, Mumbai, Delhi, or Pune for detailed listings.*"
    
    def get_brand_info(self, brand: str) -> str:
        """Get information about a car brand"""
        brand_lower = brand.lower()
        
        brand_info = {
            "maruti": {
                "full_name": "Maruti Suzuki India Limited",
                "origin": "India (Partnership with Suzuki, Japan)",
                "founded": "1981",
                "headquarters": "New Delhi, India",
                "popular_models": ["Swift", "Baleno", "Dzire", "Ertiga", "Brezza", "XL6"],
                "segments": ["Arena (Mass Market)", "Nexa (Premium)"],
                "strengths": ["Market Leader", "Fuel Efficiency", "Service Network", "Resale Value"],
                "website": "marutisuzuki.com"
            },
            "hyundai": {
                "full_name": "Hyundai Motor India Limited",
                "origin": "South Korea",
                "founded": "1996 (India operations)",
                "headquarters": "Chennai, India",
                "popular_models": ["Creta", "Venue", "Verna", "Grand i10 NIOS", "Tucson"],
                "segments": ["Mass Market", "Premium SUVs"],
                "strengths": ["Design", "Features", "Build Quality", "BlueLink Technology"],
                "website": "hyundai.com/in"
            },
            "tata": {
                "full_name": "Tata Motors Limited",
                "origin": "India",
                "founded": "1945",
                "headquarters": "Mumbai, India",
                "popular_models": ["Nexon", "Harrier", "Safari", "Punch", "Altroz"],
                "segments": ["Passenger Vehicles", "Commercial Vehicles"],
                "strengths": ["Safety", "Design", "Indian Heritage", "Connected Car Tech"],
                "website": "tatamotors.com"
            },
            "honda": {
                "full_name": "Honda Cars India Limited",
                "origin": "Japan",
                "founded": "1997 (India operations)",
                "headquarters": "Delhi NCR, India",
                "popular_models": ["City", "Amaze", "Jazz", "WR-V"],
                "segments": ["Premium Sedans", "Compact Cars"],
                "strengths": ["Reliability", "Engine Technology", "Honda Sensing", "Resale Value"],
                "website": "hondacarindia.com"
            },
            "bmw": {
                "full_name": "Bayerische Motoren Werke AG",
                "origin": "Germany",
                "founded": "1916",
                "headquarters": "Munich, Germany",
                "popular_models": ["3 Series", "5 Series", "X1", "X3", "X5"],
                "segments": ["Luxury Cars", "Sports Cars", "SUVs", "Electric (BMW i)"],
                "strengths": ["Performance", "Luxury", "Technology", "Driving Dynamics"],
                "website": "bmw.in"
            }
        }
        
        if brand_lower in brand_info:
            info = brand_info[brand_lower]
            return f"🏢 **{info['full_name']}**\n\n" \
                   f"**Origin:** {info['origin']}\n" \
                   f"**Founded:** {info['founded']}\n" \
                   f"**India HQ:** {info['headquarters']}\n\n" \
                   f"**Popular Models:** {', '.join(info['popular_models'])}\n" \
                   f"**Segments:** {', '.join(info['segments'])}\n\n" \
                   f"**Key Strengths:**\n" + "\n".join([f"• {strength}" for strength in info['strengths']]) + \
                   f"\n\n**Website:** {info['website']}\n\n" \
                   f"💡 *Ask about specific models, dealerships, or services for this brand!*"
        else:
            return f"🔍 I don't have detailed information about {brand} in my database. " \
                   f"I have comprehensive information about Maruti Suzuki, Hyundai, Tata Motors, Honda, and BMW. " \
                   f"Ask about any of these brands for detailed information!"

# Global instance
vehicle_marketplace = VehicleMarketplace()
