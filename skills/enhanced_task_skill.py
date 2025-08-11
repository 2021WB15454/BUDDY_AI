#!/usr/bin/env python3
"""
Enhanced Task Management Skill with Templates and Categories
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
from pathlib import Path

class TaskTemplate:
    """Template system for different task categories"""
    
    def __init__(self):
        self.templates = {
            "work": {
                "name": "Work Tasks",
                "icon": "💼",
                "fields": ["title", "priority", "deadline", "project", "estimated_hours", "status"],
                "default_values": {
                    "priority": "medium",
                    "status": "pending",
                    "estimated_hours": 2
                },
                "suggestions": [
                    "Complete project proposal",
                    "Attend team meeting",
                    "Review code changes",
                    "Prepare presentation",
                    "Update documentation"
                ]
            },
            "personal": {
                "name": "Personal Tasks",
                "icon": "🏠",
                "fields": ["title", "category", "deadline", "reminder", "notes"],
                "default_values": {
                    "category": "general",
                    "reminder": "1 hour before"
                },
                "suggestions": [
                    "Buy groceries",
                    "Call family member",
                    "Exercise routine",
                    "Read book chapter",
                    "Plan weekend trip"
                ]
            },
            "health": {
                "name": "Health & Fitness",
                "icon": "💪",
                "fields": ["title", "type", "duration", "frequency", "goal", "notes"],
                "default_values": {
                    "type": "exercise",
                    "duration": "30 minutes",
                    "frequency": "daily"
                },
                "suggestions": [
                    "Morning workout",
                    "Doctor appointment",
                    "Take vitamins",
                    "Drink 8 glasses of water",
                    "Meditation session"
                ]
            },
            "learning": {
                "name": "Learning & Education",
                "icon": "📚",
                "fields": ["title", "subject", "difficulty", "deadline", "progress", "resources"],
                "default_values": {
                    "difficulty": "medium",
                    "progress": "0%"
                },
                "suggestions": [
                    "Complete online course",
                    "Read technical article",
                    "Practice coding problem",
                    "Watch tutorial video",
                    "Attend webinar"
                ]
            },
            "finance": {
                "name": "Financial Tasks",
                "icon": "💰",
                "fields": ["title", "amount", "deadline", "category", "priority", "notes"],
                "default_values": {
                    "category": "expense",
                    "priority": "medium"
                },
                "suggestions": [
                    "Pay monthly bills",
                    "Review budget",
                    "Investment research",
                    "Tax preparation",
                    "Insurance renewal"
                ]
            },
            "shopping": {
                "name": "Shopping Lists",
                "icon": "🛒",
                "fields": ["title", "quantity", "category", "budget", "store", "urgent"],
                "default_values": {
                    "quantity": 1,
                    "urgent": False
                },
                "suggestions": [
                    "Buy milk and bread",
                    "Electronics shopping",
                    "Clothing items",
                    "Home supplies",
                    "Gift for friend"
                ]
            },
            "travel": {
                "name": "Travel Planning",
                "icon": "✈️",
                "fields": ["title", "destination", "date", "duration", "budget", "bookings"],
                "default_values": {
                    "duration": "1 day"
                },
                "suggestions": [
                    "Book flight tickets",
                    "Hotel reservation",
                    "Plan itinerary",
                    "Pack luggage",
                    "Travel insurance"
                ]
            }
        }
    
    def get_template(self, category: str) -> Dict[str, Any]:
        """Get template for specific category"""
        return self.templates.get(category.lower(), self.templates["personal"])
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.templates.keys())
    
    def create_task_from_template(self, category: str, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Create a task using template structure"""
        template = self.get_template(category)
        
        task = {
            "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "category": category,
            "template_used": template["name"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed": False
        }
        
        # Apply template defaults
        for field in template["fields"]:
            if field in template["default_values"]:
                task[field] = template["default_values"][field]
        
        # Override with user input
        task.update(user_input)
        
        return task

class EnhancedTaskManager:
    """Enhanced task manager with categories, templates, and learning"""
    
    def __init__(self, data_dir: str = "learning_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.tasks_file = self.data_dir / "tasks_enhanced.json"
        self.patterns_file = self.data_dir / "task_patterns.json"
        self.user_preferences_file = self.data_dir / "task_preferences.json"
        
        self.template_system = TaskTemplate()
        self.tasks = self.load_tasks()
        self.patterns = self.load_patterns()
        self.user_preferences = self.load_user_preferences()
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from file"""
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading tasks: {e}")
        return []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_patterns(self) -> Dict[str, Any]:
        """Load learned patterns from file"""
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading patterns: {e}")
        return {
            "common_categories": {},
            "time_patterns": {},
            "user_vocabulary": {},
            "completion_patterns": {}
        }
    
    def save_patterns(self):
        """Save learned patterns to file"""
        try:
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        try:
            if self.user_preferences_file.exists():
                with open(self.user_preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading user preferences: {e}")
        return {
            "preferred_categories": [],
            "default_priority": "medium",
            "reminder_preferences": "1 hour before",
            "common_deadlines": {}
        }
    
    def save_user_preferences(self):
        """Save user preferences"""
        try:
            with open(self.user_preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user preferences: {e}")
    
    def analyze_user_input(self, text: str) -> Dict[str, Any]:
        """Analyze user input to extract task details and suggest category"""
        text_lower = text.lower()
        
        # Category detection based on keywords
        category_keywords = {
            "work": ["meeting", "project", "deadline", "office", "team", "presentation", "report"],
            "personal": ["family", "home", "personal", "self", "life"],
            "health": ["exercise", "workout", "doctor", "medicine", "health", "fitness", "gym"],
            "learning": ["learn", "study", "course", "book", "tutorial", "practice", "skill"],
            "finance": ["pay", "bill", "money", "budget", "bank", "investment", "tax"],
            "shopping": ["buy", "shop", "purchase", "store", "market", "grocery"],
            "travel": ["travel", "trip", "flight", "hotel", "vacation", "visit"]
        }
        
        suggested_category = "personal"  # default
        confidence = 0
        
        for category, keywords in category_keywords.items():
            category_confidence = sum(1 for keyword in keywords if keyword in text_lower)
            if category_confidence > confidence:
                confidence = category_confidence
                suggested_category = category
        
        # Extract priority keywords
        priority = "medium"
        if any(word in text_lower for word in ["urgent", "asap", "immediate", "critical"]):
            priority = "high"
        elif any(word in text_lower for word in ["low", "someday", "maybe", "when possible"]):
            priority = "low"
        
        # Extract deadline keywords
        deadline = None
        if "today" in text_lower:
            deadline = datetime.now().date().isoformat()
        elif "tomorrow" in text_lower:
            deadline = (datetime.now() + timedelta(days=1)).date().isoformat()
        elif "next week" in text_lower:
            deadline = (datetime.now() + timedelta(weeks=1)).date().isoformat()
        
        return {
            "suggested_category": suggested_category,
            "confidence": confidence,
            "priority": priority,
            "deadline": deadline,
            "original_text": text
        }
    
    def get_template_for_category(self, category: str) -> str:
        """Generate template presentation for user"""
        template = self.template_system.get_template(category)
        
        response = f"📋 **{template['name']} Template** {template['icon']}\n\n"
        response += "Please provide the following information:\n\n"
        
        for field in template['fields']:
            if field in template['default_values']:
                response += f"• **{field.replace('_', ' ').title()}**: (default: {template['default_values'][field]})\n"
            else:
                response += f"• **{field.replace('_', ' ').title()}**: \n"
        
        response += f"\n💡 **Suggestions for {template['name']}:**\n"
        for suggestion in template['suggestions'][:3]:
            response += f"   - {suggestion}\n"
        
        response += f"\n📝 You can say: \"Add {category} task: [your task details]\""
        return response
    
    def create_task(self, category: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task with template"""
        task = self.template_system.create_task_from_template(category, user_data)
        self.tasks.append(task)
        self.save_tasks()
        
        # Learn from this interaction
        self.learn_from_task_creation(task, user_data)
        
        return task
    
    def learn_from_task_creation(self, task: Dict[str, Any], user_data: Dict[str, Any]):
        """Learn patterns from task creation"""
        category = task['category']
        
        # Update common categories
        if category not in self.patterns['common_categories']:
            self.patterns['common_categories'][category] = 0
        self.patterns['common_categories'][category] += 1
        
        # Learn user vocabulary
        if 'title' in user_data:
            words = user_data['title'].lower().split()
            for word in words:
                if word not in self.patterns['user_vocabulary']:
                    self.patterns['user_vocabulary'][word] = []
                if category not in self.patterns['user_vocabulary'][word]:
                    self.patterns['user_vocabulary'][word].append(category)
        
        # Update user preferences
        if category not in self.user_preferences['preferred_categories']:
            self.user_preferences['preferred_categories'].append(category)
        
        self.save_patterns()
        self.save_user_preferences()
    
    def get_tasks_by_category(self, category: str = None) -> List[Dict[str, Any]]:
        """Get tasks by category"""
        if category:
            return [task for task in self.tasks if task.get('category') == category and not task.get('completed', False)]
        return [task for task in self.tasks if not task.get('completed', False)]
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get task statistics for optimization"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.get('completed', False)])
        
        category_stats = {}
        for task in self.tasks:
            category = task.get('category', 'unknown')
            if category not in category_stats:
                category_stats[category] = {'total': 0, 'completed': 0}
            category_stats[category]['total'] += 1
            if task.get('completed', False):
                category_stats[category]['completed'] += 1
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'category_stats': category_stats,
            'most_used_category': max(self.patterns['common_categories'].items(), key=lambda x: x[1])[0] if self.patterns['common_categories'] else 'personal'
        }

class EnhancedTaskSkill:
    """Enhanced Task Management Skill with Templates"""
    
    def __init__(self, config=None):
        self.config = config
        self.task_manager = EnhancedTaskManager()
        
    async def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process task-related queries"""
        query_lower = query.lower()
        
        # Show all categories
        if any(phrase in query_lower for phrase in ["task categories", "categories", "task types", "templates"]):
            return self.show_task_categories()
        
        # Show template for specific category
        if "template for" in query_lower or "template" in query_lower:
            for category in self.task_manager.template_system.get_all_categories():
                if category in query_lower:
                    return self.task_manager.get_template_for_category(category)
            return self.show_task_categories()
        
        # Add task with category
        if "add" in query_lower and "task" in query_lower:
            return await self.add_task_with_template(query)
        
        # Show tasks
        if any(phrase in query_lower for phrase in ["show tasks", "my tasks", "task list", "tasks"]):
            return self.show_tasks(query)
        
        # Task statistics
        if any(phrase in query_lower for phrase in ["task stats", "task statistics", "task summary"]):
            return self.show_task_statistics()
        
        # Default help
        return self.show_task_help()
    
    def show_task_categories(self) -> str:
        """Show all available task categories with templates"""
        categories = self.task_manager.template_system.templates
        
        response = "📋 **Available Task Categories & Templates**\n\n"
        
        for category, template in categories.items():
            response += f"{template['icon']} **{template['name']}** (`{category}`)\n"
            response += f"   Fields: {', '.join(template['fields'])}\n"
            response += f"   Example: \"{template['suggestions'][0]}\"\n\n"
        
        response += "💡 **How to use:**\n"
        response += "• \"Template for work\" - Get work task template\n"
        response += "• \"Add work task: Complete project proposal\" - Create task\n"
        response += "• \"Show work tasks\" - View tasks by category\n"
        
        return response
    
    async def add_task_with_template(self, query: str) -> str:
        """Add task using appropriate template"""
        # Analyze user input
        analysis = self.task_manager.analyze_user_input(query)
        
        # Extract category from query if specified
        category = analysis['suggested_category']
        for cat in self.task_manager.template_system.get_all_categories():
            if cat in query.lower():
                category = cat
                break
        
        # Extract task details from query
        task_text = query
        for phrase in ["add task:", "add", "task:", "create task:"]:
            if phrase in query.lower():
                task_text = query.lower().split(phrase, 1)[-1].strip()
                break
        
        # Create task data
        task_data = {
            'title': task_text,
            'priority': analysis['priority'],
            'deadline': analysis['deadline']
        }
        
        # Create the task
        task = self.task_manager.create_task(category, task_data)
        
        template = self.task_manager.template_system.get_template(category)
        
        response = f"✅ **Task Created Successfully!**\n\n"
        response += f"{template['icon']} **Category**: {template['name']}\n"
        response += f"📝 **Title**: {task['title']}\n"
        response += f"🎯 **Priority**: {task['priority']}\n"
        if task.get('deadline'):
            response += f"📅 **Deadline**: {task['deadline']}\n"
        response += f"🆔 **ID**: {task['id']}\n\n"
        
        response += f"💡 **Suggestion**: Use \"Template for {category}\" to see all available fields for this category."
        
        return response
    
    def show_tasks(self, query: str) -> str:
        """Show tasks with optional category filtering"""
        category = None
        for cat in self.task_manager.template_system.get_all_categories():
            if cat in query.lower():
                category = cat
                break
        
        tasks = self.task_manager.get_tasks_by_category(category)
        
        if not tasks:
            if category:
                return f"📋 No {category} tasks found. Use \"Add {category} task: [description]\" to create one."
            else:
                return "📋 No tasks found. Use \"Task categories\" to see available templates."
        
        response = f"📋 **{'All Tasks' if not category else category.title() + ' Tasks'}**\n\n"
        
        # Group by category if showing all tasks
        if not category:
            category_groups = {}
            for task in tasks:
                task_category = task.get('category', 'unknown')
                if task_category not in category_groups:
                    category_groups[task_category] = []
                category_groups[task_category].append(task)
            
            for cat, cat_tasks in category_groups.items():
                template = self.task_manager.template_system.get_template(cat)
                response += f"{template['icon']} **{template['name']}** ({len(cat_tasks)} tasks)\n"
                for task in cat_tasks[:3]:  # Show max 3 per category
                    response += f"   • {task['title']} [{task.get('priority', 'medium')}]\n"
                if len(cat_tasks) > 3:
                    response += f"   ... and {len(cat_tasks) - 3} more\n"
                response += "\n"
        else:
            # Show detailed view for specific category
            template = self.task_manager.template_system.get_template(category)
            response += f"{template['icon']} **{template['name']}**\n\n"
            
            for i, task in enumerate(tasks[:10], 1):  # Show max 10 tasks
                response += f"**{i}. {task['title']}**\n"
                response += f"   Priority: {task.get('priority', 'medium')} | "
                if task.get('deadline'):
                    response += f"Deadline: {task['deadline']} | "
                response += f"Created: {task['created_at'][:10]}\n\n"
        
        response += f"💡 Use \"Task statistics\" to see completion rates and analytics."
        return response
    
    def show_task_statistics(self) -> str:
        """Show task statistics and analytics"""
        stats = self.task_manager.get_task_statistics()
        
        response = "📊 **Task Analytics & Statistics**\n\n"
        response += f"📈 **Overall Performance**\n"
        response += f"   Total Tasks: {stats['total_tasks']}\n"
        response += f"   Completed: {stats['completed_tasks']}\n"
        response += f"   Completion Rate: {stats['completion_rate']:.1f}%\n\n"
        
        response += f"📋 **Category Breakdown**\n"
        for category, data in stats['category_stats'].items():
            template = self.task_manager.template_system.get_template(category)
            completion_rate = (data['completed'] / data['total'] * 100) if data['total'] > 0 else 0
            response += f"   {template['icon']} {template['name']}: {data['completed']}/{data['total']} ({completion_rate:.1f}%)\n"
        
        response += f"\n🎯 **Most Used Category**: {stats['most_used_category'].title()}\n"
        
        # User preferences
        prefs = self.task_manager.user_preferences
        if prefs['preferred_categories']:
            response += f"❤️ **Your Preferences**: {', '.join(prefs['preferred_categories'])}\n"
        
        return response
    
    def show_task_help(self) -> str:
        """Show task management help"""
        return """📋 **Enhanced Task Management Help**

🎯 **Quick Commands:**
• "Task categories" - See all available templates
• "Template for work" - Get work task template  
• "Add work task: Complete project" - Create categorized task
• "Show personal tasks" - View tasks by category
• "Task statistics" - View analytics and completion rates

📝 **Available Categories:**
💼 Work, 🏠 Personal, 💪 Health, 📚 Learning, 💰 Finance, 🛒 Shopping, ✈️ Travel

🤖 **Smart Features:**
• Automatic category detection
• Template-based task creation
• Learning from your patterns
• Personalized suggestions
• Analytics and optimization

💡 **Examples:**
• "Add health task: Morning workout routine"
• "Show work tasks for this week"
• "Template for learning tasks"
"""

# Export the enhanced task skill
__all__ = ['EnhancedTaskSkill', 'TaskTemplate', 'EnhancedTaskManager']
