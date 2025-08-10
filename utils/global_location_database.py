"""
Global location database for weather queries
"""
import json
import os
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher

class GlobalLocationDatabase:
    """Database of global locations with coordinates and spell checking"""
    
    def __init__(self):
        self.locations = {
            # Major cities with coordinates
            "New York": {"coordinates": {"lat": 40.7128, "lon": -74.0060}, "country": "US", "type": "city"},
            "London": {"coordinates": {"lat": 51.5074, "lon": -0.1278}, "country": "GB", "type": "city"},
            "Paris": {"coordinates": {"lat": 48.8566, "lon": 2.3522}, "country": "FR", "type": "city"},
            "Tokyo": {"coordinates": {"lat": 35.6762, "lon": 139.6503}, "country": "JP", "type": "city"},
            "Delhi": {"coordinates": {"lat": 28.7041, "lon": 77.1025}, "country": "IN", "type": "city"},
            "Mumbai": {"coordinates": {"lat": 19.0760, "lon": 72.8777}, "country": "IN", "type": "city"},
            "Bangalore": {"coordinates": {"lat": 12.9716, "lon": 77.5946}, "country": "IN", "type": "city"},
            "Chennai": {"coordinates": {"lat": 13.0827, "lon": 80.2707}, "country": "IN", "type": "city"},
            "Kolkata": {"coordinates": {"lat": 22.5726, "lon": 88.3639}, "country": "IN", "type": "city"},
            "Hyderabad": {"coordinates": {"lat": 17.3850, "lon": 78.4867}, "country": "IN", "type": "city"},
            "Kanyakumari": {"coordinates": {"lat": 8.0883, "lon": 77.5385}, "country": "IN", "type": "city"},
            "Madurai": {"coordinates": {"lat": 9.9252, "lon": 78.1198}, "country": "IN", "type": "city"},
            "Singapore": {"coordinates": {"lat": 1.3521, "lon": 103.8198}, "country": "SG", "type": "city"},
            "Kuala Lumpur": {"coordinates": {"lat": 3.1390, "lon": 101.6869}, "country": "MY", "type": "city"},
            "Bangkok": {"coordinates": {"lat": 13.7563, "lon": 100.5018}, "country": "TH", "type": "city"},
            "Dubai": {"coordinates": {"lat": 25.2048, "lon": 55.2708}, "country": "AE", "type": "city"},
            "Los Angeles": {"coordinates": {"lat": 34.0522, "lon": -118.2437}, "country": "US", "type": "city"},
            "San Francisco": {"coordinates": {"lat": 37.7749, "lon": -122.4194}, "country": "US", "type": "city"},
            "Chicago": {"coordinates": {"lat": 41.8781, "lon": -87.6298}, "country": "US", "type": "city"},
            "Washington DC": {"coordinates": {"lat": 38.9072, "lon": -77.0369}, "country": "US", "type": "city"},
            
            # Countries
            "Malaysia": {"coordinates": {"lat": 4.2105, "lon": 101.9758}, "type": "country"},
            "Israel": {"coordinates": {"lat": 31.0461, "lon": 34.8516}, "type": "country"},
            "India": {"coordinates": {"lat": 20.5937, "lon": 78.9629}, "type": "country"},
            "United States": {"coordinates": {"lat": 37.0902, "lon": -95.7129}, "type": "country"},
            "United Kingdom": {"coordinates": {"lat": 55.3781, "lon": -3.4360}, "type": "country"},
            "Japan": {"coordinates": {"lat": 36.2048, "lon": 138.2529}, "type": "country"},
            "Thailand": {"coordinates": {"lat": 15.8700, "lon": 100.9925}, "type": "country"},
            "Australia": {"coordinates": {"lat": -25.2744, "lon": 133.7751}, "type": "country"},
            "Austria": {"coordinates": {"lat": 47.5162, "lon": 14.5501}, "type": "country"},
            "Germany": {"coordinates": {"lat": 51.1657, "lon": 10.4515}, "type": "country"},
            "France": {"coordinates": {"lat": 46.2276, "lon": 2.2137}, "type": "country"},
            "Italy": {"coordinates": {"lat": 41.8719, "lon": 12.5674}, "type": "country"},
            "Spain": {"coordinates": {"lat": 40.4637, "lon": -3.7492}, "type": "country"},
            "Canada": {"coordinates": {"lat": 56.1304, "lon": -106.3468}, "type": "country"},
            "Brazil": {"coordinates": {"lat": -14.2350, "lon": -51.9253}, "type": "country"},
            "China": {"coordinates": {"lat": 35.8617, "lon": 104.1954}, "type": "country"},
            "Russia": {"coordinates": {"lat": 61.5240, "lon": 105.3188}, "type": "country"},
            "California": {"coordinates": {"lat": 36.7783, "lon": -119.4179}, "type": "state"},
        }
        
        # Alternative names and aliases
        self.aliases = {
            "US": "United States",
            "USA": "United States",
            "UK": "United Kingdom",
            "Britain": "United Kingdom",
            "NYC": "New York",
            "LA": "Los Angeles",
            "SF": "San Francisco",
            "KL": "Kuala Lumpur",
            "Bengaluru": "Bangalore",
            "Bombay": "Mumbai",
            "Calcutta": "Kolkata",
            "DC": "Washington DC",
            "autralia": "Australia",
            "austrialia": "Australia",
            "aussie": "Australia",
            "oz": "Australia",
            "ciatel": "Israel"
        }
    
    def find_location(self, query: str) -> Tuple[Optional[str], str, float, List[str]]:
        """
        Find location in database with fuzzy matching
        Returns: (best_match, location_type, confidence, suggestions)
        """
        query = query.strip()
        
        # Exact match
        if query in self.locations:
            return query, self.locations[query].get("type", "unknown"), 1.0, []
        
        # Check aliases
        if query in self.aliases:
            actual_name = self.aliases[query]
            return actual_name, self.locations[actual_name].get("type", "unknown"), 1.0, []
        
        # Case-insensitive exact match
        query_lower = query.lower()
        for location in self.locations:
            if location.lower() == query_lower:
                return location, self.locations[location].get("type", "unknown"), 1.0, []
        
        # Fuzzy matching
        suggestions = []
        best_match = None
        best_score = 0.0
        
        all_names = list(self.locations.keys()) + list(self.aliases.keys())
        
        for name in all_names:
            similarity = SequenceMatcher(None, query_lower, name.lower()).ratio()
            if similarity > 0.6:
                actual_name = self.aliases.get(name, name)
                if similarity > best_score:
                    best_score = similarity
                    best_match = actual_name
                if actual_name not in suggestions:
                    suggestions.append(actual_name)
        
        # Sort suggestions by similarity
        suggestions.sort(key=lambda x: SequenceMatcher(None, query_lower, x.lower()).ratio(), reverse=True)
        
        return best_match, self.locations.get(best_match, {}).get("type", "unknown") if best_match else "unknown", best_score, suggestions[:5]
    
    def get_location_info(self, location: str) -> Optional[Dict]:
        """Get detailed information about a location"""
        # Check direct match
        if location in self.locations:
            return {"name": location, "data": self.locations[location]}
        
        # Check aliases
        if location in self.aliases:
            actual_name = self.aliases[location]
            return {"name": actual_name, "data": self.locations[actual_name]}
        
        return None
    
    def add_location(self, name: str, lat: float, lon: float, country: str = None, loc_type: str = "city"):
        """Add a new location to the database"""
        self.locations[name] = {
            "coordinates": {"lat": lat, "lon": lon},
            "type": loc_type
        }
        if country:
            self.locations[name]["country"] = country

# Global instance
global_location_db = GlobalLocationDatabase()
