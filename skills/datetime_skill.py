"""
DateTime Skill for BUDDY AI Assistant
Handles date, time, and calendar-related queries
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class DateTimeSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("DateTimeSkill initialized.")
    
    def _get_current_datetime(self) -> datetime:
        """Get current date and time"""
        return datetime.now()
    
    def _format_date(self, dt: datetime, format_type: str = "full") -> str:
        """Format date based on type requested"""
        if format_type == "full":
            return dt.strftime("%A, %B %d, %Y")
        elif format_type == "short":
            return dt.strftime("%B %d, %Y")
        elif format_type == "numeric":
            return dt.strftime("%m/%d/%Y")
        elif format_type == "iso":
            return dt.strftime("%Y-%m-%d")
        else:
            return dt.strftime("%A, %B %d, %Y")
    
    def _format_time(self, dt: datetime, format_type: str = "12hour") -> str:
        """Format time based on type requested"""
        if format_type == "12hour":
            return dt.strftime("%I:%M %p")
        elif format_type == "24hour":
            return dt.strftime("%H:%M")
        else:
            return dt.strftime("%I:%M %p")
    
    def _get_day_info(self, dt: datetime) -> Dict[str, Any]:
        """Get detailed day information"""
        return {
            "day_name": dt.strftime("%A"),
            "day_number": dt.day,
            "month_name": dt.strftime("%B"),
            "month_number": dt.month,
            "year": dt.year,
            "day_of_year": dt.timetuple().tm_yday,
            "week_number": dt.isocalendar()[1],
            "quarter": (dt.month - 1) // 3 + 1
        }
    
    async def handle_datetime_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """
        Handle date and time related queries
        
        Args:
            user_input: The user's query
            context: Additional context information
            
        Returns:
            Formatted response with date/time information
        """
        try:
            self.logger.info(f"Processing datetime query: {user_input}")
            
            query_lower = user_input.lower().strip()
            current_dt = self._get_current_datetime()
            
            # Handle current date queries
            if any(keyword in query_lower for keyword in ["what is today", "today's date", "current date", "today date", "date today"]):
                return self._handle_current_date(current_dt)
            
            # Handle simple "date" query
            elif query_lower in ["date", "today", "what date"]:
                return self._handle_simple_date(current_dt)
            
            # Handle current time queries
            elif any(keyword in query_lower for keyword in ["what time", "current time", "time now", "what's the time"]):
                return self._handle_current_time(current_dt)
            
            # Handle day queries
            elif any(keyword in query_lower for keyword in ["what day", "day today", "today's day", "which day"]):
                return self._handle_day_query(current_dt)
            
            # Handle month queries
            elif any(keyword in query_lower for keyword in ["what month", "current month", "this month"]):
                return self._handle_month_query(current_dt)
            
            # Handle year queries
            elif any(keyword in query_lower for keyword in ["what year", "current year", "this year"]):
                return self._handle_year_query(current_dt)
            
            # Handle tomorrow/yesterday
            elif "tomorrow" in query_lower:
                tomorrow = current_dt + timedelta(days=1)
                return self._handle_relative_date(tomorrow, "Tomorrow")
            
            elif "yesterday" in query_lower:
                yesterday = current_dt - timedelta(days=1)
                return self._handle_relative_date(yesterday, "Yesterday")
            
            # Default comprehensive response
            else:
                return self._handle_comprehensive_datetime(current_dt)
                
        except Exception as e:
            self.logger.error(f"Error processing datetime query: {e}")
            return "I'm having trouble with the date/time information right now. Please try again!"
    
    def _handle_current_date(self, dt: datetime) -> str:
        """Handle current date requests"""
        day_info = self._get_day_info(dt)
        
        response = f"📅 **Today's Date**\n\n"
        response += f"**Full Date:** {self._format_date(dt, 'full')}\n"
        response += f"**Short Format:** {self._format_date(dt, 'short')}\n"
        response += f"**Numeric Format:** {self._format_date(dt, 'numeric')}\n\n"
        response += f"**Day Details:**\n"
        response += f"• Day: {day_info['day_name']} (Day {day_info['day_number']} of {day_info['month_name']})\n"
        response += f"• Week: Week {day_info['week_number']} of {day_info['year']}\n"
        response += f"• Day of Year: {day_info['day_of_year']} of 365\n"
        response += f"• Quarter: Q{day_info['quarter']} {day_info['year']}"
        
        return response
    
    def _handle_simple_date(self, dt: datetime) -> str:
        """Handle simple date requests"""
        return f"📅 **{self._format_date(dt, 'full')}**"
    
    def _handle_current_time(self, dt: datetime) -> str:
        """Handle current time requests"""
        response = f"🕐 **Current Time**\n\n"
        response += f"**12-Hour Format:** {self._format_time(dt, '12hour')}\n"
        response += f"**24-Hour Format:** {self._format_time(dt, '24hour')}\n\n"
        response += f"**Full DateTime:** {dt.strftime('%A, %B %d, %Y at %I:%M %p')}"
        
        return response
    
    def _handle_day_query(self, dt: datetime) -> str:
        """Handle day-specific queries"""
        day_info = self._get_day_info(dt)
        
        response = f"📆 **Today is {day_info['day_name']}**\n\n"
        response += f"**Full Date:** {self._format_date(dt, 'full')}\n"
        response += f"**Day Number:** {day_info['day_number']}\n"
        response += f"**Week Number:** Week {day_info['week_number']} of {day_info['year']}"
        
        return response
    
    def _handle_month_query(self, dt: datetime) -> str:
        """Handle month-specific queries"""
        day_info = self._get_day_info(dt)
        
        response = f"📅 **Current Month: {day_info['month_name']} {day_info['year']}**\n\n"
        response += f"**Month Number:** {day_info['month_number']}\n"
        response += f"**Quarter:** Q{day_info['quarter']}\n"
        response += f"**Today:** {day_info['day_name']}, {day_info['month_name']} {day_info['day_number']}"
        
        return response
    
    def _handle_year_query(self, dt: datetime) -> str:
        """Handle year-specific queries"""
        day_info = self._get_day_info(dt)
        
        response = f"📅 **Current Year: {day_info['year']}**\n\n"
        response += f"**Quarter:** Q{day_info['quarter']}\n"
        response += f"**Day of Year:** {day_info['day_of_year']} of 365\n"
        response += f"**Today:** {self._format_date(dt, 'full')}"
        
        return response
    
    def _handle_relative_date(self, dt: datetime, label: str) -> str:
        """Handle relative date queries (tomorrow, yesterday)"""
        day_info = self._get_day_info(dt)
        
        response = f"📅 **{label}**\n\n"
        response += f"**Date:** {self._format_date(dt, 'full')}\n"
        response += f"**Day:** {day_info['day_name']}\n"
        response += f"**Numeric:** {self._format_date(dt, 'numeric')}"
        
        return response
    
    def _handle_comprehensive_datetime(self, dt: datetime) -> str:
        """Handle comprehensive date/time requests"""
        day_info = self._get_day_info(dt)
        
        response = f"🕐 **Complete Date & Time Information**\n\n"
        response += f"**📅 Date:** {self._format_date(dt, 'full')}\n"
        response += f"**🕐 Time:** {self._format_time(dt, '12hour')}\n"
        response += f"**📆 Day:** {day_info['day_name']}\n"
        response += f"**📊 Week:** Week {day_info['week_number']} of {day_info['year']}\n"
        response += f"**📈 Quarter:** Q{day_info['quarter']} {day_info['year']}\n"
        response += f"**🎯 Day of Year:** {day_info['day_of_year']} of 365\n\n"
        response += f"**📋 Different Formats:**\n"
        response += f"• Short: {self._format_date(dt, 'short')}\n"
        response += f"• Numeric: {self._format_date(dt, 'numeric')}\n"
        response += f"• ISO: {self._format_date(dt, 'iso')}\n"
        response += f"• 24-hour time: {self._format_time(dt, '24hour')}"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_datetime_skill():
        skill = DateTimeSkill()
        
        test_queries = [
            "date",
            "what is today",
            "current time",
            "what day is today",
            "tomorrow",
            "yesterday"
        ]
        
        print("🧪 Testing DateTime Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_datetime_query(query, {})
            print(f"Response: {response}")
            print("-" * 40)
    
    asyncio.run(test_datetime_skill())
