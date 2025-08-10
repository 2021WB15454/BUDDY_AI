import logging
from utils.adaptive_learning import adaptive_learning

class LearningEngine:
    def __init__(self, database, config):
        self.database = database
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.adaptive_learning = adaptive_learning

    async def initialize(self):
        self.logger.info("LearningEngine with adaptive learning initialized.")

    async def learn_from_interaction(self, user_input, nlp_result, response):
        """Enhanced learning from user interactions"""
        intent = nlp_result.get("intent", "unknown")
        
        # Use adaptive learning system
        self.adaptive_learning.learn_from_interaction(
            user_input, 
            intent, 
            response.get("response", "")
        )
        
        # Additional ML/pattern learning could go here
        self.logger.debug(f"Learned from interaction: {intent}")

    async def get_stats(self):
        """Get learning statistics"""
        base_stats = {
            "total_interactions": 0,
            "learning_enabled": True
        }
        
        # Merge with adaptive learning stats
        adaptive_stats = self.adaptive_learning.get_stats()
        base_stats.update(adaptive_stats)
        
        return base_stats

    async def get_personalized_response(self, intent, default_responses):
        """Get personalized response using adaptive learning"""
        return self.adaptive_learning.get_personalized_response(intent, default_responses)

    async def learn_user_preference(self, preference_type, value):
        """Learn specific user preferences"""
        if preference_type == "temperature_unit":
            self.adaptive_learning.learn_temperature_preference(value)
        elif preference_type == "location":
            self.adaptive_learning.learn_location_preference(value)
        
        self.logger.info(f"Learned user preference: {preference_type} = {value}")

    async def provide_feedback(self, user_input, feedback_type, details=""):
        """Process user feedback"""
        self.adaptive_learning.provide_feedback(user_input, feedback_type, details)
        self.logger.info(f"Processed {feedback_type} feedback")
class LearningEngine:
    def __init__(self, database, config):
        self.database = database
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        self.logger.info("LearningEngine initialized.")

    async def learn_from_interaction(self, user_input, nlp_result, response):
        # Placeholder for learning logic
        pass

    async def get_stats(self):
        return {"learning": "ok"}
