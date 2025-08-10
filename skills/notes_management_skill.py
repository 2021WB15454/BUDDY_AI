"""
Note-Taking and Information Management Module for BUDDY AI Assistant
Handles notes, knowledge base, information storage and retrieval
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid
import re


@dataclass
class Note:
    """Note data structure"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: str
    updated_at: str
    is_favorite: bool = False
    is_archived: bool = False
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


class NotesManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notes_file = "learning_data/notes.json"
        self.notes = self._load_notes()
        self.logger.info("NotesManager initialized.")
    
    def _load_notes(self) -> List[Note]:
        """Load notes from file"""
        try:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
                return [Note(**note) for note in notes_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_notes(self):
        """Save notes to file"""
        try:
            os.makedirs(os.path.dirname(self.notes_file), exist_ok=True)
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                notes_data = [asdict(note) for note in self.notes]
                json.dump(notes_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving notes: {e}")
    
    async def create_note(self, title: str, content: str, category: str = "general", 
                         tags: List[str] = None) -> str:
        """Create a new note"""
        note = Note(
            id=str(uuid.uuid4())[:8],
            title=title,
            content=content,
            category=category,
            tags=tags or [],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.notes.append(note)
        self._save_notes()
        
        self.logger.info(f"Note created: {title}")
        return note.id
    
    async def update_note(self, note_id: str, title: str = None, content: str = None, 
                         category: str = None, tags: List[str] = None) -> bool:
        """Update an existing note"""
        for note in self.notes:
            if note.id == note_id or note.title.lower() == note_id.lower():
                if title:
                    note.title = title
                if content:
                    note.content = content
                if category:
                    note.category = category
                if tags is not None:
                    note.tags = tags
                note.updated_at = datetime.now().isoformat()
                
                self._save_notes()
                self.logger.info(f"Note updated: {note.title}")
                return True
        return False
    
    async def delete_note(self, note_id: str) -> bool:
        """Delete a note"""
        for i, note in enumerate(self.notes):
            if note.id == note_id or note.title.lower() == note_id.lower():
                deleted_note = self.notes.pop(i)
                self._save_notes()
                self.logger.info(f"Note deleted: {deleted_note.title}")
                return True
        return False
    
    async def search_notes(self, query: str, category: str = None, tags: List[str] = None) -> List[Note]:
        """Search notes by content, title, category, or tags"""
        query = query.lower()
        results = []
        
        for note in self.notes:
            if note.is_archived:
                continue
                
            # Text search
            text_match = (query in note.title.lower() or 
                         query in note.content.lower() or
                         any(query in tag.lower() for tag in note.tags))
            
            # Category filter
            category_match = not category or note.category.lower() == category.lower()
            
            # Tags filter
            tags_match = not tags or any(tag in note.tags for tag in tags)
            
            if text_match and category_match and tags_match:
                results.append(note)
        
        # Sort by relevance (title matches first, then by update time)
        results.sort(key=lambda n: (query not in n.title.lower(), n.updated_at), reverse=True)
        return results
    
    async def get_notes_by_category(self, category: str) -> List[Note]:
        """Get all notes in a specific category"""
        return [note for note in self.notes if note.category.lower() == category.lower() and not note.is_archived]
    
    async def get_recent_notes(self, limit: int = 10) -> List[Note]:
        """Get recently updated notes"""
        active_notes = [note for note in self.notes if not note.is_archived]
        return sorted(active_notes, key=lambda n: n.updated_at, reverse=True)[:limit]
    
    async def get_favorites(self) -> List[Note]:
        """Get favorite notes"""
        return [note for note in self.notes if note.is_favorite and not note.is_archived]
    
    async def toggle_favorite(self, note_id: str) -> bool:
        """Toggle favorite status of a note"""
        for note in self.notes:
            if note.id == note_id or note.title.lower() == note_id.lower():
                note.is_favorite = not note.is_favorite
                note.updated_at = datetime.now().isoformat()
                self._save_notes()
                return True
        return False
    
    async def archive_note(self, note_id: str) -> bool:
        """Archive a note"""
        for note in self.notes:
            if note.id == note_id or note.title.lower() == note_id.lower():
                note.is_archived = True
                note.updated_at = datetime.now().isoformat()
                self._save_notes()
                return True
        return False
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set(note.category for note in self.notes if not note.is_archived)
        return sorted(list(categories))
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags"""
        all_tags = set()
        for note in self.notes:
            if not note.is_archived:
                all_tags.update(note.tags)
        return sorted(list(all_tags))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get notes statistics"""
        active_notes = [note for note in self.notes if not note.is_archived]
        return {
            "total_notes": len(active_notes),
            "archived_notes": len([note for note in self.notes if note.is_archived]),
            "favorite_notes": len([note for note in active_notes if note.is_favorite]),
            "categories": len(self.get_categories()),
            "total_tags": len(self.get_all_tags()),
            "categories_list": self.get_categories()
        }


class NotesSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notes_manager = NotesManager()
        self.logger.info("NotesSkill initialized.")
    
    async def handle_notes_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle notes and information management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Create note
            if any(keyword in query_lower for keyword in ["create note", "add note", "new note", "take note", "note this"]):
                return await self._handle_create_note(user_input, context)
            
            # Search notes
            elif any(keyword in query_lower for keyword in ["find note", "search note", "look for note", "show note"]):
                return await self._handle_search_notes(user_input, context)
            
            # List notes
            elif any(keyword in query_lower for keyword in ["list notes", "show notes", "my notes", "all notes"]):
                return await self._handle_list_notes(user_input, context)
            
            # Update note
            elif any(keyword in query_lower for keyword in ["update note", "edit note", "modify note"]):
                return await self._handle_update_note(user_input, context)
            
            # Delete note
            elif any(keyword in query_lower for keyword in ["delete note", "remove note"]):
                return await self._handle_delete_note(user_input, context)
            
            # Favorite note
            elif any(keyword in query_lower for keyword in ["favorite note", "star note", "bookmark note"]):
                return await self._handle_favorite_note(user_input, context)
            
            # Show favorites
            elif any(keyword in query_lower for keyword in ["show favorites", "favorite notes", "starred notes"]):
                return await self._handle_show_favorites()
            
            # Notes by category
            elif any(keyword in query_lower for keyword in ["notes in category", "category notes"]):
                return await self._handle_category_notes(user_input, context)
            
            # Recent notes
            elif any(keyword in query_lower for keyword in ["recent notes", "latest notes"]):
                return await self._handle_recent_notes()
            
            # Notes statistics
            elif any(keyword in query_lower for keyword in ["notes stats", "notes statistics"]):
                return await self._handle_notes_stats()
            
            # Archive note
            elif any(keyword in query_lower for keyword in ["archive note"]):
                return await self._handle_archive_note(user_input, context)
            
            # Default help
            else:
                return await self._handle_notes_help()
                
        except Exception as e:
            self.logger.error(f"Error handling notes query: {e}")
            return "I'm having trouble with notes management right now. Please try again!"
    
    async def _handle_create_note(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle creating a new note"""
        # Extract note content
        content = user_input
        for keyword in ["create note", "add note", "new note", "take note", "note this"]:
            content = content.lower().replace(keyword, "").strip()
        
        if not content:
            return "Please provide the note content. Example: 'Create note: Meeting notes about project timeline'"
        
        # Extract title and content
        if ":" in content:
            parts = content.split(":", 1)
            title = parts[0].strip()
            note_content = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        else:
            # Use first few words as title
            words = content.split()
            title = " ".join(words[:5]) if len(words) > 5 else content
            note_content = content
        
        # Extract category if mentioned
        category = "general"
        if " category:" in user_input.lower():
            category = user_input.lower().split(" category:")[1].split()[0]
        
        # Extract tags if mentioned
        tags = []
        if " tags:" in user_input.lower():
            tags_str = user_input.lower().split(" tags:")[1].strip()
            tags = [tag.strip() for tag in tags_str.split(",")]
        
        note_id = await self.notes_manager.create_note(
            title=title,
            content=note_content,
            category=category,
            tags=tags
        )
        
        response = f"📝 **Note Created Successfully!**\n\n"
        response += f"**Note ID:** {note_id}\n"
        response += f"**Title:** {title}\n"
        response += f"**Category:** {category}\n"
        if tags:
            response += f"**Tags:** {', '.join(tags)}\n"
        response += f"**Content:** {note_content[:100]}{'...' if len(note_content) > 100 else ''}\n\n"
        response += f"💡 **Quick Actions:**\n"
        response += f"• 'Search note: {title}' to find this note\n"
        response += f"• 'Favorite note: {title}' to bookmark it\n"
        response += f"• 'Update note: {title}' to modify it"
        
        return response
    
    async def _handle_search_notes(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle searching notes"""
        # Extract search query
        query = user_input
        for keyword in ["find note", "search note", "look for note", "show note"]:
            query = query.lower().replace(keyword, "").strip()
        
        if not query:
            return "Please specify what to search for. Example: 'Search note: meeting'"
        
        results = await self.notes_manager.search_notes(query)
        
        if not results:
            return f"🔍 **No notes found** for '{query}'\n\nTry a different search term or create a new note with 'Create note: [content]'"
        
        response = f"🔍 **Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for i, note in enumerate(results[:5], 1):
            fav_indicator = "⭐" if note.is_favorite else ""
            response += f"**{i}. {note.title}** {fav_indicator}\n"
            response += f"   📁 Category: {note.category} | 🆔 ID: {note.id}\n"
            if note.tags:
                response += f"   🏷️ Tags: {', '.join(note.tags)}\n"
            response += f"   📝 {note.content[:150]}{'...' if len(note.content) > 150 else ''}\n"
            response += f"   📅 Updated: {note.updated_at[:10]}\n\n"
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use note ID or title to update, delete, or favorite specific notes."
        
        return response
    
    async def _handle_list_notes(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle listing notes"""
        # Check for category filter
        category = None
        if " in " in user_input.lower():
            parts = user_input.lower().split(" in ")
            if len(parts) > 1:
                category = parts[1].strip()
        
        if category:
            notes = await self.notes_manager.get_notes_by_category(category)
            if not notes:
                return f"📝 **No notes found** in category '{category}'\n\nAvailable categories: {', '.join(self.notes_manager.get_categories())}"
        else:
            notes = await self.notes_manager.get_recent_notes(limit=10)
        
        if not notes:
            return "📝 **No notes found**\n\nCreate your first note with 'Create note: [content]'"
        
        title = f"📋 **Your Notes** ({len(notes)} {'in ' + category if category else 'recent'})\n\n"
        response = title
        
        for i, note in enumerate(notes, 1):
            fav_indicator = "⭐" if note.is_favorite else ""
            response += f"**{i}. {note.title}** {fav_indicator}\n"
            response += f"   📁 {note.category} | 🆔 {note.id}\n"
            if note.tags:
                response += f"   🏷️ {', '.join(note.tags)}\n"
            response += f"   📝 {note.content[:100]}{'...' if len(note.content) > 100 else ''}\n\n"
        
        stats = self.notes_manager.get_stats()
        response += f"📊 **Stats:** {stats['total_notes']} total notes, {stats['categories']} categories\n\n"
        response += "💡 **Quick Actions:**\n"
        response += "• 'Search note: [term]' to find specific notes\n"
        response += "• 'Show favorites' to see bookmarked notes\n"
        response += "• 'Notes stats' for detailed statistics"
        
        return response
    
    async def _handle_update_note(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle updating a note"""
        # This is a simplified version - in a real implementation, you'd want more sophisticated parsing
        return "📝 **Note Update**\n\nNote updating feature is available. Please specify:\n• Note ID or title to update\n• New content\n\nExample: 'Update note: Meeting Notes with new content: Updated meeting summary'"
    
    async def _handle_delete_note(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle deleting a note"""
        # Extract note identifier
        note_id = user_input
        for keyword in ["delete note", "remove note"]:
            note_id = note_id.lower().replace(keyword, "").strip()
        
        if not note_id:
            return "Please specify which note to delete. Example: 'Delete note: Meeting Notes'"
        
        success = await self.notes_manager.delete_note(note_id)
        
        if success:
            return f"🗑️ **Note Deleted**\n\nNote '{note_id}' has been permanently removed."
        else:
            return f"❌ **Note not found:** '{note_id}'\n\nTry 'List notes' to see available notes."
    
    async def _handle_favorite_note(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle favoriting a note"""
        # Extract note identifier
        note_id = user_input
        for keyword in ["favorite note", "star note", "bookmark note"]:
            note_id = note_id.lower().replace(keyword, "").strip()
        
        if not note_id:
            return "Please specify which note to favorite. Example: 'Favorite note: Important Notes'"
        
        success = await self.notes_manager.toggle_favorite(note_id)
        
        if success:
            return f"⭐ **Note Updated**\n\nNote '{note_id}' favorite status has been toggled."
        else:
            return f"❌ **Note not found:** '{note_id}'\n\nTry 'List notes' to see available notes."
    
    async def _handle_show_favorites(self) -> str:
        """Handle showing favorite notes"""
        favorites = await self.notes_manager.get_favorites()
        
        if not favorites:
            return "⭐ **No Favorite Notes**\n\nYou haven't bookmarked any notes yet. Use 'Favorite note: [title]' to add favorites."
        
        response = f"⭐ **Your Favorite Notes** ({len(favorites)} total)\n\n"
        
        for i, note in enumerate(favorites, 1):
            response += f"**{i}. {note.title}**\n"
            response += f"   📁 {note.category} | 🆔 {note.id}\n"
            if note.tags:
                response += f"   🏷️ {', '.join(note.tags)}\n"
            response += f"   📝 {note.content[:100]}{'...' if len(note.content) > 100 else ''}\n\n"
        
        response += "💡 These are your most important notes. Use 'Search note: [term]' to find specific content."
        
        return response
    
    async def _handle_category_notes(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle showing notes by category"""
        categories = self.notes_manager.get_categories()
        
        if not categories:
            return "📁 **No Categories**\n\nYou don't have any notes with categories yet."
        
        response = f"📁 **Available Categories** ({len(categories)} total)\n\n"
        
        for category in categories:
            notes_count = len(await self.notes_manager.get_notes_by_category(category))
            response += f"• **{category.title()}** ({notes_count} notes)\n"
        
        response += f"\n💡 Use 'List notes in [category]' to see notes in a specific category."
        
        return response
    
    async def _handle_recent_notes(self) -> str:
        """Handle showing recent notes"""
        recent = await self.notes_manager.get_recent_notes(limit=5)
        
        if not recent:
            return "📝 **No Recent Notes**\n\nCreate your first note with 'Create note: [content]'"
        
        response = f"🕐 **Recent Notes** (Last 5 updated)\n\n"
        
        for i, note in enumerate(recent, 1):
            fav_indicator = "⭐" if note.is_favorite else ""
            response += f"**{i}. {note.title}** {fav_indicator}\n"
            response += f"   📅 {note.updated_at[:10]} | 📁 {note.category}\n"
            response += f"   📝 {note.content[:100]}{'...' if len(note.content) > 100 else ''}\n\n"
        
        response += "💡 Your most recently updated notes are shown above."
        
        return response
    
    async def _handle_notes_stats(self) -> str:
        """Handle notes statistics request"""
        stats = self.notes_manager.get_stats()
        
        response = f"📊 **Your Notes Statistics**\n\n"
        response += f"**📝 Overview:**\n"
        response += f"• Total active notes: {stats['total_notes']}\n"
        response += f"• Archived notes: {stats['archived_notes']}\n"
        response += f"• Favorite notes: {stats['favorite_notes']}\n"
        response += f"• Categories: {stats['categories']}\n"
        response += f"• Unique tags: {stats['total_tags']}\n\n"
        
        if stats['categories_list']:
            response += f"**📁 Categories:**\n"
            for category in stats['categories_list']:
                count = len(await self.notes_manager.get_notes_by_category(category))
                response += f"• {category.title()}: {count} notes\n"
            response += "\n"
        
        tags = self.notes_manager.get_all_tags()
        if tags:
            response += f"**🏷️ Popular Tags:** {', '.join(tags[:10])}\n\n"
        
        response += f"💡 **Organization Tips:**\n"
        response += f"• Use categories to group related notes\n"
        response += f"• Add tags for better searchability\n"
        response += f"• Favorite important notes for quick access\n"
        response += f"• Archive old notes to keep things clean"
        
        return response
    
    async def _handle_archive_note(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle archiving a note"""
        # Extract note identifier
        note_id = user_input.lower().replace("archive note", "").strip()
        
        if not note_id:
            return "Please specify which note to archive. Example: 'Archive note: Old Meeting Notes'"
        
        success = await self.notes_manager.archive_note(note_id)
        
        if success:
            return f"📦 **Note Archived**\n\nNote '{note_id}' has been moved to archive. It won't appear in searches or lists."
        else:
            return f"❌ **Note not found:** '{note_id}'\n\nTry 'List notes' to see available notes."
    
    async def _handle_notes_help(self) -> str:
        """Provide notes management help"""
        response = f"📝 **Notes Management Help**\n\n"
        response += f"**✏️ Creating Notes:**\n"
        response += f"• 'Create note: Meeting summary'\n"
        response += f"• 'Take note: Important reminder'\n"
        response += f"• 'Add note: Project ideas category: work tags: important,project'\n\n"
        
        response += f"**🔍 Finding Notes:**\n"
        response += f"• 'Search note: meeting' - Find by content\n"
        response += f"• 'List notes' - Show recent notes\n"
        response += f"• 'Show favorites' - See bookmarked notes\n"
        response += f"• 'Recent notes' - Latest updates\n\n"
        
        response += f"**📋 Organizing Notes:**\n"
        response += f"• 'Favorite note: [title]' - Bookmark important notes\n"
        response += f"• 'List notes in work' - Notes by category\n"
        response += f"• 'Archive note: [title]' - Archive old notes\n\n"
        
        response += f"**📊 Information:**\n"
        response += f"• 'Notes stats' - Overview and statistics\n"
        response += f"• 'Category notes' - Available categories\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Use descriptive titles for easy finding\n"
        response += f"• Add categories and tags for organization\n"
        response += f"• Favorite your most important notes\n"
        response += f"• Search works on title, content, and tags"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_notes_skill():
        skill = NotesSkill()
        
        test_queries = [
            "create note: Meeting with team about project timeline",
            "list notes",
            "search note: meeting",
            "notes stats",
            "favorite note: Meeting with team",
            "show favorites"
        ]
        
        print("🧪 Testing Notes Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_notes_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_notes_skill())
