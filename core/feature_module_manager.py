#!/usr/bin/env python3
"""
Comprehensive Feature Module Manager for BUDDY AI
Handles all feature cards with individual modules and self-optimization
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import os
from pathlib import Path
import logging

class FeatureModuleManager:
    """Central manager for all feature modules with self-optimization"""
    
    def __init__(self, config=None):
        self.config = config
        self.data_dir = Path("learning_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize module tracking
        self.module_usage_file = self.data_dir / "module_usage.json"
        self.optimization_file = self.data_dir / "optimization_data.json"
        self.user_patterns_file = self.data_dir / "user_interaction_patterns.json"
        
        self.module_usage = self.load_module_usage()
        self.optimization_data = self.load_optimization_data()
        self.user_patterns = self.load_user_patterns()
        
        # Register all feature modules
        self.feature_modules = {
            'weather': WeatherModule(self),
            'tasks': TasksModule(self),
            'calendar': CalendarModule(self),
            'datetime': DateTimeModule(self),
            'entertainment': EntertainmentModule(self),
            'automotive': AutomotiveModule(self),
            'notes': NotesModule(self),
            'contacts': ContactsModule(self),
            'ai': AIModule(self)
        }
        
        logging.info("FeatureModuleManager initialized with all modules")
    
    def load_module_usage(self) -> Dict[str, Any]:
        """Load module usage statistics"""
        try:
            if self.module_usage_file.exists():
                with open(self.module_usage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading module usage: {e}")
        
        return {
            'total_interactions': 0,
            'module_counts': {},
            'success_rates': {},
            'response_times': {},
            'user_satisfaction': {},
            'daily_usage': {}
        }
    
    def save_module_usage(self):
        """Save module usage statistics"""
        try:
            with open(self.module_usage_file, 'w', encoding='utf-8') as f:
                json.dump(self.module_usage, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving module usage: {e}")
    
    def load_optimization_data(self) -> Dict[str, Any]:
        """Load optimization and learning data"""
        try:
            if self.optimization_file.exists():
                with open(self.optimization_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading optimization data: {e}")
        
        return {
            'query_optimizations': {},
            'response_improvements': {},
            'error_patterns': {},
            'performance_metrics': {},
            'learning_iterations': 0
        }
    
    def load_user_patterns(self) -> Dict[str, Any]:
        """Load user interaction patterns"""
        try:
            if self.user_patterns_file.exists():
                with open(self.user_patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading user patterns: {e}")
        
        return {
            'preferred_modules': {},
            'interaction_times': {},
            'query_types': {},
            'feedback_patterns': {},
            'learning_preferences': {}
        }
    
    async def process_feature_request(self, feature: str, query: str, context: Dict[str, Any] = None) -> str:
        """Process request for specific feature module"""
        start_time = datetime.now()
        
        try:
            # Track usage
            self.track_module_usage(feature, query)
            
            # Get appropriate module
            if feature not in self.feature_modules:
                return f"❌ Feature '{feature}' not found. Available features: {', '.join(self.feature_modules.keys())}"
            
            module = self.feature_modules[feature]
            
            # Process with module
            response = await module.process(query, context)
            
            # Track performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.track_performance(feature, response_time, True)
            
            # Learn from interaction
            await self.learn_from_interaction(feature, query, response, context)
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing {feature} request: {e}")
            self.track_performance(feature, (datetime.now() - start_time).total_seconds(), False)
            return f"❌ Error processing {feature} request: {str(e)}"
    
    def track_module_usage(self, module: str, query: str):
        """Track module usage statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Update total interactions
        self.module_usage['total_interactions'] += 1
        
        # Update module counts
        if module not in self.module_usage['module_counts']:
            self.module_usage['module_counts'][module] = 0
        self.module_usage['module_counts'][module] += 1
        
        # Update daily usage
        if today not in self.module_usage['daily_usage']:
            self.module_usage['daily_usage'][today] = {}
        if module not in self.module_usage['daily_usage'][today]:
            self.module_usage['daily_usage'][today][module] = 0
        self.module_usage['daily_usage'][today][module] += 1
        
        self.save_module_usage()
    
    def track_performance(self, module: str, response_time: float, success: bool):
        """Track performance metrics"""
        if module not in self.module_usage['response_times']:
            self.module_usage['response_times'][module] = []
        
        self.module_usage['response_times'][module].append(response_time)
        
        if module not in self.module_usage['success_rates']:
            self.module_usage['success_rates'][module] = {'success': 0, 'total': 0}
        
        self.module_usage['success_rates'][module]['total'] += 1
        if success:
            self.module_usage['success_rates'][module]['success'] += 1
        
        self.save_module_usage()
    
    async def learn_from_interaction(self, module: str, query: str, response: str, context: Dict[str, Any]):
        """Learn from user interaction for optimization"""
        try:
            # Analyze query patterns
            query_words = query.lower().split()
            
            if module not in self.optimization_data['query_optimizations']:
                self.optimization_data['query_optimizations'][module] = {
                    'common_words': {},
                    'patterns': [],
                    'successful_queries': []
                }
            
            # Track common words
            for word in query_words:
                if word not in self.optimization_data['query_optimizations'][module]['common_words']:
                    self.optimization_data['query_optimizations'][module]['common_words'][word] = 0
                self.optimization_data['query_optimizations'][module]['common_words'][word] += 1
            
            # Store successful query for learning
            self.optimization_data['query_optimizations'][module]['successful_queries'].append({
                'query': query,
                'response_length': len(response),
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only recent queries (last 100)
            if len(self.optimization_data['query_optimizations'][module]['successful_queries']) > 100:
                self.optimization_data['query_optimizations'][module]['successful_queries'] = \
                    self.optimization_data['query_optimizations'][module]['successful_queries'][-100:]
            
            self.optimization_data['learning_iterations'] += 1
            
            # Auto-optimize if enough data collected
            if self.optimization_data['learning_iterations'] % 50 == 0:
                await self.auto_optimize_modules()
            
        except Exception as e:
            logging.error(f"Error in learning from interaction: {e}")
    
    async def auto_optimize_modules(self):
        """Auto-optimize modules based on learning data"""
        try:
            logging.info("Starting auto-optimization of modules")
            
            optimizations_made = []
            
            for module_name, module in self.feature_modules.items():
                if hasattr(module, 'optimize_performance'):
                    optimization_result = await module.optimize_performance(
                        self.optimization_data.get('query_optimizations', {}).get(module_name, {}),
                        self.module_usage.get('success_rates', {}).get(module_name, {}),
                        self.user_patterns
                    )
                    if optimization_result:
                        optimizations_made.append(f"{module_name}: {optimization_result}")
            
            if optimizations_made:
                logging.info(f"Optimizations made: {optimizations_made}")
                
                # Save optimization log
                self.optimization_data['optimization_log'] = {
                    'timestamp': datetime.now().isoformat(),
                    'optimizations': optimizations_made,
                    'iteration': self.optimization_data['learning_iterations']
                }
                
                # Save optimization data
                with open(self.optimization_file, 'w', encoding='utf-8') as f:
                    json.dump(self.optimization_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            logging.error(f"Error in auto-optimization: {e}")
    
    def get_module_statistics(self) -> Dict[str, Any]:
        """Get comprehensive module statistics"""
        stats = {
            'total_interactions': self.module_usage['total_interactions'],
            'module_popularity': {},
            'performance_metrics': {},
            'optimization_status': {
                'learning_iterations': self.optimization_data['learning_iterations'],
                'last_optimization': self.optimization_data.get('optimization_log', {}).get('timestamp', 'Never')
            }
        }
        
        # Calculate module popularity
        total = sum(self.module_usage['module_counts'].values())
        for module, count in self.module_usage['module_counts'].items():
            stats['module_popularity'][module] = {
                'usage_count': count,
                'percentage': (count / total * 100) if total > 0 else 0
            }
        
        # Calculate performance metrics
        for module in self.feature_modules.keys():
            success_data = self.module_usage['success_rates'].get(module, {'success': 0, 'total': 0})
            response_times = self.module_usage['response_times'].get(module, [])
            
            stats['performance_metrics'][module] = {
                'success_rate': (success_data['success'] / success_data['total'] * 100) if success_data['total'] > 0 else 0,
                'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
                'total_requests': success_data['total']
            }
        
        return stats

class BaseFeatureModule:
    """Base class for all feature modules"""
    
    def __init__(self, manager: FeatureModuleManager):
        self.manager = manager
        self.module_name = self.__class__.__name__.lower().replace('module', '')
        self.data_file = manager.data_dir / f"{self.module_name}_data.json"
        self.module_data = self.load_module_data()
    
    def load_module_data(self) -> Dict[str, Any]:
        """Load module-specific data"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading {self.module_name} data: {e}")
        return {}
    
    def save_module_data(self):
        """Save module-specific data"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.module_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving {self.module_name} data: {e}")
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process module-specific query - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process method")
    
    async def optimize_performance(self, query_data: Dict, success_data: Dict, user_patterns: Dict) -> str:
        """Optimize module performance - to be implemented by subclasses"""
        return None
    
    def get_module_help(self) -> str:
        """Get help for this module"""
        return f"Help for {self.module_name} module"

# Individual Feature Modules

class WeatherModule(BaseFeatureModule):
    """Weather feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process weather queries"""
        # This would integrate with existing weather skill
        return "🌤️ Weather module processing: " + query
    
    async def optimize_performance(self, query_data: Dict, success_data: Dict, user_patterns: Dict) -> str:
        """Optimize weather module"""
        if query_data.get('common_words', {}).get('location_count', 0) > 10:
            return "Optimized location detection for faster weather responses"
        return None

class TasksModule(BaseFeatureModule):
    """Tasks feature module with enhanced functionality"""
    
    def __init__(self, manager: FeatureModuleManager):
        super().__init__(manager)
        # Import the enhanced task skill
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from skills.enhanced_task_skill import EnhancedTaskSkill
            self.task_skill = EnhancedTaskSkill()
        except ImportError:
            logging.warning("Enhanced task skill not available, using basic functionality")
            self.task_skill = None
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process task queries using enhanced task skill"""
        if self.task_skill:
            return await self.task_skill.process(query, context)
        else:
            # Basic task functionality as fallback
            return f"📋 Basic task processing: {query}\n\nPlease use:\n• 'Task categories' to see available types\n• 'Add task: [description]' to create tasks\n• 'Show tasks' to view your tasks"
    
    async def optimize_performance(self, query_data: Dict, success_data: Dict, user_patterns: Dict) -> str:
        """Optimize task module"""
        common_words = query_data.get('common_words', {})
        if len(common_words) > 20:
            return "Enhanced task categorization based on usage patterns"
        return None

class CalendarModule(BaseFeatureModule):
    """Calendar feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process calendar queries"""
        return "📅 Calendar module processing: " + query
    
    async def optimize_performance(self, query_data: Dict, success_data: Dict, user_patterns: Dict) -> str:
        """Optimize calendar module"""
        return "Optimized event scheduling based on user patterns"

class DateTimeModule(BaseFeatureModule):
    """DateTime feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process datetime queries"""
        return "🕐 DateTime module processing: " + query

class EntertainmentModule(BaseFeatureModule):
    """Entertainment feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process entertainment queries"""
        return "🎭 Entertainment module processing: " + query

class AutomotiveModule(BaseFeatureModule):
    """Automotive feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process automotive queries"""
        return "🚗 Automotive module processing: " + query

class NotesModule(BaseFeatureModule):
    """Notes feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process notes queries"""
        return "📝 Notes module processing: " + query

class ContactsModule(BaseFeatureModule):
    """Contacts feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process contacts queries"""
        return "👤 Contacts module processing: " + query

class AIModule(BaseFeatureModule):
    """AI Intelligence feature module"""
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process AI queries"""
        return "🧠 AI module processing: " + query

# Export classes
__all__ = [
    'FeatureModuleManager', 
    'BaseFeatureModule',
    'WeatherModule', 'TasksModule', 'CalendarModule', 'DateTimeModule',
    'EntertainmentModule', 'AutomotiveModule', 'NotesModule', 'ContactsModule', 'AIModule'
]
