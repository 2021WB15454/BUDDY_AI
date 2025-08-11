"""
Enhanced BUDDY AI Assistant with Database Integration
Comprehensive AI assistant with user data tracking and optimization
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from core.nlp_processor import NLPProcessor
from core.decision_engine import DecisionEngine
from core.memory_manager import MemoryManager
from core.learning_engine import LearningEngine
from skills.skill_manager import SkillManager
from utils.config import Config
from database.integration import get_database_integration, track_performance

class EnhancedBuddyAssistant:
    """Enhanced BUDDY AI Assistant with comprehensive database integration"""
    
    def __init__(self, config: Config = None):
        # Initialize configuration
        self.config = config or Config()
        
        # Initialize database integration
        self.db_integration = get_database_integration()
        self.session_id = None
        self.user_id = None
        
        # Initialize core components
        self.nlp = NLPProcessor(self.config)
        self.skill_manager = SkillManager(self.config)
        self.memory = MemoryManager()
        self.learning_engine = LearningEngine()
        
        # Initialize decision engine with enhanced capabilities
        self.decision_engine = DecisionEngine(
            self.nlp, self.skill_manager, self.memory, self.learning_engine, self.config
        )
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize user session
        self._initialize_session()
        
        # Load user optimizations
        self._load_user_optimizations()
    
    def _initialize_session(self):
        """Initialize user session with database"""
        self.user_id = self.db_integration.initialize_user_session()
        self.logger.info(f"Initialized session for user: {self.user_id}")
    
    def _load_user_optimizations(self):
        """Load user-specific optimizations"""
        try:
            # Get personalized suggestions
            personalization_data = self.db_integration.get_personalized_suggestions()
            
            # Apply optimizations to components
            if personalization_data.get('personalizations'):
                self._apply_personalizations(personalization_data['personalizations'])
            
        except Exception as e:
            self.logger.warning(f"Could not load user optimizations: {e}")
    
    def _apply_personalizations(self, personalizations: Dict):
        """Apply personalization data to system components"""
        preferences = personalizations.get('preferences', {})
        
        # Apply weather preferences
        if 'weather' in preferences:
            weather_prefs = preferences['weather']
            if 'default_location' in weather_prefs:
                self.memory.store_data('user_default_location', weather_prefs['default_location'])
        
        # Apply interface preferences
        if 'interface' in preferences:
            interface_prefs = preferences['interface']
            self.memory.store_data('user_interface_prefs', interface_prefs)
        
        # Apply learning patterns
        learning_patterns = personalizations.get('learning_patterns', [])
        for pattern in learning_patterns:
            if pattern['effectiveness'] > 0.7:  # Only apply effective patterns
                self.learning_engine.add_pattern(pattern['type'], pattern['data'])
    
    @track_performance('conversation', 'process_input')
    async def process_input(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Process user input with database tracking and optimization"""
        start_time = time.time()
        
        try:
            # Preprocess input with NLP
            processed_input = await self.nlp.process(user_input)
            
            # Detect intent and confidence
            intent, confidence = self.decision_engine.detect_intent(user_input)
            
            # Get response from decision engine
            response = await self.decision_engine.get_response(user_input, context)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Determine which feature was used
            feature_used = self._determine_feature_used(intent, response)
            
            # Track conversation in database
            conversation_id = self.db_integration.track_conversation(
                query=user_input,
                response=response,
                intent=intent,
                confidence=confidence,
                response_time=response_time,
                feature_used=feature_used,
                context=context or {}
            )
            
            # Update learning patterns
            self._update_learning_patterns(user_input, response, intent, confidence)
            
            # Log specific feature usage
            if feature_used:
                self._log_feature_specific_data(feature_used, user_input, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            
            # Track error in database
            self.db_integration.track_conversation(
                query=user_input,
                response=f"Error: {str(e)}",
                intent="error",
                confidence=0.0,
                response_time=time.time() - start_time,
                context={'error': True, 'error_message': str(e)}
            )
            
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def _determine_feature_used(self, intent: str, response: str) -> str:
        """Determine which feature was primarily used"""
        # Map intents to features
        intent_feature_map = {
            'weather': 'weather',
            'forecast': 'weather',
            'task_management': 'tasks',
            'calendar': 'calendar',
            'datetime': 'datetime',
            'joke': 'entertainment',
            'quote': 'entertainment',
            'automotive': 'automotive',
            'notes_management': 'notes',
            'contact_management': 'contacts',
            'personal_assistant': 'ai'
        }
        
        return intent_feature_map.get(intent, 'general')
    
    def _log_feature_specific_data(self, feature: str, query: str, response: str):
        """Log feature-specific data for optimization"""
        
        if feature == 'weather':
            # Extract location from weather queries
            location = self._extract_location_from_query(query)
            if location:
                self.db_integration.log_weather_query_with_learning(location, 'current')
        
        elif feature == 'tasks':
            # Extract task category and template usage
            category = self._extract_task_category(query)
            if category:
                self.db_integration.save_user_preference('tasks', 'preferred_category', category)
        
        # Track successful feature usage
        self.db_integration.track_feature_usage(
            feature_name=feature,
            action='query_processed',
            success=True,
            metadata={'query_length': len(query), 'response_length': len(response)}
        )
    
    def _extract_location_from_query(self, query: str) -> Optional[str]:
        """Extract location from weather query"""
        query_lower = query.lower()
        
        # Common location patterns
        location_patterns = [
            'weather in ',
            'temperature in ',
            'forecast for ',
            'climate in '
        ]
        
        for pattern in location_patterns:
            if pattern in query_lower:
                location_start = query_lower.find(pattern) + len(pattern)
                location_part = query[location_start:].strip()
                
                # Extract first word/phrase as location
                location = location_part.split()[0] if location_part.split() else None
                return location.title() if location else None
        
        return None
    
    def _extract_task_category(self, query: str) -> Optional[str]:
        """Extract task category from query"""
        query_lower = query.lower()
        
        categories = ['work', 'personal', 'health', 'learning', 'finance', 'shopping', 'travel']
        
        for category in categories:
            if category in query_lower:
                return category
        
        return None
    
    def _update_learning_patterns(self, query: str, response: str, intent: str, confidence: float):
        """Update learning patterns based on interaction"""
        
        # Query pattern learning
        query_pattern = {
            'length': len(query),
            'words': len(query.split()),
            'intent': intent,
            'confidence': confidence
        }
        
        self.db_integration.db.update_learning_pattern(
            user_id=self.user_id,
            pattern_type='query_pattern',
            pattern_data=query_pattern,
            effectiveness_score=confidence
        )
        
        # Response pattern learning
        response_pattern = {
            'length': len(response),
            'intent': intent,
            'successful': confidence > 0.7
        }
        
        self.db_integration.db.update_learning_pattern(
            user_id=self.user_id,
            pattern_type='response_pattern',
            pattern_data=response_pattern,
            effectiveness_score=0.8 if confidence > 0.7 else 0.4
        )
    
    @track_performance('optimization', 'optimize_user_experience')
    def optimize_user_experience(self) -> Dict[str, Any]:
        """Optimize user experience based on collected data"""
        return self.db_integration.optimize_user_experience()
    
    def save_user_feedback(self, conversation_id: int, rating: int, feedback_text: str = None):
        """Save user feedback for system improvement"""
        self.db_integration.save_feedback_with_learning(conversation_id, rating, feedback_text)
    
    def get_user_insights(self) -> Dict[str, Any]:
        """Get user insights and analytics"""
        return self.db_integration.get_personalized_suggestions()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard analytics data"""
        return self.db_integration.get_dashboard_analytics()
    
    async def adaptive_learning(self):
        """Perform adaptive learning based on user data"""
        try:
            # Get user behavior analysis
            insights = self.get_user_insights()
            
            # Apply optimizations
            optimizations = self.optimize_user_experience()
            
            # Update system components with new insights
            if optimizations.get('performance_tuning'):
                await self._apply_performance_tuning(optimizations['performance_tuning'])
            
            self.logger.info("Adaptive learning completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in adaptive learning: {e}")
    
    async def _apply_performance_tuning(self, tuning_data: Dict):
        """Apply performance tuning recommendations"""
        
        # Implement caching optimizations
        cache_opts = tuning_data.get('cache_optimizations', [])
        for opt in cache_opts:
            self.memory.optimize_cache(opt)
        
        # Implement response improvements
        response_improvements = tuning_data.get('response_improvements', [])
        for improvement in response_improvements:
            if hasattr(self.decision_engine, 'optimize_response_generation'):
                await self.decision_engine.optimize_response_generation(improvement)
    
    def cleanup_session(self):
        """Cleanup session and perform maintenance"""
        try:
            # Perform database cleanup and optimization
            self.db_integration.cleanup_and_optimize_database()
            
            self.logger.info("Session cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during session cleanup: {e}")
    
    def __del__(self):
        """Cleanup when assistant is destroyed"""
        try:
            self.cleanup_session()
        except:
            pass  # Ignore cleanup errors during destruction

# Wrapper for existing core assistant
class DatabaseEnabledAssistant:
    """Wrapper to add database functionality to existing assistant"""
    
    def __init__(self, original_assistant):
        self.assistant = original_assistant
        self.db_integration = get_database_integration()
        self.user_id = self.db_integration.initialize_user_session()
    
    async def process_input(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Enhanced process input with database tracking"""
        start_time = time.time()
        
        try:
            # Call original assistant
            response = await self.assistant.process_input(user_input, context)
            
            # Track in database
            response_time = time.time() - start_time
            self.db_integration.track_conversation(
                query=user_input,
                response=response,
                response_time=response_time,
                context=context or {}
            )
            
            return response
            
        except Exception as e:
            # Track error
            self.db_integration.track_conversation(
                query=user_input,
                response=f"Error: {str(e)}",
                response_time=time.time() - start_time,
                context={'error': True}
            )
            raise
