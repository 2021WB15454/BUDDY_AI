"""
Research & Knowledge Assistant Module for BUDDY AI Assistant
Handles research tracking, knowledge management, learning goals, and information organization
"""

import asyncio
import logging
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import uuid
from urllib.parse import urlparse


@dataclass
class ResearchTopic:
    """Research topic structure"""
    id: str
    title: str
    description: str
    category: str
    priority: str  # high, medium, low
    status: str    # planning, researching, completed, paused
    start_date: str
    target_completion: str
    tags: List[str]
    research_questions: List[str]
    key_findings: List[str]
    sources: List[str]
    notes: str
    progress_percentage: int
    created_at: str
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.start_date:
            self.start_date = datetime.now().isoformat()


@dataclass
class KnowledgeItem:
    """Knowledge base item structure"""
    id: str
    title: str
    content: str
    category: str
    subcategory: str
    tags: List[str]
    source: str
    source_url: str
    confidence_level: str  # high, medium, low
    date_learned: str
    last_reviewed: str
    review_frequency_days: int
    difficulty_level: str  # beginner, intermediate, advanced
    related_topics: List[str]
    practical_applications: List[str]
    notes: str
    
    def __post_init__(self):
        if not self.date_learned:
            self.date_learned = datetime.now().isoformat()


@dataclass
class LearningGoal:
    """Learning goal structure"""
    id: str
    title: str
    description: str
    category: str
    target_date: str
    status: str  # active, completed, paused, cancelled
    progress_percentage: int
    milestones: List[Dict[str, Any]]  # [{"title": str, "completed": bool, "date": str}]
    resources: List[str]
    time_invested_hours: float
    estimated_hours: float
    difficulty: str
    priority: str
    notes: str
    created_at: str
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class ResearchSession:
    """Research session log"""
    id: str
    topic_id: str
    session_date: str
    duration_minutes: int
    activities: List[str]  # reading, note-taking, experimenting, etc.
    sources_reviewed: List[str]
    key_insights: List[str]
    questions_raised: List[str]
    next_steps: List[str]
    productivity_rating: int  # 1-5 scale
    notes: str
    
    def __post_init__(self):
        if not self.session_date:
            self.session_date = datetime.now().isoformat()


class ResearchManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.topics_file = "learning_data/research_topics.json"
        self.knowledge_file = "learning_data/knowledge_base.json"
        self.goals_file = "learning_data/learning_goals.json"
        self.sessions_file = "learning_data/research_sessions.json"
        self.topics = self._load_topics()
        self.knowledge = self._load_knowledge()
        self.goals = self._load_goals()
        self.sessions = self._load_sessions()
        self.logger.info("ResearchManager initialized.")
    
    def _load_topics(self) -> List[ResearchTopic]:
        """Load research topics from file"""
        try:
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                topics_data = json.load(f)
                return [ResearchTopic(**topic) for topic in topics_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_knowledge(self) -> List[KnowledgeItem]:
        """Load knowledge base from file"""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)
                return [KnowledgeItem(**item) for item in knowledge_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_goals(self) -> List[LearningGoal]:
        """Load learning goals from file"""
        try:
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                goals_data = json.load(f)
                return [LearningGoal(**goal) for goal in goals_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_sessions(self) -> List[ResearchSession]:
        """Load research sessions from file"""
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                sessions_data = json.load(f)
                return [ResearchSession(**session) for session in sessions_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_topics(self):
        """Save research topics to file"""
        try:
            os.makedirs(os.path.dirname(self.topics_file), exist_ok=True)
            with open(self.topics_file, 'w', encoding='utf-8') as f:
                topics_data = [asdict(topic) for topic in self.topics]
                json.dump(topics_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving topics: {e}")
    
    def _save_knowledge(self):
        """Save knowledge base to file"""
        try:
            os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                knowledge_data = [asdict(item) for item in self.knowledge]
                json.dump(knowledge_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving knowledge: {e}")
    
    def _save_goals(self):
        """Save learning goals to file"""
        try:
            os.makedirs(os.path.dirname(self.goals_file), exist_ok=True)
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                goals_data = [asdict(goal) for goal in self.goals]
                json.dump(goals_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving goals: {e}")
    
    def _save_sessions(self):
        """Save research sessions to file"""
        try:
            os.makedirs(os.path.dirname(self.sessions_file), exist_ok=True)
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                sessions_data = [asdict(session) for session in self.sessions]
                json.dump(sessions_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving sessions: {e}")
    
    async def create_research_topic(self, title: str, description: str, category: str = "",
                                  priority: str = "medium", tags: List[str] = None,
                                  research_questions: List[str] = None,
                                  target_completion: str = "") -> str:
        """Create a new research topic"""
        
        topic = ResearchTopic(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            category=category,
            priority=priority.lower(),
            status="planning",
            start_date=datetime.now().isoformat(),
            target_completion=target_completion,
            tags=tags or [],
            research_questions=research_questions or [],
            key_findings=[],
            sources=[],
            notes="",
            progress_percentage=0,
            created_at=datetime.now().isoformat()
        )
        
        self.topics.append(topic)
        self._save_topics()
        
        self.logger.info(f"Research topic created: {title}")
        return topic.id
    
    async def add_knowledge_item(self, title: str, content: str, category: str = "",
                               subcategory: str = "", tags: List[str] = None,
                               source: str = "", source_url: str = "",
                               confidence_level: str = "medium",
                               difficulty_level: str = "intermediate") -> str:
        """Add a new knowledge item"""
        
        item = KnowledgeItem(
            id=str(uuid.uuid4())[:8],
            title=title,
            content=content,
            category=category,
            subcategory=subcategory,
            tags=tags or [],
            source=source,
            source_url=source_url,
            confidence_level=confidence_level.lower(),
            date_learned=datetime.now().isoformat(),
            last_reviewed=datetime.now().isoformat(),
            review_frequency_days=30,  # Default monthly review
            difficulty_level=difficulty_level.lower(),
            related_topics=[],
            practical_applications=[],
            notes=""
        )
        
        self.knowledge.append(item)
        self._save_knowledge()
        
        self.logger.info(f"Knowledge item added: {title}")
        return item.id
    
    async def create_learning_goal(self, title: str, description: str, category: str = "",
                                 target_date: str = "", estimated_hours: float = 0,
                                 difficulty: str = "intermediate", priority: str = "medium") -> str:
        """Create a new learning goal"""
        
        goal = LearningGoal(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            category=category,
            target_date=target_date,
            status="active",
            progress_percentage=0,
            milestones=[],
            resources=[],
            time_invested_hours=0.0,
            estimated_hours=estimated_hours,
            difficulty=difficulty.lower(),
            priority=priority.lower(),
            notes="",
            created_at=datetime.now().isoformat()
        )
        
        self.goals.append(goal)
        self._save_goals()
        
        self.logger.info(f"Learning goal created: {title}")
        return goal.id
    
    async def log_research_session(self, topic_id: str, duration_minutes: int,
                                 activities: List[str] = None, sources_reviewed: List[str] = None,
                                 key_insights: List[str] = None, productivity_rating: int = 3,
                                 notes: str = "") -> str:
        """Log a research session"""
        
        session = ResearchSession(
            id=str(uuid.uuid4())[:8],
            topic_id=topic_id,
            session_date=datetime.now().isoformat(),
            duration_minutes=duration_minutes,
            activities=activities or [],
            sources_reviewed=sources_reviewed or [],
            key_insights=key_insights or [],
            questions_raised=[],
            next_steps=[],
            productivity_rating=max(1, min(5, productivity_rating)),
            notes=notes
        )
        
        self.sessions.append(session)
        self._save_sessions()
        
        self.logger.info(f"Research session logged: {duration_minutes} minutes")
        return session.id
    
    async def search_knowledge(self, query: str) -> List[KnowledgeItem]:
        """Search knowledge base"""
        if not query:
            return []
        
        query = query.lower()
        results = []
        
        for item in self.knowledge:
            if (query in item.title.lower() or
                query in item.content.lower() or
                query in item.category.lower() or
                query in item.subcategory.lower() or
                any(query in tag.lower() for tag in item.tags)):
                results.append(item)
        
        # Sort by relevance
        results.sort(key=lambda i: (
            0 if query in i.title.lower() else
            1 if query in i.content.lower()[:100] else 2,
            i.confidence_level == "high"
        ), reverse=True)
        
        return results
    
    async def get_active_research_topics(self) -> List[ResearchTopic]:
        """Get all active research topics"""
        return [t for t in self.topics if t.status in ["planning", "researching"]]
    
    async def get_active_learning_goals(self) -> List[LearningGoal]:
        """Get all active learning goals"""
        return [g for g in self.goals if g.status == "active"]
    
    async def get_knowledge_for_review(self) -> List[KnowledgeItem]:
        """Get knowledge items that need review"""
        now = datetime.now()
        needs_review = []
        
        for item in self.knowledge:
            try:
                last_review = datetime.fromisoformat(item.last_reviewed)
                days_since = (now - last_review).days
                if days_since >= item.review_frequency_days:
                    needs_review.append(item)
            except:
                needs_review.append(item)  # If parsing fails, assume needs review
        
        # Sort by days overdue
        needs_review.sort(key=lambda i: 
            (datetime.now() - datetime.fromisoformat(i.last_reviewed)).days
            if i.last_reviewed else 999, reverse=True)
        
        return needs_review
    
    async def get_research_statistics(self) -> Dict[str, Any]:
        """Get research and learning statistics"""
        
        # Basic counts
        total_topics = len(self.topics)
        active_topics = len([t for t in self.topics if t.status in ["planning", "researching"]])
        completed_topics = len([t for t in self.topics if t.status == "completed"])
        
        total_knowledge = len(self.knowledge)
        total_goals = len(self.goals)
        active_goals = len([g for g in self.goals if g.status == "active"])
        
        # Recent activity
        now = datetime.now()
        recent_sessions = len([s for s in self.sessions 
                             if (now - datetime.fromisoformat(s.session_date)).days <= 7])
        
        total_research_time = sum(s.duration_minutes for s in self.sessions) / 60  # in hours
        
        # Categories
        topic_categories = {}
        for topic in self.topics:
            if topic.category:
                topic_categories[topic.category] = topic_categories.get(topic.category, 0) + 1
        
        knowledge_categories = {}
        for item in self.knowledge:
            if item.category:
                knowledge_categories[item.category] = knowledge_categories.get(item.category, 0) + 1
        
        # Progress
        avg_topic_progress = sum(t.progress_percentage for t in self.topics) / len(self.topics) if self.topics else 0
        avg_goal_progress = sum(g.progress_percentage for g in self.goals) / len(self.goals) if self.goals else 0
        
        return {
            "total_research_topics": total_topics,
            "active_research_topics": active_topics,
            "completed_research_topics": completed_topics,
            "total_knowledge_items": total_knowledge,
            "total_learning_goals": total_goals,
            "active_learning_goals": active_goals,
            "recent_research_sessions": recent_sessions,
            "total_research_hours": round(total_research_time, 1),
            "topic_categories": topic_categories,
            "knowledge_categories": knowledge_categories,
            "avg_topic_progress": round(avg_topic_progress, 1),
            "avg_goal_progress": round(avg_goal_progress, 1),
            "items_need_review": len(await self.get_knowledge_for_review())
        }


class ResearchSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.research_manager = ResearchManager()
        self.logger.info("ResearchSkill initialized.")
    
    async def handle_research_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle research and knowledge management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Research topics
            if any(keyword in query_lower for keyword in ["research topic", "new research", "research project"]):
                return await self._handle_research_topics(user_input, context)
            
            # Knowledge base
            elif any(keyword in query_lower for keyword in ["add knowledge", "save knowledge", "knowledge base"]):
                return await self._handle_knowledge_base(user_input, context)
            
            # Learning goals
            elif any(keyword in query_lower for keyword in ["learning goal", "study goal", "learn about"]):
                return await self._handle_learning_goals(user_input, context)
            
            # Search knowledge
            elif any(keyword in query_lower for keyword in ["search knowledge", "find information", "what do I know about"]):
                return await self._handle_search_knowledge(user_input, context)
            
            # Research sessions
            elif any(keyword in query_lower for keyword in ["research session", "study session", "log research"]):
                return await self._handle_research_sessions(user_input, context)
            
            # Review knowledge
            elif any(keyword in query_lower for keyword in ["review knowledge", "knowledge review", "what needs review"]):
                return await self._handle_knowledge_review()
            
            # Research progress
            elif any(keyword in query_lower for keyword in ["research progress", "learning progress", "my research"]):
                return await self._handle_research_progress()
            
            # Research statistics
            elif any(keyword in query_lower for keyword in ["research stats", "learning stats", "knowledge stats"]):
                return await self._handle_research_stats()
            
            # Default help
            else:
                return await self._handle_research_help()
                
        except Exception as e:
            self.logger.error(f"Error handling research query: {e}")
            return "I'm having trouble with research management right now. Please try again!"
    
    async def _handle_research_topics(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle research topic operations"""
        query_lower = user_input.lower()
        
        if "new research" in query_lower or "research topic" in query_lower:
            # Extract topic information (simplified parsing)
            topic_text = user_input
            for keyword in ["create research topic", "new research", "research topic"]:
                topic_text = topic_text.replace(keyword, "").strip()
            
            if not topic_text:
                return ("🔬 **Create Research Topic**\n\n"
                       "Please specify the research topic. Examples:\n"
                       "• 'Research topic: Machine Learning Applications'\n"
                       "• 'New research: Climate Change Solutions'\n"
                       "• 'Research project: Ancient History'")
            
            # For demo, create a basic topic
            topic_id = await self.research_manager.create_research_topic(
                title=topic_text,
                description=f"Research topic created from: {user_input}",
                category="general"
            )
            
            response = f"🔬 **Research Topic Created!**\n\n"
            response += f"**Topic:** {topic_text}\n"
            response += f"**ID:** {topic_id}\n"
            response += f"**Status:** Planning\n"
            response += f"**Created:** {datetime.now().strftime('%B %d, %Y')}\n\n"
            response += f"💡 **Next Steps:**\n"
            response += f"• Define research questions\n"
            response += f"• Identify key sources\n"
            response += f"• Set target completion date\n"
            response += f"• Start logging research sessions"
            
            return response
        
        # Show active research topics
        active_topics = await self.research_manager.get_active_research_topics()
        
        if not active_topics:
            return ("🔬 **No Active Research Topics**\n\n"
                   "You don't have any ongoing research projects.\n"
                   "Use 'Research topic: [subject]' to start a new research project!")
        
        response = f"🔬 **Active Research Topics** ({len(active_topics)} projects)\n\n"
        
        for topic in active_topics:
            status_emoji = {"planning": "📋", "researching": "🔍", "completed": "✅"}.get(topic.status, "📋")
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(topic.priority, "⚪")
            
            response += f"{status_emoji} {priority_emoji} **{topic.title}**\n"
            response += f"   📝 {topic.description[:60]}...\n"
            response += f"   📊 Progress: {topic.progress_percentage}%\n"
            response += f"   🏷️ Category: {topic.category or 'General'}\n"
            
            if topic.target_completion:
                try:
                    target_date = datetime.fromisoformat(topic.target_completion)
                    days_until = (target_date - datetime.now()).days
                    if days_until > 0:
                        response += f"   📅 Due in {days_until} days\n"
                    else:
                        response += f"   ⚠️ Overdue by {abs(days_until)} days\n"
                except:
                    pass
            
            response += f"   🆔 ID: {topic.id}\n\n"
        
        response += "💡 Use 'Log research session: [topic]' to track your research progress."
        
        return response
    
    async def _handle_knowledge_base(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle knowledge base operations"""
        query_lower = user_input.lower()
        
        if "add knowledge" in query_lower or "save knowledge" in query_lower:
            return ("📚 **Add Knowledge Item**\n\n"
                   "Feature coming soon! This will allow you to:\n\n"
                   "• Save important information and insights\n"
                   "• Organize knowledge by category and tags\n"
                   "• Set confidence levels and review schedules\n"
                   "• Link related concepts together\n\n"
                   "Example usage:\n"
                   "'Add knowledge: Python list comprehensions are ...'")
        
        # Show knowledge base overview
        knowledge_count = len(self.research_manager.knowledge)
        
        if knowledge_count == 0:
            return ("📚 **Knowledge Base Empty**\n\n"
                   "You haven't added any knowledge items yet.\n"
                   "Start building your personal knowledge base by saving insights from your research!")
        
        response = f"📚 **Knowledge Base Overview** ({knowledge_count} items)\n\n"
        
        # Group by category
        categories = {}
        for item in self.research_manager.knowledge:
            cat = item.category or "Uncategorized"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        for category, items in categories.items():
            response += f"**📁 {category}** ({len(items)} items)\n"
            for item in items[:3]:  # Show first 3 items per category
                confidence_emoji = {"high": "✅", "medium": "🟡", "low": "❓"}.get(item.confidence_level, "⚪")
                response += f"   {confidence_emoji} {item.title}\n"
            
            if len(items) > 3:
                response += f"   ... and {len(items) - 3} more\n"
            response += "\n"
        
        response += "💡 Use 'Search knowledge: [topic]' to find specific information."
        
        return response
    
    async def _handle_learning_goals(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle learning goals operations"""
        query_lower = user_input.lower()
        
        if "learning goal" in query_lower or "study goal" in query_lower:
            # Extract goal information
            goal_text = user_input
            for keyword in ["learning goal", "study goal", "learn about"]:
                goal_text = goal_text.replace(keyword, "").strip()
            
            if not goal_text:
                return ("🎯 **Create Learning Goal**\n\n"
                       "Please specify what you want to learn. Examples:\n"
                       "• 'Learning goal: Master Python programming'\n"
                       "• 'Study goal: Understand quantum physics basics'\n"
                       "• 'Learn about: Data visualization techniques'")
            
            # For demo, create a basic goal
            goal_id = await self.research_manager.create_learning_goal(
                title=goal_text,
                description=f"Learning goal created from: {user_input}",
                category="general"
            )
            
            response = f"🎯 **Learning Goal Created!**\n\n"
            response += f"**Goal:** {goal_text}\n"
            response += f"**ID:** {goal_id}\n"
            response += f"**Status:** Active\n"
            response += f"**Progress:** 0%\n"
            response += f"**Created:** {datetime.now().strftime('%B %d, %Y')}\n\n"
            response += f"💡 **Success Tips:**\n"
            response += f"• Break down into smaller milestones\n"
            response += f"• Set a realistic target date\n"
            response += f"• Track your study sessions\n"
            response += f"• Regularly review your progress"
            
            return response
        
        # Show active learning goals
        active_goals = await self.research_manager.get_active_learning_goals()
        
        if not active_goals:
            return ("🎯 **No Active Learning Goals**\n\n"
                   "You don't have any active learning goals.\n"
                   "Set some goals to focus your learning efforts and track progress!")
        
        response = f"🎯 **Active Learning Goals** ({len(active_goals)} goals)\n\n"
        
        for goal in active_goals:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(goal.priority, "⚪")
            
            response += f"{priority_emoji} **{goal.title}**\n"
            response += f"   📝 {goal.description[:60]}...\n"
            response += f"   📊 Progress: {goal.progress_percentage}%\n"
            response += f"   ⏱️ Time invested: {goal.time_invested_hours}h"
            
            if goal.estimated_hours > 0:
                response += f" / {goal.estimated_hours}h estimated"
            response += "\n"
            
            if goal.target_date:
                try:
                    target_date = datetime.fromisoformat(goal.target_date)
                    days_until = (target_date - datetime.now()).days
                    if days_until > 0:
                        response += f"   📅 Target: {days_until} days remaining\n"
                    else:
                        response += f"   ⚠️ Target date passed\n"
                except:
                    pass
            
            response += f"   🆔 ID: {goal.id}\n\n"
        
        response += "💡 Track your study time and update progress regularly to stay motivated!"
        
        return response
    
    async def _handle_search_knowledge(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle knowledge search requests"""
        # Extract search query
        query = user_input.lower()
        for keyword in ["search knowledge", "find information", "what do I know about"]:
            query = query.replace(keyword, "").strip()
        
        if not query:
            return ("🔍 **Search Knowledge Base**\n\n"
                   "Please specify what to search for. Examples:\n"
                   "• 'Search knowledge: machine learning'\n"
                   "• 'What do I know about Python?'\n"
                   "• 'Find information: data structures'")
        
        results = await self.research_manager.search_knowledge(query)
        
        if not results:
            return f"🔍 **No knowledge found** for '{query}'\n\nTry a different search term or add more information to your knowledge base."
        
        response = f"🔍 **Knowledge Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for item in results[:5]:  # Show top 5 results
            confidence_emoji = {"high": "✅", "medium": "🟡", "low": "❓"}.get(item.confidence_level, "⚪")
            difficulty_emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}.get(item.difficulty_level, "⚪")
            
            response += f"{confidence_emoji} {difficulty_emoji} **{item.title}**\n"
            response += f"   📂 {item.category} > {item.subcategory}\n" if item.subcategory else f"   📂 {item.category}\n"
            response += f"   📝 {item.content[:100]}...\n"
            
            if item.tags:
                response += f"   🏷️ {', '.join(item.tags[:3])}\n"
            
            if item.source:
                response += f"   📖 Source: {item.source}\n"
            
            try:
                learned_date = datetime.fromisoformat(item.date_learned)
                days_ago = (datetime.now() - learned_date).days
                response += f"   📅 Learned {days_ago} days ago\n"
            except:
                pass
            
            response += f"   🆔 ID: {item.id}\n\n"
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use specific keywords or categories to narrow down your search."
        
        return response
    
    async def _handle_research_sessions(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle research session logging"""
        return ("📊 **Research Session Logging**\n\n"
               "Feature coming soon! This will help you:\n\n"
               "• Track time spent on research activities\n"
               "• Log key insights and discoveries\n"
               "• Monitor productivity and focus\n"
               "• Identify most effective research methods\n\n"
               "Example usage:\n"
               "'Log research session: 2 hours on machine learning basics'")
    
    async def _handle_knowledge_review(self) -> str:
        """Handle knowledge review requests"""
        items_to_review = await self.research_manager.get_knowledge_for_review()
        
        if not items_to_review:
            return ("✅ **Knowledge Up to Date!**\n\n"
                   "All your knowledge items are current.\n"
                   "Regular review helps maintain and strengthen your understanding!")
        
        response = f"📖 **Knowledge Items Needing Review** ({len(items_to_review)} items)\n\n"
        
        for item in items_to_review[:8]:  # Show top 8 items
            try:
                last_review = datetime.fromisoformat(item.last_reviewed)
                days_overdue = (datetime.now() - last_review).days - item.review_frequency_days
                
                urgency_emoji = "🔴" if days_overdue > 30 else "🟡" if days_overdue > 7 else "🟢"
                difficulty_emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}.get(item.difficulty_level, "⚪")
                
                response += f"{urgency_emoji} {difficulty_emoji} **{item.title}**\n"
                response += f"   📂 {item.category}\n"
                response += f"   ⏰ {days_overdue} days overdue for review\n"
                response += f"   📅 Last reviewed: {last_review.strftime('%m/%d/%Y')}\n"
                
                if item.tags:
                    response += f"   🏷️ {', '.join(item.tags[:2])}\n"
                
                response += "\n"
                
            except Exception:
                continue
        
        if len(items_to_review) > 8:
            response += f"... and {len(items_to_review) - 8} more items\n\n"
        
        response += "💡 **Review Benefits:**\n"
        response += "• Strengthens long-term memory retention\n"
        response += "• Identifies knowledge gaps and updates needed\n"
        response += "• Connects new learning with existing knowledge\n"
        response += "• Maintains expertise in important topics"
        
        return response
    
    async def _handle_research_progress(self) -> str:
        """Handle research progress overview"""
        active_topics = await self.research_manager.get_active_research_topics()
        active_goals = await self.research_manager.get_active_learning_goals()
        
        response = f"📈 **Research & Learning Progress**\n\n"
        
        if active_topics:
            response += f"**🔬 Active Research Topics:**\n"
            for topic in active_topics[:3]:
                progress_bar = "█" * (topic.progress_percentage // 10) + "░" * (10 - topic.progress_percentage // 10)
                response += f"• {topic.title}: {topic.progress_percentage}% [{progress_bar}]\n"
            
            if len(active_topics) > 3:
                response += f"... and {len(active_topics) - 3} more topics\n"
            response += "\n"
        
        if active_goals:
            response += f"**🎯 Learning Goals Progress:**\n"
            for goal in active_goals[:3]:
                progress_bar = "█" * (goal.progress_percentage // 10) + "░" * (10 - goal.progress_percentage // 10)
                response += f"• {goal.title}: {goal.progress_percentage}% [{progress_bar}]\n"
                if goal.time_invested_hours > 0:
                    response += f"  ⏱️ {goal.time_invested_hours}h invested\n"
            
            if len(active_goals) > 3:
                response += f"... and {len(active_goals) - 3} more goals\n"
            response += "\n"
        
        if not active_topics and not active_goals:
            response += "No active research topics or learning goals.\n"
            response += "Start your learning journey by setting some goals!\n\n"
        
        # Recent activity
        recent_sessions = len([s for s in self.research_manager.sessions 
                              if (datetime.now() - datetime.fromisoformat(s.session_date)).days <= 7])
        
        response += f"**📊 Recent Activity:**\n"
        response += f"• Research sessions this week: {recent_sessions}\n"
        response += f"• Knowledge items: {len(self.research_manager.knowledge)}\n"
        response += f"• Items needing review: {len(await self.research_manager.get_knowledge_for_review())}\n\n"
        
        response += "💡 Consistent progress, even small steps, leads to significant learning over time!"
        
        return response
    
    async def _handle_research_stats(self) -> str:
        """Handle research statistics request"""
        stats = await self.research_manager.get_research_statistics()
        
        response = f"📊 **Research & Learning Statistics**\n\n"
        
        response += f"**📈 Overview:**\n"
        response += f"• Research topics: {stats['total_research_topics']} (Active: {stats['active_research_topics']})\n"
        response += f"• Learning goals: {stats['total_learning_goals']} (Active: {stats['active_learning_goals']})\n"
        response += f"• Knowledge items: {stats['total_knowledge_items']}\n"
        response += f"• Total research time: {stats['total_research_hours']} hours\n"
        response += f"• Recent sessions (7 days): {stats['recent_research_sessions']}\n\n"
        
        response += f"**📊 Progress:**\n"
        response += f"• Average topic progress: {stats['avg_topic_progress']}%\n"
        response += f"• Average goal progress: {stats['avg_goal_progress']}%\n"
        response += f"• Completed topics: {stats['completed_research_topics']}\n"
        response += f"• Items needing review: {stats['items_need_review']}\n\n"
        
        if stats['topic_categories']:
            response += f"**🔬 Research Categories:**\n"
            for category, count in sorted(stats['topic_categories'].items(), key=lambda x: x[1], reverse=True):
                response += f"• {category}: {count} topics\n"
            response += "\n"
        
        if stats['knowledge_categories']:
            response += f"**📚 Knowledge Categories:**\n"
            for category, count in sorted(stats['knowledge_categories'].items(), key=lambda x: x[1], reverse=True):
                response += f"• {category}: {count} items\n"
            response += "\n"
        
        # Learning insights
        response += f"**💡 Learning Insights:**\n"
        if stats['total_research_hours'] > 50:
            response += f"• Excellent research dedication! ({stats['total_research_hours']}h total)\n"
        elif stats['total_research_hours'] > 10:
            response += f"• Good research progress! Keep building the habit\n"
        else:
            response += f"• Start tracking research sessions for better insights\n"
        
        if stats['items_need_review'] > 10:
            response += f"• Consider reviewing older knowledge items\n"
        elif stats['items_need_review'] == 0:
            response += f"• Excellent knowledge maintenance!\n"
        
        response += f"• Diversify research categories for broader knowledge\n"
        response += f"• Regular review strengthens long-term retention"
        
        return response
    
    async def _handle_research_help(self) -> str:
        """Provide research and knowledge management help"""
        response = f"🔬 **Research & Knowledge Management Help**\n\n"
        
        response += f"**🔍 Research Management:**\n"
        response += f"• 'Research topic: [subject]' - Start new research\n"
        response += f"• 'My research topics' - View active projects\n"
        response += f"• 'Research progress' - Check overall progress\n"
        response += f"• 'Log research session' - Track study time\n\n"
        
        response += f"**📚 Knowledge Base:**\n"
        response += f"• 'Add knowledge: [information]' - Save insights\n"
        response += f"• 'Search knowledge: [topic]' - Find information\n"
        response += f"• 'Knowledge base' - Overview of saved knowledge\n"
        response += f"• 'Knowledge review' - Items needing review\n\n"
        
        response += f"**🎯 Learning Goals:**\n"
        response += f"• 'Learning goal: [objective]' - Set learning target\n"
        response += f"• 'My learning goals' - View active goals\n"
        response += f"• 'Learning progress' - Track goal advancement\n\n"
        
        response += f"**📊 Analytics:**\n"
        response += f"• 'Research stats' - Overview and insights\n"
        response += f"• 'Learning statistics' - Detailed analytics\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Set specific, measurable learning goals\n"
        response += f"• Track research sessions for motivation\n"
        response += f"• Regularly review knowledge for retention\n"
        response += f"• Use categories and tags for organization\n"
        response += f"• Connect new learning with existing knowledge\n"
        response += f"• Break large topics into manageable chunks"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_research_skill():
        skill = ResearchSkill()
        
        test_queries = [
            "research topic: artificial intelligence",
            "learning goal: master Python",
            "search knowledge: programming",
            "knowledge review",
            "research stats"
        ]
        
        print("🧪 Testing Research & Knowledge Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_research_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_research_skill())
