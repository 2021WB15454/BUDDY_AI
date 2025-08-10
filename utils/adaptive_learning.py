"""
Adaptive Learning System for BUDDY AI Assistant
Learns from user interactions and improves responses over time
"""
import json
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
import random

class AdaptiveLearningSystem:
    """
    Learning system that adapts BUDDY's responses based on user feedback and interactions
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = "learning_data"
        self.ensure_data_directory()
        
        # Learning files
        self.user_jokes_file = os.path.join(self.data_dir, "user_jokes.json")
        self.user_quotes_file = os.path.join(self.data_dir, "user_quotes.json")
        self.conversation_patterns_file = os.path.join(self.data_dir, "conversation_patterns.json")
        self.user_preferences_file = os.path.join(self.data_dir, "user_preferences.json")
        self.feedback_file = os.path.join(self.data_dir, "user_feedback.json")
        self.location_preferences_file = os.path.join(self.data_dir, "location_preferences.json")
        
        # Load existing data
        self.user_jokes = self.load_json_file(self.user_jokes_file, [])
        self.user_quotes = self.load_json_file(self.user_quotes_file, [])
        self.conversation_patterns = self.load_json_file(self.conversation_patterns_file, {})
        self.user_preferences = self.load_json_file(self.user_preferences_file, {})
        self.feedback_history = self.load_json_file(self.feedback_file, [])
        self.location_preferences = self.load_json_file(self.location_preferences_file, {})
        
    def ensure_data_directory(self):
        """Create learning data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_json_file(self, filepath: str, default):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {e}")
        return default
    
    def save_json_file(self, filepath: str, data):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving {filepath}: {e}")
    
    def learn_from_interaction(self, user_input: str, intent: str, response: str, user_reaction: str = None):
        """Learn from a user interaction"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent": intent,
            "response": response,
            "user_reaction": user_reaction
        }
        
        # Learn conversation patterns
        self.learn_conversation_pattern(user_input, intent)
        
        # If user provided a joke, learn it
        if self.is_user_teaching_joke(user_input):
            self.learn_user_joke(user_input)
        
        # If user provided a quote, learn it
        if self.is_user_teaching_quote(user_input):
            self.learn_user_quote(user_input)
        
        # Learn user preferences
        self.update_user_preferences(user_input, intent)
        
        self.logger.info(f"Learned from interaction: {intent}")
    
    def is_user_teaching_joke(self, user_input: str) -> bool:
        """Detect if user is teaching BUDDY a new joke"""
        teaching_phrases = [
            "here's a joke", "let me tell you a joke", "i have a joke",
            "want to hear a joke", "here's one", "listen to this joke",
            "learn this joke", "remember this joke", "add this joke"
        ]
        return any(phrase in user_input.lower() for phrase in teaching_phrases)
    
    def learn_user_joke(self, user_input: str):
        """Extract and learn a joke from user input"""
        # Simple extraction - look for question-answer pattern or punchline
        text = user_input.lower()
        
        # Try to extract the joke part
        joke_indicators = ["here's a joke", "let me tell you a joke", "i have a joke", "want to hear a joke"]
        for indicator in joke_indicators:
            if indicator in text:
                joke_text = user_input[text.find(indicator) + len(indicator):].strip()
                if joke_text and len(joke_text) > 10:  # Minimum joke length
                    # Clean up the joke
                    joke_text = joke_text.strip(":.,!?")
                    
                    # Add to user jokes if not already there
                    if joke_text not in self.user_jokes:
                        self.user_jokes.append({
                            "joke": joke_text,
                            "learned_from_user": True,
                            "timestamp": datetime.now().isoformat(),
                            "usage_count": 0
                        })
                        self.save_json_file(self.user_jokes_file, self.user_jokes)
                        self.logger.info(f"Learned new joke from user: {joke_text[:50]}...")
                        return True
        return False
    
    def is_user_teaching_quote(self, user_input: str) -> bool:
        """Detect if user is teaching BUDDY a new quote"""
        teaching_phrases = [
            "here's a quote", "let me share a quote", "i have a quote",
            "want to hear a quote", "here's an inspiring quote", "listen to this quote",
            "learn this quote", "remember this quote", "add this quote", "save this quote"
        ]
        return any(phrase in user_input.lower() for phrase in teaching_phrases)
    
    def learn_user_quote(self, user_input: str):
        """Extract and learn a quote from user input"""
        text = user_input.lower()
        
        # Try to extract the quote part
        quote_indicators = ["here's a quote", "let me share a quote", "i have a quote", "remember this quote"]
        for indicator in quote_indicators:
            if indicator in text:
                quote_text = user_input[text.find(indicator) + len(indicator):].strip()
                if quote_text and len(quote_text) > 15:  # Minimum quote length
                    # Clean up the quote
                    quote_text = quote_text.strip(":.,!?")
                    
                    # Add to user quotes if not already there
                    if quote_text not in [q.get("quote", q) if isinstance(q, dict) else q for q in self.user_quotes]:
                        self.user_quotes.append({
                            "quote": quote_text,
                            "learned_from_user": True,
                            "timestamp": datetime.now().isoformat(),
                            "usage_count": 0
                        })
                        self.save_json_file(self.user_quotes_file, self.user_quotes)
                        self.logger.info(f"Learned new quote from user: {quote_text[:50]}...")
                        return True
        return False
    
    def learn_conversation_pattern(self, user_input: str, intent: str):
        """Learn new conversation patterns"""
        input_lower = user_input.lower().strip()
        
        # Track patterns for each intent
        if intent not in self.conversation_patterns:
            self.conversation_patterns[intent] = []
        
        # Defensive check: ensure it's a list
        if not isinstance(self.conversation_patterns[intent], list):
            self.logger.warning(f"⚠️ conversation_patterns[{intent}] was {type(self.conversation_patterns[intent])}, resetting to list")
            self.conversation_patterns[intent] = []
        
        # Add new pattern if not already tracked
        if input_lower not in self.conversation_patterns[intent]:
            self.conversation_patterns[intent].append(input_lower)
            
            # Keep only recent patterns (max 50 per intent)
            if len(self.conversation_patterns[intent]) > 50:
                self.conversation_patterns[intent] = self.conversation_patterns[intent][-50:]
            
            self.save_json_file(self.conversation_patterns_file, self.conversation_patterns)
    
    def update_user_preferences(self, user_input: str, intent: str):
        """Track user preferences and usage patterns"""
        # Count intent usage
        if "intent_frequency" not in self.user_preferences:
            self.user_preferences["intent_frequency"] = {}
        
        if intent not in self.user_preferences["intent_frequency"]:
            self.user_preferences["intent_frequency"][intent] = 0
        
        self.user_preferences["intent_frequency"][intent] += 1
        
        # Track time of day preferences
        current_hour = datetime.now().hour
        if "time_preferences" not in self.user_preferences:
            self.user_preferences["time_preferences"] = {}
        
        if intent not in self.user_preferences["time_preferences"]:
            self.user_preferences["time_preferences"][intent] = []
        
        # Defensive check: ensure it's a list
        if not isinstance(self.user_preferences["time_preferences"][intent], list):
            self.logger.warning(f"⚠️ time_preferences[{intent}] was {type(self.user_preferences['time_preferences'][intent])}, resetting to list")
            self.user_preferences["time_preferences"][intent] = []
        
        self.user_preferences["time_preferences"][intent].append(current_hour)
        
        # Keep only recent data (last 100 interactions per intent)
        if len(self.user_preferences["time_preferences"][intent]) > 100:
            self.user_preferences["time_preferences"][intent] = self.user_preferences["time_preferences"][intent][-100:]
        
        self.save_json_file(self.user_preferences_file, self.user_preferences)
    
    def get_personalized_response(self, intent: str, default_responses: List[str]) -> str:
        """Get a personalized response based on learned preferences"""
        # Defensive check for default_responses
        if default_responses is None:
            default_responses = []
        elif not isinstance(default_responses, list):
            default_responses = []
        
        # For general_conversation, don't provide personalized responses
        # Let the decision engine handle general questions properly
        if intent == "general_conversation":
            return None
        
        # Get user's most frequent intents to personalize responses
        freq = self.user_preferences.get("intent_frequency", {})
        
        # Only provide personalized responses for specific skill intents
        if intent == "joke" and freq.get("joke", 0) > 3:
            humorous_responses = [
                "Here's another one for you!",
                "Ready for a laugh?",
                "Time for some humor!"
            ]
            if default_responses:
                return random.choice(humorous_responses + default_responses)
            return random.choice(humorous_responses)
        
        # If no default responses, return None to indicate no personalized response
        if not default_responses:
            return None
        
        return random.choice(default_responses)
    
    def get_learned_jokes(self) -> List[str]:
        """Get jokes learned from users"""
        active_jokes = []
        for joke_data in self.user_jokes:
            if isinstance(joke_data, dict):
                active_jokes.append(joke_data["joke"])
                # Increment usage count
                joke_data["usage_count"] = joke_data.get("usage_count", 0) + 1
            else:
                # Handle old format
                active_jokes.append(joke_data)
        
        # Save updated usage counts
        if active_jokes:
            self.save_json_file(self.user_jokes_file, self.user_jokes)
        
        return active_jokes
    
    def get_learned_quotes(self) -> List[str]:
        """Get quotes learned from users"""
        active_quotes = []
        for quote_data in self.user_quotes:
            if isinstance(quote_data, dict):
                active_quotes.append(quote_data["quote"])
                # Increment usage count
                quote_data["usage_count"] = quote_data.get("usage_count", 0) + 1
            else:
                # Handle old format
                active_quotes.append(quote_data)
        
        # Save updated usage counts
        if active_quotes:
            self.save_json_file(self.user_quotes_file, self.user_quotes)
        
        return active_quotes
    
    def learn_location_preference(self, location: str):
        """Learn user's preferred locations"""
        if "frequent_locations" not in self.location_preferences:
            self.location_preferences["frequent_locations"] = {}
        
        if location not in self.location_preferences["frequent_locations"]:
            self.location_preferences["frequent_locations"][location] = 0
        
        self.location_preferences["frequent_locations"][location] += 1
        self.save_json_file(self.location_preferences_file, self.location_preferences)
    
    def get_frequent_locations(self) -> List[str]:
        """Get user's most frequently requested locations"""
        freq_locs = self.location_preferences.get("frequent_locations", {})
        # Sort by frequency and return top 5
        sorted_locations = sorted(freq_locs.items(), key=lambda x: x[1], reverse=True)
        return [loc[0] for loc in sorted_locations[:5]]
    
    def get_temperature_preference(self) -> str:
        """Get user's preferred temperature unit"""
        return self.user_preferences.get("temperature_unit", "celsius")
    
    def learn_temperature_preference(self, user_input: str):
        """Learn temperature preference from user input"""
        text = user_input.lower()
        if "fahrenheit" in text or "°f" in text or " f" in text:
            self.user_preferences["temperature_unit"] = "fahrenheit"
            self.save_json_file(self.user_preferences_file, self.user_preferences)
        elif "celsius" in text or "°c" in text or " c" in text:
            self.user_preferences["temperature_unit"] = "celsius"
            self.save_json_file(self.user_preferences_file, self.user_preferences)
    
    def get_preferred_forecast_days(self, user_input: str) -> int:
        """Determine preferred forecast length from user input"""
        text = user_input.lower()
        if "tomorrow" in text or "1 day" in text:
            return 1
        elif "week" in text or "7 day" in text:
            return 7
        elif "5 day" in text:
            return 5
        else:
            # Check user's historical preference
            return self.user_preferences.get("preferred_forecast_days", 3)
    
    def learn_quote_preference(self, category: str, user_input: str):
        """Learn user's quote category preferences"""
        if "quote_preferences" not in self.user_preferences:
            self.user_preferences["quote_preferences"] = {}
        
        if category not in self.user_preferences["quote_preferences"]:
            self.user_preferences["quote_preferences"][category] = 0
        
        self.user_preferences["quote_preferences"][category] += 1
        self.save_json_file(self.user_preferences_file, self.user_preferences)
    
    def get_preferred_quote_category(self, user_input: str) -> str:
        """Get user's preferred quote category"""
        quote_prefs = self.user_preferences.get("quote_preferences", {})
        if quote_prefs:
            # Return most frequently requested category
            return max(quote_prefs.items(), key=lambda x: x[1])[0]
        return "mixed"
    
    def get_learned_patterns_for_intent(self, intent: str) -> List[str]:
        """Get learned conversation patterns for a specific intent"""
        return self.conversation_patterns.get(intent, [])
    
    def provide_feedback(self, user_input: str, feedback_type: str, details: str = ""):
        """Learn from user feedback"""
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "feedback_type": feedback_type,  # "positive", "negative", "suggestion"
            "details": details
        }
        
        self.feedback_history.append(feedback)
        
        # Keep only recent feedback (last 100)
        if len(self.feedback_history) > 100:
            self.feedback_history = self.feedback_history[-100:]
        
        self.save_json_file(self.feedback_file, self.feedback_history)
        self.logger.info(f"Received {feedback_type} feedback")

    def learn_intent_pattern(self, user_input: str, intent: str):
        """Learn intent patterns from user interactions"""
        # Use consistent structure with learn_from_interaction
        if intent not in self.conversation_patterns:
            self.conversation_patterns[intent] = []
        
        # Defensive check: ensure it's a list
        if not isinstance(self.conversation_patterns[intent], list):
            self.logger.warning(f"⚠️ conversation_patterns[{intent}] was {type(self.conversation_patterns[intent])}, resetting to list")
            self.conversation_patterns[intent] = []
        
        # Store unique patterns (avoid duplicates)
        user_input_lower = user_input.lower()
        if user_input_lower not in self.conversation_patterns[intent]:
            self.conversation_patterns[intent].append(user_input_lower)
            
            # Keep only recent patterns (max 50 per intent)
            if len(self.conversation_patterns[intent]) > 50:
                self.conversation_patterns[intent] = self.conversation_patterns[intent][-50:]
        
        # Save the updated patterns
        self.save_json_file(self.conversation_patterns_file, self.conversation_patterns)

    def get_learned_intent(self, user_input: str) -> str:
        """Get learned intent for user input"""
        user_input_lower = user_input.lower()
        
        for intent, pattern_data in self.conversation_patterns.items():
            patterns = pattern_data.get("patterns", [])
            for pattern in patterns:
                if pattern in user_input_lower or user_input_lower in pattern:
                    return intent
        
        return None

    def get_learned_patterns(self) -> Dict[str, List[str]]:
        """Get all learned patterns by intent"""
        patterns = {}
        for intent, data in self.conversation_patterns.items():
            patterns[intent] = data.get("patterns", [])
        return patterns

    def track_successful_interaction(self, intent: str):
        """Track successful interactions for learning optimization"""
        if intent not in self.conversation_patterns:
            self.conversation_patterns[intent] = {
                "patterns": [],
                "count": 0,
                "success_rate": 1.0,
                "successful_interactions": 0
            }
        
        pattern_data = self.conversation_patterns[intent]
        
        # Defensive check: ensure pattern_data is a dict
        if not isinstance(pattern_data, dict):
            print(f"⚠️ track_successful_interaction: pattern_data for {intent} was {type(pattern_data)}, resetting")
            pattern_data = {
                "patterns": [],
                "count": 0,
                "success_rate": 1.0,
                "successful_interactions": 0
            }
            self.conversation_patterns[intent] = pattern_data
        
        pattern_data["successful_interactions"] = pattern_data.get("successful_interactions", 0) + 1
        
        # Update success rate
        total_interactions = pattern_data.get("count", 1)
        successful = pattern_data.get("successful_interactions", 1)
        pattern_data["success_rate"] = successful / total_interactions if total_interactions > 0 else 1.0
        
        self.save_json_file(self.conversation_patterns_file, self.conversation_patterns)

    def get_user_preferences(self) -> Dict[str, Any]:
        """Get all user preferences"""
        return {
            "location_preferences": self.location_preferences,
            "temperature_preferences": self.get_temperature_preference(),
            "quote_preferences": self.user_preferences.get("quote_preferences", {}),
            "joke_preferences": self.user_preferences.get("joke_preferences", {}),
            "intent_frequency": self.user_preferences.get("intent_frequency", {})
        }

    def get_learned_content(self, content_type: str) -> List[str]:
        """Get learned content by type"""
        if content_type == "jokes":
            return self.get_learned_jokes()
        elif content_type == "quotes":
            return self.get_learned_quotes()
        else:
            return []

    def learn_decision_optimization(self, intent: str, success_rate: float):
        """Learn decision optimization patterns"""
        if "decision_optimization" not in self.user_preferences:
            self.user_preferences["decision_optimization"] = {}
        
        self.user_preferences["decision_optimization"][intent] = {
            "success_rate": success_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        self.save_json_file(self.user_preferences_file, self.user_preferences)

    def save_data(self):
        """Save all learning data to files"""
        try:
            self.save_json_file(self.user_jokes_file, self.user_jokes)
            self.save_json_file(self.user_quotes_file, self.user_quotes)
            self.save_json_file(self.conversation_patterns_file, self.conversation_patterns)
            self.save_json_file(self.user_preferences_file, self.user_preferences)
            self.save_json_file(self.feedback_file, self.feedback_history)
            self.save_json_file(self.location_preferences_file, self.location_preferences)
            self.logger.info("Learning data saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving learning data: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "learned_jokes": len(self.user_jokes),
            "learned_quotes": len(self.user_quotes),
            "conversation_patterns": sum(len(patterns.get("patterns", [])) for patterns in self.conversation_patterns.values()),
            "feedback_entries": len(self.feedback_history),
            "frequent_locations": len(self.location_preferences.get("frequent_locations", {})),
            "temperature_preference": self.get_temperature_preference(),
            "most_used_intent": max(self.user_preferences.get("intent_frequency", {}).items(), 
                                  key=lambda x: x[1], default=("none", 0))[0],
            "preferred_quote_category": self.get_preferred_quote_category("")
        }

# Global learning system instance
adaptive_learning = AdaptiveLearningSystem()
