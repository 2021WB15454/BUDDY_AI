"""
Task Management Module for BUDDY AI Assistant
Handles to-do lists, reminders, task scheduling, and productivity features
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str
    priority: str  # high, medium, low
    status: str    # pending, in_progress, completed, cancelled
    due_date: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None
    category: str = "general"
    tags: List[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []


class TaskManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks_file = "learning_data/tasks.json"
        self.tasks = self._load_tasks()
        self.logger.info("TaskManager initialized.")
    
    def _load_tasks(self) -> List[Task]:
        """Load tasks from file"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_tasks(self):
        """Save tasks to file"""
        try:
            import os
            os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                tasks_data = [asdict(task) for task in self.tasks]
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving tasks: {e}")
    
    async def add_task(self, title: str, description: str = "", priority: str = "medium", 
                      due_date: str = None, category: str = "general", tags: List[str] = None) -> str:
        """Add a new task"""
        task = Task(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            priority=priority.lower(),
            status="pending",
            due_date=due_date,
            category=category,
            tags=tags or []
        )
        
        self.tasks.append(task)
        self._save_tasks()
        
        self.logger.info(f"Task added: {title}")
        return task.id
    
    async def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        for task in self.tasks:
            if task.id == task_id or task.title.lower() == task_id.lower():
                task.status = "completed"
                task.completed_at = datetime.now().isoformat()
                self._save_tasks()
                self.logger.info(f"Task completed: {task.title}")
                return True
        return False
    
    async def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id or task.title.lower() == task_id.lower():
                deleted_task = self.tasks.pop(i)
                self._save_tasks()
                self.logger.info(f"Task deleted: {deleted_task.title}")
                return True
        return False
    
    async def get_tasks(self, status: str = None, category: str = None, priority: str = None) -> List[Task]:
        """Get tasks with optional filters"""
        filtered_tasks = self.tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status.lower()]
        if category:
            filtered_tasks = [t for t in filtered_tasks if t.category == category.lower()]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority.lower()]
        
        return filtered_tasks
    
    async def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due in the next N days"""
        upcoming = []
        cutoff_date = datetime.now() + timedelta(days=days)
        
        for task in self.tasks:
            if task.due_date and task.status != "completed":
                try:
                    due_date = datetime.fromisoformat(task.due_date)
                    if due_date <= cutoff_date:
                        upcoming.append(task)
                except ValueError:
                    continue
        
        return sorted(upcoming, key=lambda t: t.due_date)
    
    async def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title, description, or tags"""
        query = query.lower()
        results = []
        
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower() or 
                any(query in tag.lower() for tag in task.tags)):
                results.append(task)
        
        return results
    
    def get_task_stats(self) -> Dict[str, Any]:
        """Get task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.status == "completed"])
        pending = len([t for t in self.tasks if t.status == "pending"])
        in_progress = len([t for t in self.tasks if t.status == "in_progress"])
        
        by_priority = {
            "high": len([t for t in self.tasks if t.priority == "high" and t.status != "completed"]),
            "medium": len([t for t in self.tasks if t.priority == "medium" and t.status != "completed"]),
            "low": len([t for t in self.tasks if t.priority == "low" and t.status != "completed"])
        }
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
            "by_priority": by_priority
        }


class TaskSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.task_manager = TaskManager()
        self.logger.info("TaskSkill initialized.")
    
    async def handle_task_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle task management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Add task
            if any(keyword in query_lower for keyword in ["add task", "create task", "new task", "add to do", "create todo"]):
                return await self._handle_add_task(user_input, context)
            
            # Complete task
            elif any(keyword in query_lower for keyword in ["complete task", "finish task", "mark done", "task done"]):
                return await self._handle_complete_task(user_input, context)
            
            # Delete task
            elif any(keyword in query_lower for keyword in ["delete task", "remove task", "cancel task"]):
                return await self._handle_delete_task(user_input, context)
            
            # List tasks
            elif any(keyword in query_lower for keyword in ["show tasks", "list tasks", "my tasks", "todo list", "task list"]):
                return await self._handle_list_tasks(user_input, context)
            
            # Task statistics
            elif any(keyword in query_lower for keyword in ["task stats", "task statistics", "productivity stats"]):
                return await self._handle_task_stats()
            
            # Upcoming tasks
            elif any(keyword in query_lower for keyword in ["upcoming tasks", "due tasks", "deadlines"]):
                return await self._handle_upcoming_tasks()
            
            # Search tasks
            elif any(keyword in query_lower for keyword in ["find task", "search task", "look for task"]):
                return await self._handle_search_tasks(user_input, context)
            
            # Default help
            else:
                return await self._handle_task_help()
                
        except Exception as e:
            self.logger.error(f"Error handling task query: {e}")
            return "I'm having trouble with task management right now. Please try again!"
    
    async def _handle_add_task(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle adding a new task"""
        # Extract task details from input
        # This is a simplified version - you could enhance with more sophisticated parsing
        input_parts = user_input.lower().replace("add task", "").replace("create task", "").strip()
        
        if not input_parts:
            return "Please specify the task you want to add. Example: 'Add task: Buy groceries'"
        
        # Extract title (everything before description indicators)
        title = input_parts.split(" description:")[0].split(" due:")[0].strip()
        
        # Extract description if provided
        description = ""
        if " description:" in user_input.lower():
            description = user_input.lower().split(" description:")[1].split(" due:")[0].strip()
        
        # Extract due date if provided
        due_date = None
        if " due:" in user_input.lower():
            due_date_str = user_input.lower().split(" due:")[1].strip()
            # Simple date parsing - could be enhanced
            try:
                if "tomorrow" in due_date_str:
                    due_date = (datetime.now() + timedelta(days=1)).isoformat()
                elif "today" in due_date_str:
                    due_date = datetime.now().isoformat()
            except:
                pass
        
        task_id = await self.task_manager.add_task(
            title=title,
            description=description,
            due_date=due_date
        )
        
        response = f"✅ **Task Added Successfully!**\n\n"
        response += f"**Task ID:** {task_id}\n"
        response += f"**Title:** {title}\n"
        if description:
            response += f"**Description:** {description}\n"
        if due_date:
            response += f"**Due Date:** {due_date}\n"
        response += f"\n💡 **Tips:**\n"
        response += f"• Say 'list tasks' to see all your tasks\n"
        response += f"• Say 'complete task {task_id}' to mark it as done\n"
        response += f"• Say 'task stats' to see your productivity"
        
        return response
    
    async def _handle_complete_task(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle completing a task"""
        # Extract task identifier
        for keyword in ["complete task", "finish task", "mark done", "task done"]:
            if keyword in user_input.lower():
                task_id = user_input.lower().replace(keyword, "").strip()
                break
        else:
            return "Please specify which task to complete. Example: 'Complete task: Buy groceries'"
        
        success = await self.task_manager.complete_task(task_id)
        
        if success:
            stats = self.task_manager.get_task_stats()
            response = f"🎉 **Task Completed!**\n\n"
            response += f"Great job! You've completed another task.\n\n"
            response += f"📊 **Your Progress:**\n"
            response += f"• Total tasks: {stats['total']}\n"
            response += f"• Completed: {stats['completed']}\n"
            response += f"• Completion rate: {stats['completion_rate']}%\n\n"
            response += f"Keep up the great work! 💪"
            return response
        else:
            return f"❌ **Task not found:** '{task_id}'\n\nTry 'list tasks' to see available tasks."
    
    async def _handle_delete_task(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle deleting a task"""
        for keyword in ["delete task", "remove task", "cancel task"]:
            if keyword in user_input.lower():
                task_id = user_input.lower().replace(keyword, "").strip()
                break
        else:
            return "Please specify which task to delete. Example: 'Delete task: Buy groceries'"
        
        success = await self.task_manager.delete_task(task_id)
        
        if success:
            return f"🗑️ **Task Deleted**\n\nTask '{task_id}' has been removed from your list."
        else:
            return f"❌ **Task not found:** '{task_id}'\n\nTry 'list tasks' to see available tasks."
    
    async def _handle_list_tasks(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle listing tasks"""
        # Determine filter
        status_filter = None
        if "pending" in user_input.lower() or "todo" in user_input.lower():
            status_filter = "pending"
        elif "completed" in user_input.lower() or "done" in user_input.lower():
            status_filter = "completed"
        
        tasks = await self.task_manager.get_tasks(status=status_filter)
        
        if not tasks:
            return "📝 **No tasks found**\n\nYou don't have any tasks yet. Say 'add task: [task name]' to create one!"
        
        response = f"📋 **Your Tasks** ({len(tasks)} total)\n\n"
        
        # Group by status
        pending_tasks = [t for t in tasks if t.status == "pending"]
        in_progress_tasks = [t for t in tasks if t.status == "in_progress"]
        completed_tasks = [t for t in tasks if t.status == "completed"]
        
        if pending_tasks:
            response += "**📌 Pending Tasks:**\n"
            for task in pending_tasks[:5]:  # Show first 5
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                response += f"{priority_emoji.get(task.priority, '⚪')} {task.title} (ID: {task.id})\n"
                if task.due_date:
                    response += f"   📅 Due: {task.due_date[:10]}\n"
            response += "\n"
        
        if in_progress_tasks:
            response += "**🔄 In Progress:**\n"
            for task in in_progress_tasks[:3]:
                response += f"• {task.title} (ID: {task.id})\n"
            response += "\n"
        
        if completed_tasks and not status_filter:
            response += f"**✅ Recently Completed:** {len(completed_tasks)} tasks\n\n"
        
        response += "💡 **Quick Actions:**\n"
        response += "• 'Complete task [ID/name]' to mark as done\n"
        response += "• 'Add task: [name]' to create new task\n"
        response += "• 'Task stats' for productivity overview"
        
        return response
    
    async def _handle_task_stats(self) -> str:
        """Handle task statistics request"""
        stats = self.task_manager.get_task_stats()
        
        response = f"📊 **Your Productivity Stats**\n\n"
        response += f"**📈 Overall Progress:**\n"
        response += f"• Total tasks: {stats['total']}\n"
        response += f"• Completed: {stats['completed']}\n"
        response += f"• Pending: {stats['pending']}\n"
        response += f"• In Progress: {stats['in_progress']}\n"
        response += f"• Completion Rate: {stats['completion_rate']}%\n\n"
        
        response += f"**🎯 By Priority (Active Tasks):**\n"
        response += f"• 🔴 High Priority: {stats['by_priority']['high']}\n"
        response += f"• 🟡 Medium Priority: {stats['by_priority']['medium']}\n"
        response += f"• 🟢 Low Priority: {stats['by_priority']['low']}\n\n"
        
        # Motivational message based on completion rate
        if stats['completion_rate'] >= 80:
            response += "🌟 **Outstanding!** You're crushing your goals!"
        elif stats['completion_rate'] >= 60:
            response += "👍 **Great work!** Keep up the momentum!"
        elif stats['completion_rate'] >= 40:
            response += "💪 **Good progress!** You're getting there!"
        else:
            response += "🚀 **Ready to tackle more?** Every task completed is progress!"
        
        return response
    
    async def _handle_upcoming_tasks(self) -> str:
        """Handle upcoming tasks request"""
        upcoming = await self.task_manager.get_upcoming_tasks(days=7)
        
        if not upcoming:
            return "🗓️ **No Upcoming Deadlines**\n\nYou don't have any tasks with due dates in the next 7 days. Great job staying on top of things!"
        
        response = f"⏰ **Upcoming Tasks** (Next 7 Days)\n\n"
        
        for task in upcoming:
            try:
                due_date = datetime.fromisoformat(task.due_date)
                days_until = (due_date - datetime.now()).days
                
                if days_until < 0:
                    status_emoji = "🔴"
                    time_text = f"Overdue by {abs(days_until)} days"
                elif days_until == 0:
                    status_emoji = "🟠"
                    time_text = "Due today"
                elif days_until == 1:
                    status_emoji = "🟡"
                    time_text = "Due tomorrow"
                else:
                    status_emoji = "🟢"
                    time_text = f"Due in {days_until} days"
                
                response += f"{status_emoji} **{task.title}**\n"
                response += f"   📅 {time_text} ({due_date.strftime('%Y-%m-%d')})\n"
                if task.description:
                    response += f"   📝 {task.description[:50]}...\n"
                response += "\n"
            except:
                continue
        
        response += "💡 Focus on overdue and today's tasks first!"
        
        return response
    
    async def _handle_search_tasks(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle task search request"""
        # Extract search query
        for keyword in ["find task", "search task", "look for task"]:
            if keyword in user_input.lower():
                query = user_input.lower().replace(keyword, "").strip()
                break
        else:
            return "Please specify what to search for. Example: 'Search task: groceries'"
        
        if not query:
            return "Please provide a search term. Example: 'Find task: meeting'"
        
        results = await self.task_manager.search_tasks(query)
        
        if not results:
            return f"🔍 **No tasks found** for '{query}'\n\nTry a different search term or check your spelling."
        
        response = f"🔍 **Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for task in results[:5]:  # Show first 5 results
            status_emoji = {"pending": "📌", "in_progress": "🔄", "completed": "✅"}.get(task.status, "📝")
            response += f"{status_emoji} **{task.title}** (ID: {task.id})\n"
            if task.description:
                response += f"   📝 {task.description[:100]}...\n"
            response += f"   📊 Status: {task.status.title()}, Priority: {task.priority.title()}\n\n"
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use the task ID to complete or delete specific tasks."
        
        return response
    
    async def _handle_task_help(self) -> str:
        """Provide task management help"""
        response = f"📋 **Task Management Help**\n\n"
        response += f"**📝 Adding Tasks:**\n"
        response += f"• 'Add task: Buy groceries'\n"
        response += f"• 'Create task: Meeting with team description: Discuss project due: tomorrow'\n\n"
        
        response += f"**✅ Managing Tasks:**\n"
        response += f"• 'Complete task: Buy groceries' or 'Complete task [ID]'\n"
        response += f"• 'Delete task: Old meeting'\n"
        response += f"• 'List tasks' or 'Show pending tasks'\n\n"
        
        response += f"**🔍 Finding Tasks:**\n"
        response += f"• 'Search task: meeting'\n"
        response += f"• 'Upcoming tasks' or 'Show deadlines'\n"
        response += f"• 'Task stats' for productivity overview\n\n"
        
        response += f"**💡 Tips:**\n"
        response += f"• Use specific task names for easier management\n"
        response += f"• Set due dates to track deadlines\n"
        response += f"• Check your stats regularly for motivation\n"
        response += f"• Break large tasks into smaller ones"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_task_skill():
        skill = TaskSkill()
        
        test_queries = [
            "add task: Buy groceries",
            "list tasks",
            "task stats",
            "add task: Meeting with team description: Discuss new features due: tomorrow",
            "complete task: Buy groceries",
            "upcoming tasks"
        ]
        
        print("🧪 Testing Task Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_task_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_task_skill())
