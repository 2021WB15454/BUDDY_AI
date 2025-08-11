"""
User Analytics and Optimization Engine
Analyzes user data and provides optimization recommendations
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import numpy as np
from database.database_manager import get_database_manager

class UserAnalytics:
    """Advanced user analytics and optimization engine"""
    
    def __init__(self):
        self.db = get_database_manager()
    
    def analyze_user_behavior(self, user_id: str) -> Dict[str, Any]:
        """Comprehensive user behavior analysis"""
        analysis = {
            'usage_patterns': self._analyze_usage_patterns(user_id),
            'preferences': self._analyze_preferences(user_id),
            'performance_metrics': self._analyze_performance(user_id),
            'optimization_recommendations': self._generate_recommendations(user_id),
            'personalization_data': self._get_personalization_data(user_id)
        }
        return analysis
    
    def _analyze_usage_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's usage patterns"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Time-based patterns
            cursor.execute("""
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                FROM conversations
                WHERE user_id = ?
                GROUP BY hour
                ORDER BY hour
            """, (user_id,))
            
            hourly_usage = {row['hour']: row['count'] for row in cursor.fetchall()}
            
            # Day-based patterns
            cursor.execute("""
                SELECT strftime('%w', timestamp) as day_of_week, COUNT(*) as count
                FROM conversations
                WHERE user_id = ?
                GROUP BY day_of_week
                ORDER BY day_of_week
            """, (user_id,))
            
            daily_usage = {row['day_of_week']: row['count'] for row in cursor.fetchall()}
            
            # Feature usage frequency
            cursor.execute("""
                SELECT feature_used, COUNT(*) as frequency
                FROM conversations
                WHERE user_id = ? AND feature_used IS NOT NULL
                GROUP BY feature_used
                ORDER BY frequency DESC
            """, (user_id,))
            
            feature_frequency = {row['feature_used']: row['frequency'] for row in cursor.fetchall()}
            
            # Query length analysis
            cursor.execute("""
                SELECT LENGTH(query) as query_length, COUNT(*) as count
                FROM conversations
                WHERE user_id = ?
                GROUP BY LENGTH(query)
                ORDER BY query_length
            """, (user_id,))
            
            query_lengths = [row['query_length'] for row in cursor.fetchall()]
            avg_query_length = np.mean(query_lengths) if query_lengths else 0
            
            return {
                'hourly_usage': hourly_usage,
                'daily_usage': daily_usage,
                'feature_frequency': feature_frequency,
                'avg_query_length': avg_query_length,
                'peak_usage_hour': max(hourly_usage, key=hourly_usage.get) if hourly_usage else None,
                'most_active_day': max(daily_usage, key=daily_usage.get) if daily_usage else None,
                'primary_feature': max(feature_frequency, key=feature_frequency.get) if feature_frequency else None
            }
    
    def _analyze_preferences(self, user_id: str) -> Dict[str, Any]:
        """Analyze user preferences and interests"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Weather location preferences
            cursor.execute("""
                SELECT location, COUNT(*) as frequency
                FROM weather_queries
                WHERE user_id = ?
                GROUP BY location
                ORDER BY frequency DESC
                LIMIT 5
            """, (user_id,))
            
            weather_locations = [dict(row) for row in cursor.fetchall()]
            
            # Task categories preferences
            cursor.execute("""
                SELECT category, COUNT(*) as frequency,
                       template_used, COUNT(template_used) as template_frequency
                FROM tasks
                WHERE user_id = ? AND category IS NOT NULL
                GROUP BY category, template_used
                ORDER BY frequency DESC
            """, (user_id,))
            
            task_preferences = [dict(row) for row in cursor.fetchall()]
            
            # Intent preferences
            cursor.execute("""
                SELECT intent, COUNT(*) as frequency,
                       AVG(confidence) as avg_confidence
                FROM conversations
                WHERE user_id = ? AND intent IS NOT NULL
                GROUP BY intent
                ORDER BY frequency DESC
            """, (user_id,))
            
            intent_preferences = [dict(row) for row in cursor.fetchall()]
            
            # Response satisfaction patterns
            cursor.execute("""
                SELECT c.intent, AVG(f.rating) as avg_rating, COUNT(f.rating) as rating_count
                FROM conversations c
                LEFT JOIN user_feedback f ON c.id = f.conversation_id
                WHERE c.user_id = ? AND f.rating IS NOT NULL
                GROUP BY c.intent
                ORDER BY avg_rating DESC
            """, (user_id,))
            
            satisfaction_by_intent = [dict(row) for row in cursor.fetchall()]
            
            return {
                'weather_locations': weather_locations,
                'task_preferences': task_preferences,
                'intent_preferences': intent_preferences,
                'satisfaction_by_intent': satisfaction_by_intent,
                'preferred_location': weather_locations[0]['location'] if weather_locations else None,
                'preferred_task_category': task_preferences[0]['category'] if task_preferences else None
            }
    
    def _analyze_performance(self, user_id: str) -> Dict[str, Any]:
        """Analyze system performance for this user"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Response time analysis
            cursor.execute("""
                SELECT AVG(response_time) as avg_response_time,
                       MIN(response_time) as min_response_time,
                       MAX(response_time) as max_response_time,
                       COUNT(*) as total_queries
                FROM conversations
                WHERE user_id = ? AND response_time IS NOT NULL
            """, (user_id,))
            
            response_times = dict(cursor.fetchone())
            
            # Success rate by feature
            cursor.execute("""
                SELECT feature_name,
                       AVG(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) as success_rate,
                       COUNT(*) as total_attempts
                FROM feature_usage
                WHERE user_id = ?
                GROUP BY feature_name
                ORDER BY success_rate DESC
            """, (user_id,))
            
            feature_success_rates = [dict(row) for row in cursor.fetchall()]
            
            # User satisfaction trends
            cursor.execute("""
                SELECT DATE(f.timestamp) as date, AVG(f.rating) as avg_rating
                FROM user_feedback f
                WHERE f.user_id = ?
                GROUP BY DATE(f.timestamp)
                ORDER BY date DESC
                LIMIT 30
            """, (user_id,))
            
            satisfaction_trends = [dict(row) for row in cursor.fetchall()]
            
            return {
                'response_times': response_times,
                'feature_success_rates': feature_success_rates,
                'satisfaction_trends': satisfaction_trends,
                'overall_success_rate': np.mean([f['success_rate'] for f in feature_success_rates]) if feature_success_rates else 0
            }
    
    def _generate_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Generate optimization recommendations for user"""
        recommendations = []
        
        usage_patterns = self._analyze_usage_patterns(user_id)
        preferences = self._analyze_preferences(user_id)
        performance = self._analyze_performance(user_id)
        
        # Time-based recommendations
        if usage_patterns.get('peak_usage_hour'):
            hour = int(usage_patterns['peak_usage_hour'])
            if 6 <= hour <= 12:
                time_period = "morning"
            elif 12 <= hour <= 18:
                time_period = "afternoon"
            else:
                time_period = "evening"
            
            recommendations.append({
                'type': 'time_optimization',
                'priority': 'medium',
                'message': f"You're most active in the {time_period}. Consider setting up automated reminders during this time.",
                'action': 'setup_reminders',
                'data': {'peak_hour': hour, 'time_period': time_period}
            })
        
        # Feature recommendations
        if usage_patterns.get('primary_feature'):
            primary_feature = usage_patterns['primary_feature']
            recommendations.append({
                'type': 'feature_optimization',
                'priority': 'high',
                'message': f"You frequently use {primary_feature}. Consider exploring advanced features in this area.",
                'action': 'suggest_advanced_features',
                'data': {'feature': primary_feature}
            })
        
        # Location-based recommendations
        if preferences.get('preferred_location'):
            location = preferences['preferred_location']
            recommendations.append({
                'type': 'location_optimization',
                'priority': 'medium',
                'message': f"Setting {location} as your default location for faster weather updates.",
                'action': 'set_default_location',
                'data': {'location': location}
            })
        
        # Performance recommendations
        if performance.get('response_times', {}).get('avg_response_time', 0) > 2.0:
            recommendations.append({
                'type': 'performance_optimization',
                'priority': 'high',
                'message': "Response times can be improved. Consider using shorter, more specific queries.",
                'action': 'optimize_queries',
                'data': {'avg_response_time': performance['response_times']['avg_response_time']}
            })
        
        # Task management recommendations
        if preferences.get('preferred_task_category'):
            category = preferences['preferred_task_category']
            recommendations.append({
                'type': 'task_optimization',
                'priority': 'medium',
                'message': f"Create custom templates for your frequent {category} tasks to save time.",
                'action': 'create_custom_template',
                'data': {'category': category}
            })
        
        return recommendations
    
    def _get_personalization_data(self, user_id: str) -> Dict[str, Any]:
        """Get data for personalizing user experience"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get all user preferences
            cursor.execute("""
                SELECT preference_type, preference_key, preference_value
                FROM user_preferences
                WHERE user_id = ?
            """, (user_id,))
            
            preferences = defaultdict(dict)
            for row in cursor.fetchall():
                preferences[row['preference_type']][row['preference_key']] = row['preference_value']
            
            # Get recent learning patterns
            cursor.execute("""
                SELECT pattern_type, pattern_data, effectiveness_score
                FROM learning_patterns
                WHERE user_id = ?
                ORDER BY last_seen DESC
                LIMIT 20
            """, (user_id,))
            
            learning_patterns = []
            for row in cursor.fetchall():
                try:
                    pattern_data = json.loads(row['pattern_data'])
                    learning_patterns.append({
                        'type': row['pattern_type'],
                        'data': pattern_data,
                        'effectiveness': row['effectiveness_score']
                    })
                except json.JSONDecodeError:
                    continue
            
            return {
                'preferences': dict(preferences),
                'learning_patterns': learning_patterns
            }
    
    def optimize_for_user(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive optimization strategy for user"""
        analysis = self.analyze_user_behavior(user_id)
        
        # Apply optimizations based on analysis
        optimizations = {
            'personalized_suggestions': self._generate_personalized_suggestions(analysis),
            'interface_customization': self._generate_interface_customization(analysis),
            'workflow_optimization': self._generate_workflow_optimization(analysis),
            'performance_tuning': self._generate_performance_tuning(analysis)
        }
        
        # Update learning patterns
        self._update_optimization_patterns(user_id, analysis, optimizations)
        
        return optimizations
    
    def _generate_personalized_suggestions(self, analysis: Dict) -> List[str]:
        """Generate personalized suggestions based on analysis"""
        suggestions = []
        
        usage_patterns = analysis['usage_patterns']
        preferences = analysis['preferences']
        
        # Time-based suggestions
        if usage_patterns.get('peak_usage_hour'):
            suggestions.append(f"Set up daily reminders at {usage_patterns['peak_usage_hour']}:00")
        
        # Feature suggestions
        if usage_patterns.get('primary_feature') == 'weather':
            suggestions.append("Enable weather alerts for your favorite locations")
        elif usage_patterns.get('primary_feature') == 'tasks':
            suggestions.append("Try using task templates to speed up task creation")
        
        # Location suggestions
        if preferences.get('preferred_location'):
            suggestions.append(f"Set {preferences['preferred_location']} as your default weather location")
        
        return suggestions
    
    def _generate_interface_customization(self, analysis: Dict) -> Dict[str, Any]:
        """Generate interface customization recommendations"""
        customization = {
            'quick_actions': [],
            'default_queries': [],
            'feature_priority': []
        }
        
        usage_patterns = analysis['usage_patterns']
        preferences = analysis['preferences']
        
        # Prioritize features based on usage
        feature_freq = usage_patterns.get('feature_frequency', {})
        customization['feature_priority'] = sorted(feature_freq.keys(), 
                                                 key=lambda x: feature_freq[x], 
                                                 reverse=True)
        
        # Default queries based on preferences
        if preferences.get('preferred_location'):
            customization['default_queries'].append(f"Weather in {preferences['preferred_location']}")
        
        if preferences.get('preferred_task_category'):
            customization['default_queries'].append(f"Show {preferences['preferred_task_category']} tasks")
        
        return customization
    
    def _generate_workflow_optimization(self, analysis: Dict) -> Dict[str, Any]:
        """Generate workflow optimization recommendations"""
        workflow = {
            'automation_opportunities': [],
            'shortcut_suggestions': [],
            'template_recommendations': []
        }
        
        preferences = analysis['preferences']
        
        # Template recommendations
        if preferences.get('task_preferences'):
            for task_pref in preferences['task_preferences'][:3]:
                workflow['template_recommendations'].append({
                    'category': task_pref['category'],
                    'frequency': task_pref['frequency'],
                    'suggested_template': task_pref.get('template_used', 'custom')
                })
        
        return workflow
    
    def _generate_performance_tuning(self, analysis: Dict) -> Dict[str, Any]:
        """Generate performance tuning recommendations"""
        tuning = {
            'cache_optimizations': [],
            'response_improvements': [],
            'efficiency_gains': []
        }
        
        performance = analysis['performance_metrics']
        
        # Response time optimizations
        if performance.get('response_times', {}).get('avg_response_time', 0) > 1.5:
            tuning['response_improvements'].append("Implement query caching for frequent requests")
            tuning['response_improvements'].append("Optimize database queries for user patterns")
        
        return tuning
    
    def _update_optimization_patterns(self, user_id: str, analysis: Dict, optimizations: Dict):
        """Update learning patterns based on optimization results"""
        
        # Store successful optimization patterns
        pattern_data = {
            'analysis_summary': {
                'primary_feature': analysis['usage_patterns'].get('primary_feature'),
                'preferred_location': analysis['preferences'].get('preferred_location'),
                'avg_response_time': analysis['performance_metrics'].get('response_times', {}).get('avg_response_time')
            },
            'optimizations_applied': list(optimizations.keys())
        }
        
        self.db.update_learning_pattern(
            user_id=user_id,
            pattern_type='optimization_strategy',
            pattern_data=pattern_data,
            effectiveness_score=0.7  # Initial score, will be updated based on feedback
        )

# Singleton instance
_analytics_engine = None

def get_analytics_engine() -> UserAnalytics:
    """Get singleton analytics engine instance"""
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = UserAnalytics()
    return _analytics_engine
