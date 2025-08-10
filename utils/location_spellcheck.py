"""
Location spell checker for weather queries
"""
import json
import os
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher

class LocationSpellChecker:
    """Simple location spell checker with learning capabilities"""
    
    def __init__(self):
        self.corrections = {
            # Common misspellings
            "malasiya": "Malaysia",
            "malaysiya": "Malaysia", 
            "kolalampur": "Kuala Lumpur",
            "kualalampur": "Kuala Lumpur",
            "kolalumpur": "Kuala Lumpur",
            "israil": "Israel",
            "isreal": "Israel",
            "singapur": "Singapore",
            "bangalor": "Bangalore",
            "bangaluru": "Bangalore",
            "mumbay": "Mumbai",
            "kolkatta": "Kolkata",
            "chenai": "Chennai",
            "dilli": "Delhi",
            "hydrabad": "Hyderabad",
            "new yourk": "New York",
            "newyork": "New York",
            "los angelas": "Los Angeles",
            "losangeles": "Los Angeles",
            "sanfrancisco": "San Francisco",
            "washingtondc": "Washington DC"
        }
        
        # Load additional corrections from file if it exists
        self.corrections_file = os.path.join(os.path.dirname(__file__), "learned_corrections.json")
        self._load_learned_corrections()
    
    def check_spelling(self, location: str) -> Tuple[Optional[str], float, List[str]]:
        """
        Check spelling of location and return corrected version
        Returns: (corrected_location, confidence, suggestions)
        """
        location_lower = location.lower().strip()
        
        # Exact match in corrections
        if location_lower in self.corrections:
            return self.corrections[location_lower], 1.0, []
        
        # Find similar matches
        suggestions = []
        best_match = None
        best_score = 0.0
        
        for wrong, correct in self.corrections.items():
            similarity = SequenceMatcher(None, location_lower, wrong).ratio()
            if similarity > 0.8:
                if similarity > best_score:
                    best_score = similarity
                    best_match = correct
                suggestions.append(correct)
        
        # Remove duplicates and sort by relevance
        suggestions = list(set(suggestions))
        
        return best_match, best_score, suggestions[:3]
    
    def learn_correction(self, original: str, corrected: str):
        """Learn a new correction"""
        self.corrections[original.lower().strip()] = corrected
        self._save_learned_corrections()
    
    def _load_learned_corrections(self):
        """Load learned corrections from file"""
        try:
            if os.path.exists(self.corrections_file):
                with open(self.corrections_file, 'r') as f:
                    learned = json.load(f)
                    self.corrections.update(learned)
        except Exception:
            pass
    
    def _save_learned_corrections(self):
        """Save learned corrections to file"""
        try:
            # Only save user-learned corrections, not built-in ones
            learned = {}
            builtin_keys = set([
                "malasiya", "malaysiya", "kolalampur", "kualalampur", "kolalumpur",
                "israil", "isreal", "singapur", "bangalor", "bangaluru", "mumbay",
                "kolkatta", "chenai", "dilli", "hydrabad", "new yourk", "newyork",
                "los angelas", "losangeles", "sanfrancisco", "washingtondc"
            ])
            
            for key, value in self.corrections.items():
                if key not in builtin_keys:
                    learned[key] = value
            
            with open(self.corrections_file, 'w') as f:
                json.dump(learned, f, indent=2)
        except Exception:
            pass

# Global instance
location_checker = LocationSpellChecker()
