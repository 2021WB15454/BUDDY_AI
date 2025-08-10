"""
BUDDY AI Assistant - Core Assistant Module
Advanced AI Assistant with Adaptive Learning and Multi-Modal Capabilities
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .nlp_processor import NLPProcessor
from .decision_engine import DecisionEngine
from .memory_manager import MemoryManager
from .learning_engine import LearningEngine
from skills.skill_manager import SkillManager
from utils.database import DatabaseManager
from utils.adaptive_learning import adaptive_learning

class BuddyAssistant:
    """
    BUDDY AI Assistant - Main coordination class
    
    Features:
    - Advanced NLP processing
    - Intelligent decision making
    - Adaptive learning
    - Memory management
    - Skill-based architecture
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.nlp = None
        self.decision_engine = None
        self.memory = None
        self.learning_engine = None
        self.skill_manager = None
        self.database = None
        
        # State management
        self.is_initialized = False
        self.conversation_context = []
        self.user_preferences = {}
        
    async def initialize(self):
        """Initialize all BUDDY components"""
        try:
            self.logger.info("🔧 Initializing BUDDY AI Assistant...")
            
            # Initialize database
            self.database = DatabaseManager(self.config)
            await self.database.initialize()
            
            # Initialize memory manager
            self.memory = MemoryManager(self.database, self.config)
            await self.memory.initialize()
            
            # Initialize NLP processor
            self.nlp = NLPProcessor(self.config)
            await self.nlp.initialize()
            
            # Initialize learning engine
            self.learning_engine = LearningEngine(self.database, self.config)
            await self.learning_engine.initialize()
            
            # Initialize skill manager
            self.skill_manager = SkillManager(self.config)
            await self.skill_manager.initialize()
            
            # Initialize decision engine
            self.decision_engine = DecisionEngine(
                self.nlp, 
                self.skill_manager, 
                self.memory, 
                self.learning_engine,
                self.config
            )
            await self.decision_engine.initialize()
            
            # Load user preferences
            await self._load_user_preferences()
            
            self.is_initialized = True
            self.logger.info("✅ BUDDY AI Assistant initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize BUDDY: {e}")
            raise
    
    async def process_input(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user input and generate response
        
        Args:
            user_input: Raw user input text
            context: Optional context information
            
        Returns:
            Response dictionary with text, actions, and metadata
        """
        if not self.is_initialized:
            raise RuntimeError("BUDDY not initialized. Call initialize() first.")
        
        # Defensive check: ensure conversation_context is always a list
        if not isinstance(self.conversation_context, list):
            self.logger.warning(f"⚠️ conversation_context was {type(self.conversation_context)}, resetting to list")
            self.conversation_context = []
        
        try:
            # Start processing timer
            start_time = datetime.now()
            self.logger.info(f"🔍 Starting to process input: {user_input}")

            # Ensure context is always a list of dicts
            self.logger.info(f"🔍 Input context type: {type(context)}")
            if context is None:
                context_list = []
            elif isinstance(context, list):
                context_list = context.copy()
            elif isinstance(context, dict):
                context_list = [context]
            else:
                context_list = []
            self.logger.info(f"🔍 Created context_list type: {type(context_list)}")

            # Defensive check: ensure context_list is actually a list
            if not isinstance(context_list, list):
                self.logger.warning(f"⚠️ context_list was {type(context_list)}, resetting to list")
                context_list = []

            # Add current conversation context (ensure all entries are dicts)
            self.logger.info(f"🔍 conversation_context has {len(self.conversation_context)} entries")
            for i, entry in enumerate(self.conversation_context):
                self.logger.info(f"🔍 Processing entry {i}: type={type(entry)}")
                if isinstance(entry, dict):
                    self.logger.info(f"🔍 About to append entry {i} to context_list (type: {type(context_list)})")
                    context_list.append(entry)
                    self.logger.info(f"🔍 Successfully appended entry {i}")
            self.logger.info(f"🔍 Final context_list length: {len(context_list)}")

            # NLP Processing
            self.logger.debug(f"🔍 About to process NLP with context_list type: {type(context_list)}")
            nlp_result = await self.nlp.process(user_input, context_list)
            self.logger.debug(f"✅ NLP processing completed")

            # Store in memory
            self.logger.debug(f"🔍 About to store interaction")
            self.logger.debug(f"🔍 conversation_context type before memory: {type(self.conversation_context)}")
            await self.memory.store_interaction(user_input, nlp_result)
            self.logger.debug(f"✅ Memory storage completed")
            self.logger.debug(f"🔍 conversation_context type after memory: {type(self.conversation_context)}")

            # Decision making
            self.logger.debug(f"🔍 About to process decision with context_list type: {type(context_list)}")
            response = await self.decision_engine.process(nlp_result, context_list)
            self.logger.debug(f"✅ Decision processing completed")
            self.logger.debug(f"🔍 conversation_context type after decision: {type(self.conversation_context)}")

            # Learning from interaction
            self.logger.debug(f"🔍 About to learn from interaction")
            await self.learning_engine.learn_from_interaction(
                user_input, nlp_result, response
            )
            self.logger.debug(f"✅ Learning completed")
            self.logger.debug(f"🔍 conversation_context type after learning: {type(self.conversation_context)}")

            # Add context to conversation (after processing to avoid interference)
            conversation_entry = {
                "timestamp": start_time.isoformat(),
                "user_input": user_input,
                "context": context if isinstance(context, dict) else {},
                "nlp_result": nlp_result,
                "response": response,
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
            
            # Defensive check: ensure conversation_context is still a list
            if self.conversation_context is None:
                self.logger.warning("⚠️ conversation_context became None, resetting to list")
                self.conversation_context = []
            elif not isinstance(self.conversation_context, list):
                self.logger.warning(f"⚠️ conversation_context was {type(self.conversation_context)}, resetting to list")
                self.conversation_context = []
                
            self.conversation_context.append(conversation_entry)
            
            # Maintain context window
            if len(self.conversation_context) > self.config.get("max_context_length", 10):
                self.conversation_context.pop(0)
            
            self.logger.info(f"✅ Processed input in {conversation_entry['processing_time']:.2f}s")
            
            # Learn from this interaction using adaptive learning
            intent = nlp_result.get("intent", "unknown")
            
            # Defensive check: ensure response is a dict
            if not isinstance(response, dict):
                self.logger.warning(f"⚠️ response was {type(response)}, creating default dict")
                response = {"success": False, "response": str(response) if response else "Unknown response"}
                
            response_text = response.get("response", "")
            self.logger.debug(f"🔍 About to call adaptive_learning.learn_from_interaction with: user_input='{user_input}', intent='{intent}', response_text='{response_text}'")
            try:
                adaptive_learning.learn_from_interaction(user_input, intent, response_text)
                self.logger.debug(f"✅ First adaptive_learning.learn_from_interaction completed")
            except Exception as e:
                self.logger.error(f"❌ Error in first adaptive_learning.learn_from_interaction: {e}")
            
            # Enhanced learning integration
            try:
                if response.get("success", False):
                    self.logger.debug(f"🔍 About to call adaptive_learning.track_successful_interaction")
                    adaptive_learning.track_successful_interaction(intent)
                    self.logger.debug(f"✅ track_successful_interaction completed")
            except Exception as e:
                self.logger.error(f"❌ Error in track_successful_interaction: {e}")
            
            # Learn user preferences from this interaction
            try:
                entities = nlp_result.get("entities", {})
                # Defensive check: ensure entities is a dict
                if not isinstance(entities, dict):
                    self.logger.warning(f"⚠️ entities was {type(entities)}, resetting to dict")
                    entities = {}
                    
                if "location" in entities:
                    self.logger.debug(f"🔍 About to learn location preference: {entities['location']}")
                    adaptive_learning.learn_location_preference(entities["location"])
                    self.logger.debug(f"✅ learn_location_preference completed")
                
                if "temperature_units" in entities:
                    # Defensive check: ensure temperature_units is iterable
                    temp_units = entities["temperature_units"]
                    if isinstance(temp_units, (list, tuple)):
                        for unit in temp_units:
                            self.logger.debug(f"🔍 About to learn temperature preference: {unit}")
                            adaptive_learning.learn_temperature_preference(unit)
                            self.logger.debug(f"✅ learn_temperature_preference completed")
                    elif isinstance(temp_units, str):
                        self.logger.debug(f"🔍 About to learn temperature preference (string): {temp_units}")
                        adaptive_learning.learn_temperature_preference(temp_units)
                        self.logger.debug(f"✅ learn_temperature_preference (string) completed")
            except Exception as e:
                self.logger.error(f"❌ Error in user preferences learning: {e}")
            
            self.logger.debug(f"🔍 About to return response: {type(response)}")
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error processing input: {e}")
            return {
                "success": False,
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "error": str(e)
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get BUDDY's current status and capabilities with enhanced learning stats"""
        base_status = {
            "initialized": self.is_initialized,
            "conversation_length": len(self.conversation_context),
            "adaptive_learning_enabled": True
        }
        
        if self.skill_manager:
            base_status["available_skills"] = await self.skill_manager.get_available_skills()
        
        if self.memory:
            memory_stats = await self.memory.get_stats()
            base_status.update(memory_stats)
        
        if self.learning_engine:
            learning_stats = await self.learning_engine.get_stats()
            base_status.update(learning_stats)
        
        # Add comprehensive adaptive learning statistics
        adaptive_stats = adaptive_learning.get_stats()
        base_status.update(adaptive_stats)
        
        return base_status

    async def get_learning_insights(self) -> Dict[str, Any]:
        """Get detailed learning insights"""
        return {
            "user_preferences": adaptive_learning.get_user_preferences(),
            "learned_content": {
                "jokes": adaptive_learning.get_learned_content("jokes"),
                "quotes": adaptive_learning.get_learned_content("quotes")
            },
            "conversation_patterns": adaptive_learning.data.get("conversation_patterns", {}),
            "learning_stats": adaptive_learning.get_stats(),
            "total_interactions": len(self.conversation_context)
        }

    async def provide_feedback(self, user_input: str, feedback_type: str, details: str = ""):
        """Process user feedback for continuous learning"""
        try:
            # Process feedback through adaptive learning
            adaptive_learning.provide_feedback(user_input, feedback_type, details)
            
            # Also process through learning engine if available
            if self.learning_engine:
                await self.learning_engine.provide_feedback(user_input, feedback_type, details)
            
            self.logger.info(f"📝 Processed {feedback_type} feedback")
            return {
                "success": True,
                "message": f"Thank you for the {feedback_type} feedback! I'm learning from it."
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error processing feedback: {e}")
            return {"success": False, "error": str(e)}
    
    async def _load_user_preferences(self):
        """Load user preferences from database"""
        try:
            preferences = await self.database.get_user_preferences()
            self.user_preferences = preferences or {}
            self.logger.info(f"📋 Loaded {len(self.user_preferences)} user preferences")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load user preferences: {e}")
            self.user_preferences = {}
    
    async def update_user_preference(self, key: str, value: Any):
        """Update a user preference"""
        self.user_preferences[key] = value
        await self.database.save_user_preference(key, value)
        self.logger.info(f"💾 Updated user preference: {key}")
    
    async def shutdown(self):
        """Graceful shutdown of BUDDY"""
        self.logger.info("🔄 Shutting down BUDDY AI Assistant...")
        
        if self.database:
            await self.database.close()
        
        self.is_initialized = False
        self.logger.info("👋 BUDDY AI Assistant shutdown complete")
