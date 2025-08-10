"""
Calendar and Scheduling Module for BUDDY AI Assistant
Handles appointments, events, reminders, and schedule management
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid
import re


@dataclass
class Event:
    """Event/appointment data structure"""
    id: str
    title: str
    description: str
    start_time: str
    end_time: str
    location: str
    attendees: List[str]
    category: str
    priority: str  # high, medium, low
    status: str    # scheduled, completed, cancelled
    reminder_minutes: int  # minutes before event to remind
    created_at: str
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class CalendarManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.events_file = "learning_data/calendar_events.json"
        self.events = self._load_events()
        self.logger.info("CalendarManager initialized.")
    
    def _load_events(self) -> List[Event]:
        """Load events from file"""
        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
                return [Event(**event) for event in events_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_events(self):
        """Save events to file"""
        try:
            os.makedirs(os.path.dirname(self.events_file), exist_ok=True)
            with open(self.events_file, 'w', encoding='utf-8') as f:
                events_data = [asdict(event) for event in self.events]
                json.dump(events_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving events: {e}")
    
    def _parse_datetime(self, date_str: str, time_str: str = None) -> Optional[datetime]:
        """Parse date and time strings into datetime object"""
        try:
            # Handle common date formats
            today = datetime.now()
            
            if "today" in date_str.lower():
                base_date = today
            elif "tomorrow" in date_str.lower():
                base_date = today + timedelta(days=1)
            elif "next week" in date_str.lower():
                base_date = today + timedelta(weeks=1)
            else:
                # Try to parse specific date formats
                for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m-%d-%Y"]:
                    try:
                        base_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return None
            
            # Handle time
            if time_str:
                time_str = time_str.lower().replace(" ", "")
                
                # Handle AM/PM format
                if "am" in time_str or "pm" in time_str:
                    time_str = time_str.replace("am", " AM").replace("pm", " PM")
                    for fmt in ["%I:%M %p", "%I %p"]:
                        try:
                            time_obj = datetime.strptime(time_str, fmt).time()
                            return datetime.combine(base_date.date(), time_obj)
                        except ValueError:
                            continue
                
                # Handle 24-hour format
                for fmt in ["%H:%M", "%H"]:
                    try:
                        time_obj = datetime.strptime(time_str, fmt).time()
                        return datetime.combine(base_date.date(), time_obj)
                    except ValueError:
                        continue
            
            # Return date with default time if no time specified
            return datetime.combine(base_date.date(), datetime.min.time().replace(hour=9))
            
        except Exception as e:
            self.logger.error(f"Error parsing datetime: {e}")
            return None
    
    async def create_event(self, title: str, start_time: str, end_time: str = None,
                          description: str = "", location: str = "", attendees: List[str] = None,
                          category: str = "general", priority: str = "medium") -> str:
        """Create a new event/appointment"""
        
        # If end_time not provided, default to 1 hour after start
        if not end_time:
            try:
                start_dt = datetime.fromisoformat(start_time)
                end_dt = start_dt + timedelta(hours=1)
                end_time = end_dt.isoformat()
            except:
                end_time = start_time
        
        event = Event(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            attendees=attendees or [],
            category=category,
            priority=priority.lower(),
            status="scheduled",
            reminder_minutes=15,  # Default 15 minutes reminder
            created_at=datetime.now().isoformat()
        )
        
        self.events.append(event)
        self._save_events()
        
        self.logger.info(f"Event created: {title}")
        return event.id
    
    async def get_events_for_date(self, date: datetime) -> List[Event]:
        """Get all events for a specific date"""
        target_date = date.date()
        day_events = []
        
        for event in self.events:
            try:
                event_date = datetime.fromisoformat(event.start_time).date()
                if event_date == target_date and event.status == "scheduled":
                    day_events.append(event)
            except:
                continue
        
        # Sort by start time
        day_events.sort(key=lambda e: e.start_time)
        return day_events
    
    async def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """Get upcoming events in the next N days"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        upcoming = []
        
        for event in self.events:
            try:
                event_time = datetime.fromisoformat(event.start_time)
                if now <= event_time <= cutoff and event.status == "scheduled":
                    upcoming.append(event)
            except:
                continue
        
        upcoming.sort(key=lambda e: e.start_time)
        return upcoming
    
    async def search_events(self, query: str) -> List[Event]:
        """Search events by title, description, or location"""
        query = query.lower()
        results = []
        
        for event in self.events:
            if (query in event.title.lower() or
                query in event.description.lower() or
                query in event.location.lower() or
                any(query in attendee.lower() for attendee in event.attendees)):
                results.append(event)
        
        return sorted(results, key=lambda e: e.start_time)
    
    async def cancel_event(self, event_id: str) -> bool:
        """Cancel an event"""
        for event in self.events:
            if event.id == event_id or event.title.lower() == event_id.lower():
                event.status = "cancelled"
                self._save_events()
                self.logger.info(f"Event cancelled: {event.title}")
                return True
        return False
    
    async def complete_event(self, event_id: str) -> bool:
        """Mark an event as completed"""
        for event in self.events:
            if event.id == event_id or event.title.lower() == event_id.lower():
                event.status = "completed"
                self._save_events()
                self.logger.info(f"Event completed: {event.title}")
                return True
        return False
    
    def get_schedule_stats(self) -> Dict[str, Any]:
        """Get scheduling statistics"""
        now = datetime.now()
        upcoming = [e for e in self.events if datetime.fromisoformat(e.start_time) > now and e.status == "scheduled"]
        completed = [e for e in self.events if e.status == "completed"]
        cancelled = [e for e in self.events if e.status == "cancelled"]
        
        # Events by category
        categories = {}
        for event in self.events:
            if event.status == "scheduled":
                categories[event.category] = categories.get(event.category, 0) + 1
        
        return {
            "total_events": len(self.events),
            "upcoming_events": len(upcoming),
            "completed_events": len(completed),
            "cancelled_events": len(cancelled),
            "events_by_category": categories,
            "events_this_week": len([e for e in upcoming if datetime.fromisoformat(e.start_time) <= now + timedelta(weeks=1)])
        }


class CalendarSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.calendar_manager = CalendarManager()
        self.logger.info("CalendarSkill initialized.")
    
    async def handle_calendar_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle calendar and scheduling queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Schedule appointment/event
            if any(keyword in query_lower for keyword in ["schedule", "book appointment", "add event", "create appointment"]):
                return await self._handle_schedule_event(user_input, context)
            
            # Show schedule/calendar
            elif any(keyword in query_lower for keyword in ["show schedule", "my calendar", "what's my schedule", "schedule for"]):
                return await self._handle_show_schedule(user_input, context)
            
            # Upcoming events
            elif any(keyword in query_lower for keyword in ["upcoming events", "next events", "upcoming appointments"]):
                return await self._handle_upcoming_events(user_input, context)
            
            # Today's schedule
            elif any(keyword in query_lower for keyword in ["today's schedule", "schedule today", "what's today"]):
                return await self._handle_today_schedule()
            
            # Tomorrow's schedule
            elif any(keyword in query_lower for keyword in ["tomorrow's schedule", "schedule tomorrow", "what's tomorrow"]):
                return await self._handle_tomorrow_schedule()
            
            # Cancel event
            elif any(keyword in query_lower for keyword in ["cancel event", "cancel appointment", "remove event"]):
                return await self._handle_cancel_event(user_input, context)
            
            # Find/search events
            elif any(keyword in query_lower for keyword in ["find event", "search event", "look for appointment"]):
                return await self._handle_search_events(user_input, context)
            
            # Schedule statistics
            elif any(keyword in query_lower for keyword in ["schedule stats", "calendar stats"]):
                return await self._handle_schedule_stats()
            
            # Check availability
            elif any(keyword in query_lower for keyword in ["free time", "available time", "when am i free"]):
                return await self._handle_check_availability(user_input, context)
            
            # Default help
            else:
                return await self._handle_calendar_help()
                
        except Exception as e:
            self.logger.error(f"Error handling calendar query: {e}")
            return "I'm having trouble with calendar management right now. Please try again!"
    
    async def _handle_schedule_event(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle scheduling a new event"""
        # This is a simplified parser - could be enhanced with more sophisticated NLP
        input_lower = user_input.lower()
        
        # Extract title
        title = "New Event"
        for keyword in ["schedule", "book appointment", "add event", "create appointment"]:
            if keyword in input_lower:
                remaining = input_lower.replace(keyword, "").strip()
                if remaining:
                    # Extract title (first part before time/date indicators)
                    title_parts = remaining.split(" at ")[0].split(" on ")[0].split(" for ")[0]
                    title = title_parts.strip()
                break
        
        # Default scheduling for demonstration
        now = datetime.now()
        
        # Simple time extraction
        start_time = now + timedelta(hours=1)  # Default to 1 hour from now
        if "tomorrow" in input_lower:
            start_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif "at" in input_lower and any(time_word in input_lower for time_word in ["am", "pm", ":"]):
            # Basic time parsing - could be enhanced
            if "9am" in input_lower or "9 am" in input_lower:
                start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
            elif "2pm" in input_lower or "2 pm" in input_lower:
                start_time = now.replace(hour=14, minute=0, second=0, microsecond=0)
        
        # Extract location if mentioned
        location = ""
        if " at " in user_input and " at " != title:
            location_part = user_input.split(" at ")[-1]
            if not any(time_word in location_part.lower() for time_word in ["am", "pm", "o'clock"]):
                location = location_part.strip()
        
        event_id = await self.calendar_manager.create_event(
            title=title,
            start_time=start_time.isoformat(),
            description=f"Event created from: {user_input}",
            location=location
        )
        
        response = f"📅 **Event Scheduled Successfully!**\n\n"
        response += f"**Event ID:** {event_id}\n"
        response += f"**Title:** {title}\n"
        response += f"**Date & Time:** {start_time.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
        if location:
            response += f"**Location:** {location}\n"
        response += f"**Duration:** 1 hour (default)\n\n"
        response += f"💡 **Quick Actions:**\n"
        response += f"• 'Show schedule' to see all your events\n"
        response += f"• 'Cancel event: {title}' to cancel\n"
        response += f"• 'Today's schedule' for today's events"
        
        return response
    
    async def _handle_show_schedule(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle showing schedule"""
        # Determine date range
        query_lower = user_input.lower()
        
        if "today" in query_lower:
            target_date = datetime.now()
            events = await self.calendar_manager.get_events_for_date(target_date)
            date_str = "Today"
        elif "tomorrow" in query_lower:
            target_date = datetime.now() + timedelta(days=1)
            events = await self.calendar_manager.get_events_for_date(target_date)
            date_str = "Tomorrow"
        else:
            # Show upcoming events (default)
            events = await self.calendar_manager.get_upcoming_events(days=7)
            date_str = "Upcoming (Next 7 Days)"
        
        if not events:
            return f"📅 **{date_str} - No Events Scheduled**\n\nYou have a free schedule! Use 'Schedule [event] at [time]' to add appointments."
        
        response = f"📅 **Your Schedule - {date_str}** ({len(events)} events)\n\n"
        
        current_date = None
        for event in events:
            try:
                event_dt = datetime.fromisoformat(event.start_time)
                event_date = event_dt.date()
                
                # Add date header if different from previous
                if current_date != event_date:
                    if current_date is not None:
                        response += "\n"
                    response += f"**📆 {event_dt.strftime('%A, %B %d')}**\n"
                    current_date = event_date
                
                # Event details
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(event.priority, "⚪")
                response += f"{priority_emoji} **{event.title}**\n"
                response += f"   🕐 {event_dt.strftime('%I:%M %p')}"
                
                if event.location:
                    response += f" | 📍 {event.location}"
                response += f" | 🆔 {event.id}\n"
                
                if event.description and event.description != f"Event created from: {user_input}":
                    response += f"   📝 {event.description[:50]}...\n"
                
                if event.attendees:
                    response += f"   👥 {', '.join(event.attendees[:3])}\n"
                
                response += "\n"
                
            except Exception as e:
                continue
        
        response += "💡 **Quick Actions:**\n"
        response += "• 'Cancel event: [title]' to cancel an event\n"
        response += "• 'Schedule [event] at [time]' to add new event\n"
        response += "• 'Upcoming events' for next week's schedule"
        
        return response
    
    async def _handle_upcoming_events(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle upcoming events request"""
        # Extract time range if specified
        days = 7  # default
        if "week" in user_input.lower():
            days = 7
        elif "month" in user_input.lower():
            days = 30
        elif "today" in user_input.lower():
            days = 1
        
        events = await self.calendar_manager.get_upcoming_events(days=days)
        
        if not events:
            period = "week" if days == 7 else ("month" if days == 30 else "today")
            return f"📅 **No Upcoming Events**\n\nYou don't have any events scheduled for the next {period}. Perfect time to plan something!"
        
        response = f"⏰ **Upcoming Events** (Next {days} days - {len(events)} events)\n\n"
        
        # Group by urgency
        today = datetime.now().date()
        today_events = []
        tomorrow_events = []
        this_week_events = []
        later_events = []
        
        for event in events:
            try:
                event_date = datetime.fromisoformat(event.start_time).date()
                days_until = (event_date - today).days
                
                if days_until == 0:
                    today_events.append(event)
                elif days_until == 1:
                    tomorrow_events.append(event)
                elif days_until <= 7:
                    this_week_events.append(event)
                else:
                    later_events.append(event)
            except:
                continue
        
        # Display by priority
        if today_events:
            response += "🔴 **Today:**\n"
            for event in today_events:
                event_time = datetime.fromisoformat(event.start_time)
                response += f"• {event_time.strftime('%I:%M %p')} - {event.title}\n"
            response += "\n"
        
        if tomorrow_events:
            response += "🟡 **Tomorrow:**\n"
            for event in tomorrow_events:
                event_time = datetime.fromisoformat(event.start_time)
                response += f"• {event_time.strftime('%I:%M %p')} - {event.title}\n"
            response += "\n"
        
        if this_week_events:
            response += "🟢 **This Week:**\n"
            for event in this_week_events:
                event_time = datetime.fromisoformat(event.start_time)
                response += f"• {event_time.strftime('%a %m/%d %I:%M %p')} - {event.title}\n"
            response += "\n"
        
        if later_events:
            response += "📅 **Later:**\n"
            for event in later_events[:3]:  # Show first 3
                event_time = datetime.fromisoformat(event.start_time)
                response += f"• {event_time.strftime('%m/%d %I:%M %p')} - {event.title}\n"
            if len(later_events) > 3:
                response += f"... and {len(later_events) - 3} more\n"
        
        response += "\n💡 Use 'Show schedule today' or 'Show schedule tomorrow' for detailed views."
        
        return response
    
    async def _handle_today_schedule(self) -> str:
        """Handle today's schedule request"""
        today = datetime.now()
        events = await self.calendar_manager.get_events_for_date(today)
        
        if not events:
            return f"📅 **Today's Schedule - {today.strftime('%A, %B %d')}**\n\n🆓 **You're free today!** \n\nNo events scheduled. Perfect time for spontaneous activities or catching up on tasks!"
        
        response = f"📅 **Today's Schedule - {today.strftime('%A, %B %d')}** ({len(events)} events)\n\n"
        
        current_time = datetime.now()
        
        for event in events:
            try:
                event_time = datetime.fromisoformat(event.start_time)
                
                # Status indicator
                if event_time < current_time:
                    status_emoji = "✅"  # Past
                elif event_time <= current_time + timedelta(hours=1):
                    status_emoji = "🔔"  # Upcoming soon
                else:
                    status_emoji = "📌"  # Future
                
                response += f"{status_emoji} **{event.title}**\n"
                response += f"   🕐 {event_time.strftime('%I:%M %p')}"
                
                if event.location:
                    response += f" | 📍 {event.location}"
                
                # Time until event
                time_diff = event_time - current_time
                if time_diff.total_seconds() > 0:
                    hours = int(time_diff.total_seconds() // 3600)
                    minutes = int((time_diff.total_seconds() % 3600) // 60)
                    if hours > 0:
                        response += f" (in {hours}h {minutes}m)"
                    else:
                        response += f" (in {minutes}m)"
                
                response += "\n"
                
                if event.description and "Event created from:" not in event.description:
                    response += f"   📝 {event.description[:60]}...\n"
                
                response += "\n"
                
            except Exception as e:
                continue
        
        # Add helpful summary
        completed = sum(1 for e in events if datetime.fromisoformat(e.start_time) < current_time)
        remaining = len(events) - completed
        
        response += f"📊 **Summary:** {completed} completed, {remaining} remaining\n\n"
        response += "💡 Stay organized! Use 'Complete event: [title]' after meetings."
        
        return response
    
    async def _handle_tomorrow_schedule(self) -> str:
        """Handle tomorrow's schedule request"""
        tomorrow = datetime.now() + timedelta(days=1)
        events = await self.calendar_manager.get_events_for_date(tomorrow)
        
        if not events:
            return f"📅 **Tomorrow's Schedule - {tomorrow.strftime('%A, %B %d')}**\n\n🆓 **Free day tomorrow!** \n\nNo events scheduled. Good time to plan ahead or schedule important tasks."
        
        response = f"📅 **Tomorrow's Schedule - {tomorrow.strftime('%A, %B %d')}** ({len(events)} events)\n\n"
        
        for event in events:
            try:
                event_time = datetime.fromisoformat(event.start_time)
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(event.priority, "📌")
                
                response += f"{priority_emoji} **{event.title}**\n"
                response += f"   🕐 {event_time.strftime('%I:%M %p')}"
                
                if event.location:
                    response += f" | 📍 {event.location}"
                response += "\n"
                
                if event.description and "Event created from:" not in event.description:
                    response += f"   📝 {event.description[:60]}...\n"
                
                if event.attendees:
                    response += f"   👥 {', '.join(event.attendees[:2])}\n"
                
                response += "\n"
                
            except Exception as e:
                continue
        
        # Preparation tips
        high_priority = sum(1 for e in events if e.priority == "high")
        response += f"📊 **Tomorrow Summary:** {len(events)} events"
        if high_priority > 0:
            response += f", {high_priority} high priority"
        response += "\n\n"
        
        response += "💡 **Preparation Tips:**\n"
        response += "• Review locations and prepare for travel time\n"
        response += "• Check if any materials are needed\n"
        response += "• Set reminders for important meetings"
        
        return response
    
    async def _handle_cancel_event(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle cancelling an event"""
        # Extract event identifier
        event_id = user_input
        for keyword in ["cancel event", "cancel appointment", "remove event"]:
            event_id = event_id.lower().replace(keyword, "").strip()
        
        if not event_id:
            return "Please specify which event to cancel. Example: 'Cancel event: Team Meeting'"
        
        success = await self.calendar_manager.cancel_event(event_id)
        
        if success:
            return f"❌ **Event Cancelled**\n\nEvent '{event_id}' has been cancelled and removed from your schedule."
        else:
            return f"❌ **Event not found:** '{event_id}'\n\nTry 'Show schedule' to see available events."
    
    async def _handle_search_events(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle searching events"""
        # Extract search query
        query = user_input
        for keyword in ["find event", "search event", "look for appointment"]:
            query = query.lower().replace(keyword, "").strip()
        
        if not query:
            return "Please specify what to search for. Example: 'Find event: meeting'"
        
        results = await self.calendar_manager.search_events(query)
        
        if not results:
            return f"🔍 **No events found** for '{query}'\n\nTry a different search term or check your spelling."
        
        response = f"🔍 **Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for event in results[:5]:
            try:
                event_time = datetime.fromisoformat(event.start_time)
                status_emoji = {"scheduled": "📅", "completed": "✅", "cancelled": "❌"}.get(event.status, "📅")
                
                response += f"{status_emoji} **{event.title}**\n"
                response += f"   📅 {event_time.strftime('%A, %B %d at %I:%M %p')}\n"
                if event.location:
                    response += f"   📍 {event.location}\n"
                response += f"   📊 Status: {event.status.title()} | ID: {event.id}\n\n"
                
            except Exception as e:
                continue
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use the event ID to cancel or modify specific events."
        
        return response
    
    async def _handle_schedule_stats(self) -> str:
        """Handle schedule statistics request"""
        stats = self.calendar_manager.get_schedule_stats()
        
        response = f"📊 **Your Schedule Statistics**\n\n"
        response += f"**📈 Overview:**\n"
        response += f"• Total events: {stats['total_events']}\n"
        response += f"• Upcoming events: {stats['upcoming_events']}\n"
        response += f"• Completed events: {stats['completed_events']}\n"
        response += f"• Cancelled events: {stats['cancelled_events']}\n"
        response += f"• Events this week: {stats['events_this_week']}\n\n"
        
        if stats['events_by_category']:
            response += f"**📁 By Category:**\n"
            for category, count in stats['events_by_category'].items():
                response += f"• {category.title()}: {count} events\n"
            response += "\n"
        
        # Calculate productivity metrics
        total_scheduled = stats['completed_events'] + stats['cancelled_events']
        if total_scheduled > 0:
            completion_rate = round((stats['completed_events'] / total_scheduled) * 100, 1)
            response += f"**📈 Productivity:**\n"
            response += f"• Completion rate: {completion_rate}%\n"
            response += f"• Meeting reliability: {'Excellent' if completion_rate >= 90 else 'Good' if completion_rate >= 75 else 'Needs improvement'}\n\n"
        
        response += f"💡 **Schedule Insights:**\n"
        if stats['upcoming_events'] > 10:
            response += f"• You have a busy schedule ahead!\n"
        elif stats['upcoming_events'] < 3:
            response += f"• You have a light schedule - good time to plan new activities\n"
        else:
            response += f"• You have a well-balanced schedule\n"
        
        response += f"• Use categories to better organize your events\n"
        response += f"• Set reminders for important appointments"
        
        return response
    
    async def _handle_check_availability(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle checking availability/free time"""
        # For now, show today's gaps - could be enhanced to check specific dates
        today = datetime.now()
        events = await self.calendar_manager.get_events_for_date(today)
        
        if not events:
            return f"🆓 **You're completely free today!**\n\nNo events scheduled for {today.strftime('%A, %B %d')}. Perfect time for:\n• Planning new projects\n• Catching up on tasks\n• Scheduling important meetings"
        
        response = f"🕐 **Your Availability - {today.strftime('%A, %B %d')}**\n\n"
        
        # Sort events by time
        events.sort(key=lambda e: e.start_time)
        
        current_time = datetime.now()
        work_start = today.replace(hour=9, minute=0, second=0, microsecond=0)
        work_end = today.replace(hour=17, minute=0, second=0, microsecond=0)
        
        response += "**📅 Scheduled Events:**\n"
        for event in events:
            try:
                event_time = datetime.fromisoformat(event.start_time)
                response += f"• {event_time.strftime('%I:%M %p')} - {event.title}\n"
            except:
                continue
        
        response += "\n**🆓 Available Time Slots:**\n"
        
        # Simple gap detection
        if not events:
            response += f"• All day available!\n"
        else:
            # Check gaps between events (simplified)
            prev_end = work_start
            for event in events:
                try:
                    event_start = datetime.fromisoformat(event.start_time)
                    event_end = datetime.fromisoformat(event.end_time)
                    
                    if event_start > prev_end and (event_start - prev_end).total_seconds() > 3600:  # 1+ hour gap
                        response += f"• {prev_end.strftime('%I:%M %p')} - {event_start.strftime('%I:%M %p')} ({int((event_start - prev_end).total_seconds() // 3600)}h available)\n"
                    
                    prev_end = event_end
                except:
                    continue
            
            # Check if free after last event
            if prev_end < work_end:
                response += f"• {prev_end.strftime('%I:%M %p')} onwards (rest of day)\n"
        
        response += "\n💡 **Suggestions:**\n"
        response += "• Schedule important tasks during your longest free blocks\n"
        response += "• Keep some buffer time between meetings\n"
        response += "• Use 'Schedule [event] at [time]' to book appointments"
        
        return response
    
    async def _handle_calendar_help(self) -> str:
        """Provide calendar management help"""
        response = f"📅 **Calendar & Scheduling Help**\n\n"
        response += f"**📝 Scheduling Events:**\n"
        response += f"• 'Schedule meeting tomorrow at 2pm'\n"
        response += f"• 'Book appointment: Doctor visit at clinic'\n"
        response += f"• 'Add event: Team lunch at restaurant'\n\n"
        
        response += f"**📋 Viewing Schedule:**\n"
        response += f"• 'Show schedule' or 'My calendar'\n"
        response += f"• 'Today's schedule' or 'Tomorrow's schedule'\n"
        response += f"• 'Upcoming events' for next week\n"
        response += f"• 'Show schedule for [date]'\n\n"
        
        response += f"**🔍 Finding Events:**\n"
        response += f"• 'Find event: meeting' - Search by keyword\n"
        response += f"• 'Search event: doctor' - Find specific events\n\n"
        
        response += f"**⚙️ Managing Events:**\n"
        response += f"• 'Cancel event: [title]' - Cancel appointment\n"
        response += f"• 'Complete event: [title]' - Mark as done\n\n"
        
        response += f"**📊 Information:**\n"
        response += f"• 'Schedule stats' - Overview and statistics\n"
        response += f"• 'When am I free?' - Check availability\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Use descriptive event titles for easy finding\n"
        response += f"• Include locations for better organization\n"
        response += f"• Set reminders for important meetings\n"
        response += f"• Review tomorrow's schedule each evening"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_calendar_skill():
        skill = CalendarSkill()
        
        test_queries = [
            "schedule meeting tomorrow at 2pm",
            "today's schedule",
            "upcoming events",
            "schedule stats",
            "when am I free"
        ]
        
        print("🧪 Testing Calendar Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_calendar_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_calendar_skill())
