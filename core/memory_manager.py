import logging
import json
from datetime import datetime, timedelta
from utils.adaptive_learning import adaptive_learning

class MemoryManager:
    def __init__(self, database, config):
        self.database = database
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.recent_interactions = []
        self.max_recent = config.get("max_recent_interactions", 10)
        self.adaptive_learning = adaptive_learning

    async def initialize(self):
        self.logger.info("MemoryManager with adaptive learning initialized.")

    async def store_interaction(self, user_input, nlp_result, response=None):
        """Enhanced interaction storage with adaptive learning"""
        # Defensive check: ensure recent_interactions is always a list
        if not isinstance(self.recent_interactions, list):
            self.logger.warning(f"⚠️ recent_interactions was {type(self.recent_interactions)}, resetting to list")
            self.recent_interactions = []
            
        interaction = {
            "user_input": user_input,
            "response": response or "",
            "timestamp": datetime.now().isoformat(),
            "metadata": nlp_result or {}
        }
        
        self.recent_interactions.append(interaction)
        if len(self.recent_interactions) > self.max_recent:
            self.recent_interactions.pop(0)
        
        # Store in database (await async method)
        await self.database.store_conversation_history(interaction)
        
        # Store in adaptive learning system
        if nlp_result:
            self.adaptive_learning.learn_from_interaction(
                user_input, 
                nlp_result.get("intent", "unknown"), 
                response or ""
            )
        
        self.logger.debug(f"Stored interaction: {user_input[:50]}...")

    async def get_recent_context(self, limit=5):
        """Get recent conversation context"""
        return self.recent_interactions[-limit:] if self.recent_interactions else []

    async def get_conversation_history(self, days=7):
        """Get conversation history from database (await async method)"""
        return await self.database.get_conversation_history(days)

    async def clear_recent_memory(self):
        """Clear recent memory"""
        self.recent_interactions = []
        self.logger.info("Recent memory cleared.")

    async def get_user_preferences(self):
        """Get user preferences from adaptive learning"""
        return self.adaptive_learning.get_user_preferences()

    async def get_learned_content(self, content_type):
        """Get learned content like jokes or quotes"""
        return self.adaptive_learning.get_learned_content(content_type)

    async def get_conversation_patterns(self):
        """Get learned conversation patterns"""
        data = self.adaptive_learning.data
        return data.get("conversation_patterns", {})

    async def remember_location_preference(self, location):
        """Remember user's location preference"""
        self.adaptive_learning.learn_location_preference(location)

    async def remember_temperature_preference(self, unit):
        """Remember user's temperature unit preference"""
        self.adaptive_learning.learn_temperature_preference(unit)

    async def get_stats(self):
        """Get memory and learning statistics"""
        base_stats = {
            "memory": "ok",
            "recent_interactions": len(self.recent_interactions)
        }
        
        # Merge with adaptive learning stats
        adaptive_stats = self.adaptive_learning.get_stats()
        base_stats.update(adaptive_stats)
        
        return base_stats
