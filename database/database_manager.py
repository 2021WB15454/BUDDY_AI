"""
Comprehensive Database Manager for BUDDY AI Assistant
Handles user data storage, analytics, and optimization
"""

import sqlite3
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from contextlib import contextmanager
import os

class DatabaseManager:
    """Comprehensive database manager for BUDDY AI Assistant"""
    
    def __init__(self, db_path: str = "database/buddy_ai.db"):
        self.db_path = db_path
        self.setup_logging()
        self.ensure_database_directory()
        self.initialize_database()
    
    def ensure_database_directory(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def setup_logging(self):
        """Setup logging for database operations"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        try:
            yield conn
        finally:
            conn.close()
    
    def initialize_database(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    session_id TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    preferences TEXT DEFAULT '{}',
                    timezone TEXT DEFAULT 'UTC',
                    location TEXT,
                    language TEXT DEFAULT 'en'
                )
            """)
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    intent TEXT,
                    confidence REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    response_time REAL,
                    satisfaction_score INTEGER,
                    feature_used TEXT,
                    context TEXT DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    preference_type TEXT,
                    preference_key TEXT,
                    preference_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, preference_type, preference_key)
                )
            """)
            
            # Feature usage analytics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feature_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    feature_name TEXT,
                    action TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT 1,
                    execution_time REAL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Task management data
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    title TEXT NOT NULL,
                    category TEXT,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'pending',
                    description TEXT,
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    template_used TEXT,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Weather query patterns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    location TEXT,
                    query_type TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accuracy_feedback INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Learning patterns for optimization
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    pattern_type TEXT,
                    pattern_data TEXT,
                    frequency INTEGER DEFAULT 1,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    effectiveness_score REAL DEFAULT 0.5,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # System optimization metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            # User feedback and ratings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    conversation_id INTEGER,
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                    feedback_text TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            conn.commit()
            self.logger.info("Database initialized successfully")
    
    def create_user_session(self, session_id: str = None) -> str:
        """Create or get user session"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        user_id = hashlib.sha256(session_id.encode()).hexdigest()[:16]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO users (id, session_id)
                VALUES (?, ?)
            """, (user_id, session_id))
            
            # Update last active
            cursor.execute("""
                UPDATE users SET last_active = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
        
        return user_id
    
    def log_conversation(self, user_id: str, query: str, response: str, 
                        intent: str = None, confidence: float = None,
                        response_time: float = None, feature_used: str = None,
                        context: Dict = None) -> int:
        """Log conversation for analysis and optimization"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations 
                (user_id, query, response, intent, confidence, response_time, feature_used, context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, query, response, intent, confidence, response_time, 
                  feature_used, json.dumps(context or {})))
            
            conversation_id = cursor.lastrowid
            conn.commit()
            return conversation_id
    
    def track_feature_usage(self, user_id: str, feature_name: str, action: str,
                           success: bool = True, execution_time: float = None,
                           metadata: Dict = None):
        """Track feature usage for optimization"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feature_usage 
                (user_id, feature_name, action, success, execution_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, feature_name, action, success, execution_time,
                  json.dumps(metadata or {})))
            conn.commit()
    
    def save_user_preference(self, user_id: str, preference_type: str,
                           preference_key: str, preference_value: Any):
        """Save user preferences for personalization"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_preferences
                (user_id, preference_type, preference_key, preference_value, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, preference_type, preference_key, str(preference_value)))
            conn.commit()
    
    def get_user_preferences(self, user_id: str, preference_type: str = None) -> Dict:
        """Get user preferences for personalization"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if preference_type:
                cursor.execute("""
                    SELECT preference_key, preference_value
                    FROM user_preferences
                    WHERE user_id = ? AND preference_type = ?
                """, (user_id, preference_type))
            else:
                cursor.execute("""
                    SELECT preference_type, preference_key, preference_value
                    FROM user_preferences
                    WHERE user_id = ?
                """, (user_id,))
            
            rows = cursor.fetchall()
            if preference_type:
                return {row['preference_key']: row['preference_value'] for row in rows}
            else:
                preferences = {}
                for row in rows:
                    if row['preference_type'] not in preferences:
                        preferences[row['preference_type']] = {}
                    preferences[row['preference_type']][row['preference_key']] = row['preference_value']
                return preferences
    
    def save_task(self, user_id: str, title: str, category: str = None,
                  priority: int = 1, description: str = None,
                  due_date: datetime = None, template_used: str = None,
                  metadata: Dict = None) -> int:
        """Save user task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks
                (user_id, title, category, priority, description, due_date, template_used, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, title, category, priority, description, due_date,
                  template_used, json.dumps(metadata or {})))
            
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
    
    def get_user_tasks(self, user_id: str, status: str = None,
                      category: str = None, limit: int = None) -> List[Dict]:
        """Get user tasks with optional filtering"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM tasks WHERE user_id = ?"
            params = [user_id]
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def log_weather_query(self, user_id: str, location: str, query_type: str):
        """Log weather queries for location preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO weather_queries (user_id, location, query_type)
                VALUES (?, ?, ?)
            """, (user_id, location, query_type))
            conn.commit()
    
    def get_user_location_preferences(self, user_id: str) -> List[Tuple[str, int]]:
        """Get user's most queried locations"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT location, COUNT(*) as frequency
                FROM weather_queries
                WHERE user_id = ?
                GROUP BY location
                ORDER BY frequency DESC
                LIMIT 10
            """, (user_id,))
            return [(row['location'], row['frequency']) for row in cursor.fetchall()]
    
    def update_learning_pattern(self, user_id: str, pattern_type: str,
                               pattern_data: Dict, effectiveness_score: float = 0.5):
        """Update learning patterns for AI optimization"""
        pattern_json = json.dumps(pattern_data)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if pattern exists
            cursor.execute("""
                SELECT id, frequency FROM learning_patterns
                WHERE user_id = ? AND pattern_type = ? AND pattern_data = ?
            """, (user_id, pattern_type, pattern_json))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing pattern
                cursor.execute("""
                    UPDATE learning_patterns
                    SET frequency = frequency + 1,
                        last_seen = CURRENT_TIMESTAMP,
                        effectiveness_score = ?
                    WHERE id = ?
                """, (effectiveness_score, existing['id']))
            else:
                # Create new pattern
                cursor.execute("""
                    INSERT INTO learning_patterns
                    (user_id, pattern_type, pattern_data, effectiveness_score)
                    VALUES (?, ?, ?, ?)
                """, (user_id, pattern_type, pattern_json, effectiveness_score))
            
            conn.commit()
    
    def get_optimization_insights(self, user_id: str) -> Dict:
        """Get optimization insights for user"""
        insights = {}
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Most used features
            cursor.execute("""
                SELECT feature_name, COUNT(*) as usage_count,
                       AVG(execution_time) as avg_time
                FROM feature_usage
                WHERE user_id = ?
                GROUP BY feature_name
                ORDER BY usage_count DESC
                LIMIT 5
            """, (user_id,))
            
            insights['top_features'] = [dict(row) for row in cursor.fetchall()]
            
            # Conversation patterns
            cursor.execute("""
                SELECT intent, COUNT(*) as frequency,
                       AVG(confidence) as avg_confidence
                FROM conversations
                WHERE user_id = ? AND intent IS NOT NULL
                GROUP BY intent
                ORDER BY frequency DESC
                LIMIT 5
            """, (user_id,))
            
            insights['conversation_patterns'] = [dict(row) for row in cursor.fetchall()]
            
            # Task categories
            cursor.execute("""
                SELECT category, COUNT(*) as task_count,
                       AVG(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completion_rate
                FROM tasks
                WHERE user_id = ? AND category IS NOT NULL
                GROUP BY category
                ORDER BY task_count DESC
            """, (user_id,))
            
            insights['task_patterns'] = [dict(row) for row in cursor.fetchall()]
            
            # Location preferences
            insights['location_preferences'] = self.get_user_location_preferences(user_id)
            
        return insights
    
    def log_system_metric(self, metric_type: str, metric_value: float, metadata: Dict = None):
        """Log system performance metrics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_metrics (metric_type, metric_value, metadata)
                VALUES (?, ?, ?)
            """, (metric_type, metric_value, json.dumps(metadata or {})))
            conn.commit()
    
    def get_system_performance(self, days: int = 7) -> Dict:
        """Get system performance metrics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get metrics from last N days
            cursor.execute("""
                SELECT metric_type, AVG(metric_value) as avg_value,
                       COUNT(*) as sample_count
                FROM system_metrics
                WHERE timestamp >= datetime('now', '-{} days')
                GROUP BY metric_type
            """.format(days))
            
            metrics = {row['metric_type']: {
                'average': row['avg_value'],
                'samples': row['sample_count']
            } for row in cursor.fetchall()}
            
            return metrics
    
    def save_user_feedback(self, user_id: str, conversation_id: int,
                          rating: int, feedback_text: str = None):
        """Save user feedback for system improvement"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_feedback
                (user_id, conversation_id, rating, feedback_text)
                VALUES (?, ?, ?, ?)
            """, (user_id, conversation_id, rating, feedback_text))
            conn.commit()
    
    def get_analytics_dashboard(self) -> Dict:
        """Get comprehensive analytics for dashboard"""
        analytics = {}
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) as total_users FROM users")
            analytics['total_users'] = cursor.fetchone()['total_users']
            
            # Total conversations
            cursor.execute("SELECT COUNT(*) as total_conversations FROM conversations")
            analytics['total_conversations'] = cursor.fetchone()['total_conversations']
            
            # Active users (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) as active_users
                FROM users
                WHERE last_active >= datetime('now', '-7 days')
            """)
            analytics['active_users_7d'] = cursor.fetchone()['active_users']
            
            # Top features
            cursor.execute("""
                SELECT feature_name, COUNT(*) as usage_count
                FROM feature_usage
                GROUP BY feature_name
                ORDER BY usage_count DESC
                LIMIT 10
            """)
            analytics['top_features'] = [dict(row) for row in cursor.fetchall()]
            
            # Average response time
            cursor.execute("""
                SELECT AVG(response_time) as avg_response_time
                FROM conversations
                WHERE response_time IS NOT NULL
            """)
            result = cursor.fetchone()
            analytics['avg_response_time'] = result['avg_response_time'] if result['avg_response_time'] else 0
            
            # User satisfaction
            cursor.execute("""
                SELECT AVG(rating) as avg_rating, COUNT(*) as total_ratings
                FROM user_feedback
            """)
            feedback = cursor.fetchone()
            analytics['user_satisfaction'] = {
                'average_rating': feedback['avg_rating'] if feedback['avg_rating'] else 0,
                'total_ratings': feedback['total_ratings']
            }
            
        return analytics
    
    def cleanup_old_data(self, days: int = 90):
        """Cleanup old data to maintain performance"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Remove old conversations (keeping recent ones)
            cursor.execute("""
                DELETE FROM conversations
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            
            # Remove old feature usage logs
            cursor.execute("""
                DELETE FROM feature_usage
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            
            # Remove old system metrics
            cursor.execute("""
                DELETE FROM system_metrics
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            
            conn.commit()
            self.logger.info(f"Cleaned up data older than {days} days")

# Singleton instance
_db_manager = None

def get_database_manager() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
