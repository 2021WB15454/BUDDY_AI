"""
Automotive Skill for BUDDY AI Assistant
Handles vehicle information, specifications, pricing, maintenance, and automotive services
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from utils.vehicle_marketplace import vehicle_marketplace

class AutomotiveSkill:
    """
    Automotive skill for handling car-related queries including:
    - Vehicle specifications and comparisons
    - Pricing and market information
    - Maintenance schedules and tips
    - Fuel efficiency calculations
    - Insurance and financing guidance
    - Automotive industry news and trends
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize vehicle marketplace
        self.vehicle_marketplace = vehicle_marketplace
        
        # Automotive database
        self.vehicle_database = {
            # Popular Cars in India
            "maruti swift": {
                "brand": "Maruti Suzuki",
                "model": "Swift",
                "type": "Hatchback",
                "price_range": "₹5.9 - 8.7 Lakhs",
                "mileage": "22-24 kmpl",
                "engine": "1.2L Petrol",
                "seating": "5",
                "features": ["ABS", "Airbags", "Touchscreen", "Bluetooth"],
                "popular_variants": ["LXI", "VXI", "ZXI", "ZXI+"]
            },
            "hyundai creta": {
                "brand": "Hyundai",
                "model": "Creta",
                "type": "Compact SUV",
                "price_range": "₹10.9 - 18.4 Lakhs",
                "mileage": "16-21 kmpl",
                "engine": "1.5L Petrol/Diesel",
                "seating": "5",
                "features": ["Sunroof", "Wireless Charging", "10.25\" Touchscreen", "BlueLink"],
                "popular_variants": ["E", "EX", "S", "SX", "SX(O)"]
            },
            "tata nexon": {
                "brand": "Tata",
                "model": "Nexon",
                "type": "Compact SUV",
                "price_range": "₹7.8 - 14.5 Lakhs",
                "mileage": "17-24 kmpl",
                "engine": "1.2L Turbo Petrol/1.5L Diesel",
                "seating": "5",
                "features": ["7\" Touchscreen", "Harman Audio", "6 Airbags", "ESP"],
                "popular_variants": ["XE", "XM", "XT", "XZ+", "XZA+"]
            },
            "mahindra thar": {
                "brand": "Mahindra",
                "model": "Thar",
                "type": "Off-road SUV",
                "price_range": "₹13.6 - 16.9 Lakhs",
                "mileage": "15-16 kmpl",
                "engine": "2.0L Turbo Petrol/2.2L Diesel",
                "seating": "4-6",
                "features": ["4WD", "Convertible Top", "Touchscreen", "Adventure Ready"],
                "popular_variants": ["AX", "LX"]
            },
            "honda city": {
                "brand": "Honda",
                "model": "City",
                "type": "Sedan",
                "price_range": "₹11.8 - 16.4 Lakhs",
                "mileage": "17-24 kmpl",
                "engine": "1.5L Petrol/Hybrid",
                "seating": "5",
                "features": ["Honda SENSING", "Sunroof", "8\" Display", "Cruise Control"],
                "popular_variants": ["V", "VX", "ZX"]
            },
            # Luxury Cars
            "bmw 3 series": {
                "brand": "BMW",
                "model": "3 Series",
                "type": "Luxury Sedan",
                "price_range": "₹42.3 - 52.8 Lakhs",
                "mileage": "13-16 kmpl",
                "engine": "2.0L Turbo Petrol/Diesel",
                "seating": "5",
                "features": ["iDrive", "Adaptive Suspension", "LED Headlights", "Wireless Charging"],
                "popular_variants": ["Sport", "Luxury Line", "M Sport"]
            },
            "mercedes c class": {
                "brand": "Mercedes-Benz",
                "model": "C-Class",
                "type": "Luxury Sedan",
                "price_range": "₹56.2 - 66.8 Lakhs",
                "mileage": "13-15 kmpl",
                "engine": "1.5L Turbo Petrol",
                "seating": "5",
                "features": ["MBUX", "Air Suspension", "64-color Ambient Lighting", "Burmester Audio"],
                "popular_variants": ["C200", "C220d"]
            },
            "audi a4": {
                "brand": "Audi",
                "model": "A4",
                "type": "Luxury Sedan",
                "price_range": "₹42.3 - 49.2 Lakhs",
                "mileage": "14-17 kmpl",
                "engine": "2.0L TFSI Petrol",
                "seating": "5",
                "features": ["MMI Touch", "Virtual Cockpit", "Matrix LED", "Quattro AWD"],
                "popular_variants": ["Premium", "Premium Plus", "Technology"]
            }
        }
        
        # Maintenance schedules
        self.maintenance_schedules = {
            "petrol": {
                "oil_change": "5000-7500 km or 6 months",
                "air_filter": "10000-15000 km or 12 months",
                "spark_plugs": "20000-30000 km or 2 years",
                "brake_pads": "20000-40000 km (varies by usage)",
                "battery": "3-5 years",
                "tyres": "40000-60000 km (varies by driving)"
            },
            "diesel": {
                "oil_change": "7500-10000 km or 6 months",
                "air_filter": "10000-15000 km or 12 months",
                "fuel_filter": "15000-20000 km or 18 months",
                "brake_pads": "20000-40000 km (varies by usage)",
                "battery": "3-5 years",
                "tyres": "40000-60000 km (varies by driving)"
            }
        }
        
        # Fuel efficiency tips
        self.fuel_tips = [
            "Maintain proper tire pressure - can improve mileage by 3-5%",
            "Regular servicing and clean air filters boost efficiency",
            "Avoid aggressive acceleration and hard braking",
            "Use cruise control on highways for consistent speed",
            "Remove excess weight from your vehicle",
            "Plan and combine trips to reduce cold starts",
            "Keep windows closed at high speeds, use AC efficiently",
            "Regular wheel alignment and balancing",
            "Use the recommended grade of motor oil",
            "Turn off engine during long idles (traffic signals)"
        ]
    
    async def handle(self, nlp_result: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Handle automotive-related queries"""
        try:
            text = nlp_result.get("text", "").lower()
            intent = nlp_result.get("intent", "")
            
            # Extract car model if mentioned
            mentioned_car = self._extract_car_model(text)
            
            # Route to specific handlers based on query type
            if any(word in text for word in ["dealership", "dealer", "showroom", "service center", "near me", "in chennai", "in bangalore", "in mumbai", "in delhi", "in pune"]):
                return await self._handle_dealership_query(text, mentioned_car)
            elif any(word in text for word in ["brand info", "company", "manufacturer", "about brand", "brand details"]):
                return await self._handle_brand_query(text, mentioned_car)
            elif any(word in text for word in ["price", "cost", "expensive", "cheap", "budget"]):
                return await self._handle_pricing_query(text, mentioned_car)
            elif any(word in text for word in ["mileage", "fuel", "efficiency", "average", "kmpl"]):
                return await self._handle_mileage_query(text, mentioned_car)
            elif any(word in text for word in ["maintenance", "service", "servicing", "oil change", "schedule"]):
                return await self._handle_maintenance_query(text, mentioned_car)
            elif any(word in text for word in ["specs", "specification", "features", "engine", "power"]):
                return await self._handle_specs_query(text, mentioned_car)
            elif any(word in text for word in ["compare", "comparison", "vs", "versus", "better", "difference"]):
                return await self._handle_comparison_query(text)
            elif any(word in text for word in ["tips", "advice", "recommendation", "suggest", "best"]):
                return await self._handle_advice_query(text)
            elif any(word in text for word in ["insurance", "policy", "coverage", "claim"]):
                return await self._handle_insurance_query(text)
            elif any(word in text for word in ["loan", "financing", "emi", "down payment", "finance"]):
                return await self._handle_finance_query(text)
            elif mentioned_car:
                return await self._handle_general_car_info(mentioned_car)
            else:
                return await self._handle_general_automotive_query(text)
                
        except Exception as e:
            self.logger.error(f"Automotive skill error: {e}")
            return "I'm having trouble with automotive information right now. Please try asking about specific car models, prices, or maintenance tips."

    async def _handle_dealership_query(self, text, car=None):
        """Handle dealership and service center queries."""
        try:
            # Extract city from query
            city = None
            city_keywords = {
                'chennai': 'chennai',
                'bangalore': 'bangalore', 
                'mumbai': 'mumbai',
                'delhi': 'delhi',
                'pune': 'pune'
            }
            
            for keyword, city_name in city_keywords.items():
                if keyword in text.lower():
                    city = city_name
                    break
            
            if not city:
                # Default to general dealership information
                return "🏢 **Dealership Locator Service**\n\nI can help you find dealerships in:\n• Chennai\n• Bangalore\n• Mumbai\n• Delhi\n• Pune\n\nPlease specify a city and brand, for example:\n• 'Honda dealers in Chennai'\n• 'BMW showroom in Bangalore'"
            
            # Extract brand if mentioned
            brand = None
            if car:
                for brand_name in ['maruti', 'hyundai', 'tata', 'honda', 'bmw', 'mercedes', 'audi', 'mahindra']:
                    if brand_name in car.lower():
                        brand = brand_name
                        break
            
            if not brand:
                # Try to extract from text
                for brand_name in ['maruti', 'hyundai', 'tata', 'honda', 'bmw', 'mercedes', 'audi', 'mahindra']:
                    if brand_name in text.lower():
                        brand = brand_name
                        break
            
            if brand:
                # Get specific brand dealerships
                dealerships = self.vehicle_marketplace.find_dealerships(brand, city)
                
                if not dealerships:
                    return f"I don't have {brand.title()} dealership information for {city.title()} currently. Please try another brand or city."
                
                response = f"🏢 **{brand.title()} Dealerships in {city.title()}:**\n\n"
                for dealer in dealerships:
                    response += f"� **{dealer['name']}**\n"
                    response += f"📍 {dealer['address']}\n"
                    response += f"📞 {dealer['phone']}\n"
                    response += f"🔧 Services: {', '.join(dealer['services'])}\n\n"
                
                return response
            else:
                # Get all dealerships for the city
                return f"🏢 **Auto Dealerships in {city.title()}:**\n\nPlease specify a brand for detailed information:\n• Maruti Suzuki\n• Hyundai\n• Tata Motors\n• Honda\n• BMW\n\nExample: 'Honda dealers in {city}'"
            
        except Exception as e:
            return f"Error retrieving dealership information: {str(e)}"

    async def _handle_brand_query(self, text, car=None):
        """Handle brand information queries."""
        try:
            # Extract brand from query or car
            brand = None
            if car:
                for brand_name in ['Maruti', 'Hyundai', 'Tata', 'Honda', 'BMW']:
                    if brand_name.lower() in car.lower():
                        brand = brand_name
                        break
            
            if not brand:
                # Try to extract from text
                for brand_name in ['maruti', 'hyundai', 'tata', 'honda', 'bmw']:
                    if brand_name in text.lower():
                        brand = brand_name.capitalize()
                        break
            
            if brand:
                return self.vehicle_marketplace.get_brand_info(brand)
            else:
                return "Which brand would you like to know about? I have information on Maruti, Hyundai, Tata, Honda, and BMW."
                
        except Exception as e:
            return f"Error retrieving brand information: {str(e)}"
    
    def _extract_car_model(self, text: str) -> Optional[str]:
        """Extract car model from text"""
        text_lower = text.lower()
        
        # Check for exact matches in our database
        for car_key in self.vehicle_database.keys():
            if car_key in text_lower:
                return car_key
        
        # Check for partial matches (brand names)
        brands = ["maruti", "suzuki", "hyundai", "tata", "mahindra", "honda", "bmw", "mercedes", "audi", "toyota", "ford", "volkswagen"]
        models = ["swift", "creta", "nexon", "thar", "city", "3 series", "c class", "a4", "innova", "fortuner", "scorpio"]
        
        for brand in brands:
            if brand in text_lower:
                for model in models:
                    if model in text_lower:
                        combined = f"{brand} {model}"
                        if combined in self.vehicle_database:
                            return combined
        
        return None
    
    async def _handle_pricing_query(self, text: str, car_model: Optional[str]) -> str:
        """Handle pricing and cost-related queries"""
        if car_model and car_model in self.vehicle_database:
            car_info = self.vehicle_database[car_model]
            return f"💰 **{car_info['brand']} {car_info['model']} Pricing:**\n\n" \
                   f"**Price Range:** {car_info['price_range']}\n" \
                   f"**Type:** {car_info['type']}\n" \
                   f"**Popular Variants:** {', '.join(car_info['popular_variants'])}\n\n" \
                   f"💡 *Tip: Prices may vary by location and dealer. Consider test driving different variants to find the best value for your needs.*"
        else:
            return "💰 **Car Pricing Guide:**\n\n" \
                   "**Budget Cars (₹3-8 Lakhs):** Maruti Swift, Alto, Hyundai Grand i10\n" \
                   "**Mid-Range (₹8-15 Lakhs):** Hyundai Creta, Tata Nexon, Honda City\n" \
                   "**Premium (₹15-30 Lakhs):** Toyota Innova, Mahindra XUV700\n" \
                   "**Luxury (₹30+ Lakhs):** BMW 3 Series, Mercedes C-Class, Audi A4\n\n" \
                   "💡 *Specify a car model for detailed pricing information!*"
    
    async def _handle_mileage_query(self, text: str, car_model: Optional[str]) -> str:
        """Handle fuel efficiency and mileage queries"""
        if car_model and car_model in self.vehicle_database:
            car_info = self.vehicle_database[car_model]
            response = f"⛽ **{car_info['brand']} {car_info['model']} Fuel Efficiency:**\n\n" \
                      f"**Mileage:** {car_info['mileage']}\n" \
                      f"**Engine:** {car_info['engine']}\n" \
                      f"**Type:** {car_info['type']}\n\n"
        else:
            response = "⛽ **Fuel Efficiency Guide:**\n\n" \
                      "**Excellent (20+ kmpl):** Maruti Swift, Honda City Hybrid\n" \
                      "**Good (15-20 kmpl):** Hyundai Creta, Tata Nexon\n" \
                      "**Average (12-15 kmpl):** Premium/Luxury cars\n" \
                      "**SUVs (10-15 kmpl):** Mahindra Thar, Toyota Fortuner\n\n"
        
        # Add fuel efficiency tips
        response += "🔧 **Top Fuel Efficiency Tips:**\n"
        for i, tip in enumerate(self.fuel_tips[:5], 1):
            response += f"{i}. {tip}\n"
        
        return response
    
    async def _handle_maintenance_query(self, text: str, car_model: Optional[str]) -> str:
        """Handle maintenance and service queries"""
        response = "🔧 **Vehicle Maintenance Guide:**\n\n"
        
        if "petrol" in text or "gasoline" in text:
            schedule = self.maintenance_schedules["petrol"]
            response += "**Petrol Engine Maintenance:**\n"
        elif "diesel" in text:
            schedule = self.maintenance_schedules["diesel"]
            response += "**Diesel Engine Maintenance:**\n"
        else:
            schedule = self.maintenance_schedules["petrol"]
            response += "**General Maintenance Schedule:**\n"
        
        for item, interval in schedule.items():
            response += f"• **{item.replace('_', ' ').title()}:** {interval}\n"
        
        response += "\n💡 **Maintenance Tips:**\n" \
                   "• Follow manufacturer's service schedule\n" \
                   "• Use genuine or quality spare parts\n" \
                   "• Regular cleaning and inspection\n" \
                   "• Address issues promptly to avoid bigger problems\n" \
                   "• Keep service records for warranty and resale value"
        
        if car_model and car_model in self.vehicle_database:
            car_info = self.vehicle_database[car_model]
            response += f"\n\n🚗 **Specific to {car_info['brand']} {car_info['model']}:**\n" \
                       f"Consult your authorized {car_info['brand']} service center for model-specific maintenance requirements."
        
        return response
    
    async def _handle_specs_query(self, text: str, car_model: Optional[str]) -> str:
        """Handle specifications and features queries"""
        if car_model and car_model in self.vehicle_database:
            car_info = self.vehicle_database[car_model]
            response = f"📋 **{car_info['brand']} {car_info['model']} Specifications:**\n\n" \
                      f"**Type:** {car_info['type']}\n" \
                      f"**Engine:** {car_info['engine']}\n" \
                      f"**Seating:** {car_info['seating']} passengers\n" \
                      f"**Mileage:** {car_info['mileage']}\n" \
                      f"**Price Range:** {car_info['price_range']}\n\n" \
                      f"**Key Features:**\n"
            
            for feature in car_info['features']:
                response += f"• {feature}\n"
            
            response += f"\n**Available Variants:** {', '.join(car_info['popular_variants'])}"
            
            return response
        else:
            return "📋 **Car Specifications Guide:**\n\n" \
                   "Please specify a car model to get detailed specifications. I have information about:\n\n" \
                   "• **Popular Cars:** Maruti Swift, Hyundai Creta, Tata Nexon\n" \
                   "• **Sedans:** Honda City, BMW 3 Series, Mercedes C-Class\n" \
                   "• **SUVs:** Mahindra Thar, Toyota Fortuner\n" \
                   "• **Luxury Cars:** Audi A4, BMW X3, Mercedes GLC\n\n" \
                   "💡 *Ask: 'Show specs of Honda City' or 'Hyundai Creta features'*"
    
    async def _handle_comparison_query(self, text: str) -> str:
        """Handle car comparison queries"""
        # Extract potential car models for comparison
        mentioned_cars = []
        for car_key in self.vehicle_database.keys():
            if car_key in text.lower():
                mentioned_cars.append(car_key)
        
        if len(mentioned_cars) >= 2:
            car1, car2 = mentioned_cars[0], mentioned_cars[1]
            info1, info2 = self.vehicle_database[car1], self.vehicle_database[car2]
            
            return f"🆚 **{info1['brand']} {info1['model']} vs {info2['brand']} {info2['model']}**\n\n" \
                   f"| Feature | {info1['model']} | {info2['model']} |\n" \
                   f"|---------|----------|----------|\n" \
                   f"| **Price** | {info1['price_range']} | {info2['price_range']} |\n" \
                   f"| **Type** | {info1['type']} | {info2['type']} |\n" \
                   f"| **Mileage** | {info1['mileage']} | {info2['mileage']} |\n" \
                   f"| **Engine** | {info1['engine']} | {info2['engine']} |\n" \
                   f"| **Seating** | {info1['seating']} | {info2['seating']} |\n\n" \
                   f"**{info1['model']} Key Features:** {', '.join(info1['features'][:3])}\n" \
                   f"**{info2['model']} Key Features:** {', '.join(info2['features'][:3])}\n\n" \
                   f"💡 *Consider test driving both vehicles to experience the differences firsthand.*"
        else:
            return "🆚 **Car Comparison Guide:**\n\n" \
                   "I can compare cars when you mention specific models. Try asking:\n\n" \
                   "• 'Compare Hyundai Creta vs Tata Nexon'\n" \
                   "• 'Honda City vs BMW 3 Series comparison'\n" \
                   "• 'Maruti Swift vs Hyundai Grand i10 difference'\n\n" \
                   "**Popular Comparisons:**\n" \
                   "• **Compact SUVs:** Creta vs Nexon vs Seltos\n" \
                   "• **Hatchbacks:** Swift vs i20 vs Baleno\n" \
                   "• **Sedans:** City vs Verna vs Ciaz\n" \
                   "• **Luxury:** BMW 3 Series vs Mercedes C-Class vs Audi A4"
    
    async def _handle_advice_query(self, text: str) -> str:
        """Handle advice and recommendation queries"""
        if any(word in text for word in ["first", "new", "beginner", "family"]):
            return "🚗 **Car Buying Advice for First-Time Buyers:**\n\n" \
                   "**Budget-Friendly Options (₹5-10 Lakhs):**\n" \
                   "• Maruti Swift - Reliable, good resale value\n" \
                   "• Hyundai Grand i10 NIOS - Feature-rich\n" \
                   "• Tata Tiago - Safety-focused\n\n" \
                   "**Family Cars (₹8-15 Lakhs):**\n" \
                   "• Hyundai Creta - Spacious SUV\n" \
                   "• Honda City - Premium sedan\n" \
                   "• Tata Nexon - Safe compact SUV\n\n" \
                   "**Key Considerations:**\n" \
                   "• Define your budget (including insurance, registration)\n" \
                   "• Consider fuel type based on usage\n" \
                   "• Prioritize safety features\n" \
                   "• Check service network availability\n" \
                   "• Take multiple test drives\n" \
                   "• Research resale value"
        else:
            return "💡 **General Automotive Advice:**\n\n" \
                   "**Before Buying:**\n" \
                   "• Research thoroughly online\n" \
                   "• Check reviews and ratings\n" \
                   "• Compare multiple options\n" \
                   "• Visit dealerships for test drives\n" \
                   "• Negotiate price and accessories\n\n" \
                   "**After Purchase:**\n" \
                   "• Follow service schedule religiously\n" \
                   "• Keep all service records\n" \
                   "• Drive responsibly for better mileage\n" \
                   "• Regular cleaning and maintenance\n" \
                   "• Update insurance annually\n\n" \
                   "**Red Flags to Avoid:**\n" \
                   "• Too-good-to-be-true prices\n" \
                   "• Pressure to buy immediately\n" \
                   "• Hidden charges and fees\n" \
                   "• Poor after-sales service reputation"
    
    async def _handle_insurance_query(self, text: str) -> str:
        """Handle insurance-related queries"""
        return "🛡️ **Car Insurance Guide:**\n\n" \
               "**Types of Coverage:**\n" \
               "• **Third-Party:** Mandatory by law (₹2,000-5,000/year)\n" \
               "• **Comprehensive:** Own damage + third-party (₹8,000-25,000/year)\n" \
               "• **Zero Depreciation:** Full claim value (₹12,000-35,000/year)\n\n" \
               "**Key Features to Consider:**\n" \
               "• IDV (Insured Declared Value)\n" \
               "• No Claim Bonus (NCB)\n" \
               "• Roadside assistance\n" \
               "• Engine protection cover\n" \
               "• Consumables cover\n\n" \
               "**Tips for Lower Premiums:**\n" \
               "• Install anti-theft devices\n" \
               "• Maintain good driving record\n" \
               "• Choose higher voluntary deductible\n" \
               "• Compare quotes from multiple insurers\n" \
               "• Renew before expiry for NCB retention\n\n" \
               "💡 *Always read policy terms carefully and choose reputable insurers with good claim settlement ratios.*"
    
    async def _handle_finance_query(self, text: str) -> str:
        """Handle financing and loan queries"""
        return "💳 **Car Loan & Financing Guide:**\n\n" \
               "**Typical Loan Terms:**\n" \
               "• **Interest Rate:** 8.5% - 15% per annum\n" \
               "• **Loan Tenure:** 1-7 years\n" \
               "• **Down Payment:** 10-20% of car value\n" \
               "• **Processing Fee:** 0.5-2% of loan amount\n\n" \
               "**EMI Calculation Example (₹10 Lakhs, 10%, 5 years):**\n" \
               "• Monthly EMI: ~₹21,250\n" \
               "• Total Interest: ~₹2.75 Lakhs\n" \
               "• Total Amount: ~₹12.75 Lakhs\n\n" \
               "**Tips to Get Better Rates:**\n" \
               "• Maintain good credit score (750+)\n" \
               "• Compare offers from multiple banks\n" \
               "• Consider manufacturer financing schemes\n" \
               "• Make higher down payment if possible\n" \
               "• Check for pre-approved loan offers\n\n" \
               "**Documents Required:**\n" \
               "• Income proof, bank statements\n" \
               "• Identity and address proof\n" \
               "• Employment verification\n" \
               "• Car quotation and proforma invoice\n\n" \
               "💡 *Pre-approval helps in negotiating better car prices with dealers.*"
    
    async def _handle_general_car_info(self, car_model: str) -> str:
        """Handle general information about a specific car"""
        if car_model in self.vehicle_database:
            car_info = self.vehicle_database[car_model]
            return f"🚗 **{car_info['brand']} {car_info['model']} Overview:**\n\n" \
                   f"**Type:** {car_info['type']}\n" \
                   f"**Price Range:** {car_info['price_range']}\n" \
                   f"**Mileage:** {car_info['mileage']}\n" \
                   f"**Engine:** {car_info['engine']}\n" \
                   f"**Seating:** {car_info['seating']} passengers\n\n" \
                   f"**Top Features:**\n" + "\n".join([f"• {feature}" for feature in car_info['features']]) + \
                   f"\n\n**Available Variants:** {', '.join(car_info['popular_variants'])}\n\n" \
                   f"💡 *Ask me about pricing, specifications, mileage, or maintenance for more detailed information!*"
        else:
            return f"I don't have detailed information about {car_model} in my database. Please ask about popular models like Maruti Swift, Hyundai Creta, Tata Nexon, Honda City, BMW 3 Series, or Mercedes C-Class."
    
    async def _handle_general_automotive_query(self, text: str) -> str:
        """Handle general automotive queries"""
        return "🚗 **BUDDY AI Automotive Assistant**\n\n" \
               "I can help you with:\n\n" \
               "**🔍 Car Information:**\n" \
               "• Specifications and features\n" \
               "• Pricing and variants\n" \
               "• Fuel efficiency and performance\n" \
               "• Car comparisons\n\n" \
               "**🔧 Maintenance & Care:**\n" \
               "• Service schedules\n" \
               "• Fuel efficiency tips\n" \
               "• General maintenance advice\n\n" \
               "**💰 Financial Guidance:**\n" \
               "• Insurance information\n" \
               "• Loan and financing options\n" \
               "• Buying advice\n\n" \
               "**Popular Queries:**\n" \
               "• 'Honda City price and features'\n" \
               "• 'Compare Creta vs Nexon'\n" \
               "• 'Best mileage cars under 10 lakhs'\n" \
               "• 'Car insurance guide'\n" \
               "• 'Maintenance schedule for diesel cars'\n\n" \
               "💡 *Ask me anything about cars - I'm here to help with your automotive needs!*"

# Initialize skill
def create_skill(config):
    return AutomotiveSkill(config)
