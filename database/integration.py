"""
Database Integration Layer for BUDDY AI Core Components
Integrates database functionality with existing core systems
"""

import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional
from database.database_manager import get_database_manager
from database.user_analytics import get_analytics_engine

class DatabaseIntegration:
    """Integration layer for database functionality"""
    
    def __init__(self):
        self.db = get_database_manager()
        self.analytics = get_analytics_engine()
        self.current_user_id = None
        self.session_id = None
    
    def initialize_user_session(self, session_id: str = None) -> str:
        """Initialize user session and return user ID"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.session_id = session_id
        self.current_user_id = self.db.create_user_session(session_id)
        return self.current_user_id
    
    def track_conversation(self, query: str, response: str, intent: str = None,
                          confidence: float = None, response_time: float = None,
                          feature_used: str = None, context: Dict = None) -> int:
        """Track conversation with performance metrics"""
        if not self.current_user_id:
            self.current_user_id = self.initialize_user_session()
        
        conversation_id = self.db.log_conversation(
            user_id=self.current_user_id,
            query=query,
            response=response,
            intent=intent,
            confidence=confidence,
            response_time=response_time,
            feature_used=feature_used,
            context=context
        )
        
        # Log system performance metric
        if response_time:
            self.db.log_system_metric('response_time', response_time, {
                'feature': feature_used,
                'intent': intent
            })
        
        return conversation_id
    
    def track_feature_usage(self, feature_name: str, action: str, success: bool = True,
                           execution_time: float = None, metadata: Dict = None):
        """Track feature usage with detailed metrics"""
        if not self.current_user_id:
            self.current_user_id = self.initialize_user_session()
        
        self.db.track_feature_usage(
            user_id=self.current_user_id,
            feature_name=feature_name,
            action=action,
            success=success,
            execution_time=execution_time,
            metadata=metadata
        )
        
        # Log system metric
        if execution_time:
            self.db.log_system_metric(f'{feature_name}_execution_time', execution_time)
    
    def save_user_preference(self, preference_type: str, preference_key: str, 
                           preference_value: Any):
        """Save user preference with automatic session management"""
        if not self.current_user_id:
            self.current_user_id = self.initialize_user_session()
        
        self.db.save_user_preference(
            user_id=self.current_user_id,
            preference_type=preference_type,
            preference_key=preference_key,
            preference_value=preference_value
        )
    
    def get_user_preferences(self, preference_type: str = None) -> Dict:
        """Get user preferences with session management"""
        if not self.current_user_id:
            return {}
        
        return self.db.get_user_preferences(self.current_user_id, preference_type)
    
    def save_task_with_analytics(self, title: str, category: str = None,
                               priority: int = 1, description: str = None,
                               due_date: datetime = None, template_used: str = None,
                               metadata: Dict = None) -> int:
        """Save task with analytics tracking"""
        if not self.current_user_id:
            self.current_user_id = self.initialize_user_session()
        
        task_id = self.db.save_task(
            user_id=self.current_user_id,
            title=title,
            category=category,
            priority=priority,
            description=description,
            due_date=due_date,
            template_used=template_used,
            metadata=metadata
        )
        
        # Update learning patterns
        if category and template_used:
            pattern_data = {
                'category': category,
                'template': template_used,
                'priority': priority,
                'has_due_date': due_date is not None
            }
            self.db.update_learning_pattern(
                user_id=self.current_user_id,
                pattern_type='task_creation',
                pattern_data=pattern_data
            )
        
        return task_id
    
    def log_weather_query_with_learning(self, location: str, query_type: str):
        """Log weather query with location learning"""
        if not self.current_user_id:
            self.current_user_id = self.initialize_user_session()
        
        self.db.log_weather_query(self.current_user_id, location, query_type)
        
        # Update location preferences
        self.save_user_preference('weather', 'last_location', location)
        
        # Check if this should become default location
        location_prefs = self.db.get_user_location_preferences(self.current_user_id)
        if location_prefs and location_prefs[0][1] >= 5:  # 5+ queries for same location
            self.save_user_preference('weather', 'default_location', location_prefs[0][0])
    
    def get_personalized_suggestions(self) -> Dict[str, Any]:
        """Get personalized suggestions based on user data"""
        if not self.current_user_id:
            return {'suggestions': [], 'personalizations': {}}
        
        # Get optimization insights
        insights = self.db.get_optimization_insights(self.current_user_id)
        
        # Get detailed analysis
        analysis = self.analytics.analyze_user_behavior(self.current_user_id)
        
        return {
            'insights': insights,
            'analysis': analysis,
            'suggestions': analysis.get('optimization_recommendations', []),
            'personalizations': analysis.get('personalization_data', {})
        }
    
    def optimize_user_experience(self) -> Dict[str, Any]:
        """Generate and apply user experience optimizations"""
        if not self.current_user_id:
            return {}
        
        # Get comprehensive optimization strategy
        optimizations = self.analytics.optimize_for_user(self.current_user_id)
        
        # Apply automatic optimizations
        self._apply_automatic_optimizations(optimizations)
        
        return optimizations
    
    def _apply_automatic_optimizations(self, optimizations: Dict[str, Any]):
        """Apply automatic optimizations based on analysis"""
        
        # Apply interface customizations
        interface_custom = optimizations.get('interface_customization', {})
        
        # Set default queries as preferences
        default_queries = interface_custom.get('default_queries', [])
        for i, query in enumerate(default_queries[:3]):  # Limit to top 3
            self.save_user_preference('interface', f'default_query_{i}', query)
        
        # Set feature priorities
        feature_priority = interface_custom.get('feature_priority', [])
        if feature_priority:
            self.save_user_preference('interface', 'feature_priority', 
                                    ','.join(feature_priority[:5]))
        
        # Apply personalized suggestions as preferences
        suggestions = optimizations.get('personalized_suggestions', [])
        for i, suggestion in enumerate(suggestions[:5]):
            self.save_user_preference('suggestions', f'suggestion_{i}', suggestion)
    
    def save_feedback_with_learning(self, conversation_id: int, rating: int,
                                  feedback_text: str = None):
        """Save feedback and update learning patterns"""
        if not self.current_user_id:
            return
        
        self.db.save_user_feedback(self.current_user_id, conversation_id, rating, feedback_text)
        
        # Update learning effectiveness based on feedback
        if rating >= 4:  # Good feedback
            effectiveness_score = 0.8
        elif rating >= 3:  # Neutral feedback
            effectiveness_score = 0.6
        else:  # Poor feedback
            effectiveness_score = 0.3
        
        # Update recent learning patterns with effectiveness score
        self.db.update_learning_pattern(
            user_id=self.current_user_id,
            pattern_type='feedback_learning',
            pattern_data={'rating': rating, 'conversation_id': conversation_id},
            effectiveness_score=effectiveness_score
        )
    
    def get_dashboard_analytics(self) -> Dict[str, Any]:
        """Get comprehensive dashboard analytics"""
        dashboard_data = self.db.get_analytics_dashboard()
        
        if self.current_user_id:
            # Add user-specific analytics
            user_insights = self.db.get_optimization_insights(self.current_user_id)
            dashboard_data['user_insights'] = user_insights
        
        return dashboard_data
    
    def cleanup_and_optimize_database(self):
        """Perform database maintenance and optimization"""
        # Cleanup old data
        self.db.cleanup_old_data(days=90)
        
        # Log optimization metric
        self.db.log_system_metric('database_cleanup', 1.0, {'timestamp': datetime.now().isoformat()})

# Decorator for automatic performance tracking
def track_performance(feature_name: str, action: str = 'execute'):
    """Decorator to automatically track feature performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error = str(e)
                raise
            finally:
                execution_time = time.time() - start_time
                
                # Get database integration instance
                db_integration = DatabaseIntegration()
                
                metadata = {
                    'function_name': func.__name__,
                    'args_count': len(args),
                    'kwargs_count': len(kwargs)
                }
                
                if error:
                    metadata['error'] = error
                
                db_integration.track_feature_usage(
                    feature_name=feature_name,
                    action=action,
                    success=success,
                    execution_time=execution_time,
                    metadata=metadata
                )
        
        return wrapper
    return decorator

# Singleton instance
_db_integration = None

def get_database_integration() -> DatabaseIntegration:
    """Get singleton database integration instance"""
    global _db_integration
    if _db_integration is None:
        _db_integration = DatabaseIntegration()
    return _db_integration
