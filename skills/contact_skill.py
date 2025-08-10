"""
Contact Management Module for BUDDY AI Assistant
Handles contact storage, search, organization, and communication tracking
"""

import asyncio
import logging
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid


@dataclass
class Contact:
    """Contact data structure"""
    id: str
    first_name: str
    last_name: str
    display_name: str
    email: str
    phone: str
    company: str
    title: str
    address: str
    birthday: str
    notes: str
    tags: List[str]
    groups: List[str]
    social_links: Dict[str, str]  # platform: url
    last_contact: str
    contact_frequency: int  # days between contacts
    importance: str  # high, medium, low
    created_at: str
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.display_name:
            self.display_name = f"{self.first_name} {self.last_name}".strip()


@dataclass
class ContactInteraction:
    """Contact interaction/communication log"""
    id: str
    contact_id: str
    interaction_type: str  # call, email, meeting, text, other
    direction: str  # incoming, outgoing
    subject: str
    notes: str
    date: str
    duration_minutes: int
    outcome: str
    follow_up_needed: bool
    follow_up_date: str
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().isoformat()


class ContactManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contacts_file = "learning_data/contacts.json"
        self.interactions_file = "learning_data/contact_interactions.json"
        self.contacts = self._load_contacts()
        self.interactions = self._load_interactions()
        self.logger.info("ContactManager initialized.")
    
    def _load_contacts(self) -> List[Contact]:
        """Load contacts from file"""
        try:
            with open(self.contacts_file, 'r', encoding='utf-8') as f:
                contacts_data = json.load(f)
                return [Contact(**contact) for contact in contacts_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_interactions(self) -> List[ContactInteraction]:
        """Load interactions from file"""
        try:
            with open(self.interactions_file, 'r', encoding='utf-8') as f:
                interactions_data = json.load(f)
                return [ContactInteraction(**interaction) for interaction in interactions_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_contacts(self):
        """Save contacts to file"""
        try:
            os.makedirs(os.path.dirname(self.contacts_file), exist_ok=True)
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                contacts_data = [asdict(contact) for contact in self.contacts]
                json.dump(contacts_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving contacts: {e}")
    
    def _save_interactions(self):
        """Save interactions to file"""
        try:
            os.makedirs(os.path.dirname(self.interactions_file), exist_ok=True)
            with open(self.interactions_file, 'w', encoding='utf-8') as f:
                interactions_data = [asdict(interaction) for interaction in self.interactions]
                json.dump(interactions_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving interactions: {e}")
    
    def _parse_phone_number(self, phone: str) -> str:
        """Clean and format phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Format based on length
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return phone  # Return as-is if can't format
    
    def _validate_email(self, email: str) -> bool:
        """Basic email validation"""
        if not email:
            return True  # Empty email is allowed
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def add_contact(self, first_name: str, last_name: str = "", email: str = "",
                         phone: str = "", company: str = "", title: str = "",
                         address: str = "", birthday: str = "", notes: str = "",
                         tags: List[str] = None, groups: List[str] = None,
                         importance: str = "medium") -> str:
        """Add a new contact"""
        
        # Validate required fields
        if not first_name.strip():
            raise ValueError("First name is required")
        
        if email and not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        # Check for duplicates
        display_name = f"{first_name} {last_name}".strip()
        for contact in self.contacts:
            if (contact.display_name.lower() == display_name.lower() or
                (email and contact.email.lower() == email.lower()) or
                (phone and contact.phone == self._parse_phone_number(phone))):
                raise ValueError(f"Contact already exists: {contact.display_name}")
        
        contact = Contact(
            id=str(uuid.uuid4())[:8],
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            display_name=display_name,
            email=email.strip().lower(),
            phone=self._parse_phone_number(phone),
            company=company.strip(),
            title=title.strip(),
            address=address.strip(),
            birthday=birthday.strip(),
            notes=notes.strip(),
            tags=tags or [],
            groups=groups or [],
            social_links={},
            last_contact="",
            contact_frequency=30,  # Default 30 days
            importance=importance.lower(),
            created_at=datetime.now().isoformat()
        )
        
        self.contacts.append(contact)
        self._save_contacts()
        
        self.logger.info(f"Contact added: {display_name}")
        return contact.id
    
    async def find_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name, email, company, or other fields"""
        if not query:
            return []
        
        query = query.lower()
        results = []
        
        for contact in self.contacts:
            if (query in contact.display_name.lower() or
                query in contact.first_name.lower() or
                query in contact.last_name.lower() or
                query in contact.email.lower() or
                query in contact.company.lower() or
                query in contact.title.lower() or
                query in contact.phone or
                any(query in tag.lower() for tag in contact.tags) or
                any(query in group.lower() for group in contact.groups) or
                query in contact.notes.lower()):
                results.append(contact)
        
        # Sort by relevance (exact name matches first)
        results.sort(key=lambda c: (
            0 if query in c.display_name.lower() else
            1 if query in c.first_name.lower() or query in c.last_name.lower() else
            2 if query in c.email.lower() else 3
        ))
        
        return results
    
    async def get_contact_by_id(self, contact_id: str) -> Optional[Contact]:
        """Get contact by ID or name"""
        # Try by ID first
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        
        # Try by name
        for contact in self.contacts:
            if contact.display_name.lower() == contact_id.lower():
                return contact
        
        return None
    
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> bool:
        """Update contact information"""
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            return False
        
        # Update fields
        for field, value in updates.items():
            if hasattr(contact, field):
                if field == "phone":
                    setattr(contact, field, self._parse_phone_number(value))
                elif field == "email" and value and not self._validate_email(value):
                    continue  # Skip invalid email
                else:
                    setattr(contact, field, value)
        
        # Update display name if name changed
        if "first_name" in updates or "last_name" in updates:
            contact.display_name = f"{contact.first_name} {contact.last_name}".strip()
        
        self._save_contacts()
        self.logger.info(f"Contact updated: {contact.display_name}")
        return True
    
    async def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact"""
        for i, contact in enumerate(self.contacts):
            if contact.id == contact_id or contact.display_name.lower() == contact_id.lower():
                deleted_contact = self.contacts.pop(i)
                self._save_contacts()
                
                # Also delete related interactions
                self.interactions = [i for i in self.interactions if i.contact_id != deleted_contact.id]
                self._save_interactions()
                
                self.logger.info(f"Contact deleted: {deleted_contact.display_name}")
                return True
        return False
    
    async def add_interaction(self, contact_id: str, interaction_type: str, direction: str,
                            subject: str = "", notes: str = "", duration_minutes: int = 0,
                            outcome: str = "", follow_up_needed: bool = False,
                            follow_up_date: str = "") -> str:
        """Log an interaction with a contact"""
        
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            raise ValueError(f"Contact not found: {contact_id}")
        
        interaction = ContactInteraction(
            id=str(uuid.uuid4())[:8],
            contact_id=contact.id,
            interaction_type=interaction_type.lower(),
            direction=direction.lower(),
            subject=subject.strip(),
            notes=notes.strip(),
            date=datetime.now().isoformat(),
            duration_minutes=duration_minutes,
            outcome=outcome.strip(),
            follow_up_needed=follow_up_needed,
            follow_up_date=follow_up_date
        )
        
        self.interactions.append(interaction)
        self._save_interactions()
        
        # Update last contact date
        contact.last_contact = datetime.now().isoformat()
        self._save_contacts()
        
        self.logger.info(f"Interaction logged: {interaction_type} with {contact.display_name}")
        return interaction.id
    
    async def get_contact_interactions(self, contact_id: str) -> List[ContactInteraction]:
        """Get all interactions for a specific contact"""
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            return []
        
        contact_interactions = [i for i in self.interactions if i.contact_id == contact.id]
        contact_interactions.sort(key=lambda i: i.date, reverse=True)  # Most recent first
        return contact_interactions
    
    async def get_contacts_by_group(self, group: str) -> List[Contact]:
        """Get all contacts in a specific group"""
        return [c for c in self.contacts if group.lower() in [g.lower() for g in c.groups]]
    
    async def get_contacts_by_tag(self, tag: str) -> List[Contact]:
        """Get all contacts with a specific tag"""
        return [c for c in self.contacts if tag.lower() in [t.lower() for t in c.tags]]
    
    async def get_overdue_contacts(self) -> List[Contact]:
        """Get contacts that haven't been contacted recently"""
        now = datetime.now()
        overdue = []
        
        for contact in self.contacts:
            if contact.last_contact:
                try:
                    last_contact_date = datetime.fromisoformat(contact.last_contact)
                    days_since = (now - last_contact_date).days
                    if days_since >= contact.contact_frequency:
                        overdue.append(contact)
                except:
                    continue
            else:
                # Never contacted
                created_date = datetime.fromisoformat(contact.created_at)
                days_since = (now - created_date).days
                if days_since >= contact.contact_frequency:
                    overdue.append(contact)
        
        # Sort by importance and days overdue
        overdue.sort(key=lambda c: (
            0 if c.importance == "high" else 1 if c.importance == "medium" else 2,
            c.contact_frequency
        ))
        
        return overdue
    
    async def get_upcoming_birthdays(self, days: int = 30) -> List[Contact]:
        """Get contacts with birthdays in the next N days"""
        if not days:
            days = 30
        
        upcoming = []
        today = datetime.now().date()
        
        for contact in self.contacts:
            if contact.birthday:
                try:
                    # Parse birthday (assuming MM-DD or MM/DD format)
                    if "/" in contact.birthday:
                        month, day = map(int, contact.birthday.split("/"))
                    elif "-" in contact.birthday:
                        month, day = map(int, contact.birthday.split("-"))
                    else:
                        continue
                    
                    # Create birthday for this year
                    birthday_this_year = today.replace(month=month, day=day)
                    
                    # If birthday already passed this year, use next year
                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                    
                    days_until = (birthday_this_year - today).days
                    if 0 <= days_until <= days:
                        upcoming.append((contact, days_until))
                        
                except Exception:
                    continue
        
        # Sort by days until birthday
        upcoming.sort(key=lambda x: x[1])
        return [contact for contact, days in upcoming]
    
    def get_contact_stats(self) -> Dict[str, Any]:
        """Get contact management statistics"""
        # Basic counts
        total_contacts = len(self.contacts)
        total_interactions = len(self.interactions)
        
        # Groups and tags
        all_groups = set()
        all_tags = set()
        for contact in self.contacts:
            all_groups.update(contact.groups)
            all_tags.update(contact.tags)
        
        # Interactions by type
        interaction_types = {}
        for interaction in self.interactions:
            interaction_types[interaction.interaction_type] = interaction_types.get(interaction.interaction_type, 0) + 1
        
        # Contacts by importance
        importance_counts = {"high": 0, "medium": 0, "low": 0}
        for contact in self.contacts:
            importance_counts[contact.importance] = importance_counts.get(contact.importance, 0) + 1
        
        # Recent activity
        now = datetime.now()
        recent_interactions = len([i for i in self.interactions 
                                 if (now - datetime.fromisoformat(i.date)).days <= 7])
        
        return {
            "total_contacts": total_contacts,
            "total_interactions": total_interactions,
            "total_groups": len(all_groups),
            "total_tags": len(all_tags),
            "groups": list(all_groups),
            "tags": list(all_tags),
            "interaction_types": interaction_types,
            "importance_breakdown": importance_counts,
            "recent_interactions": recent_interactions,
            "avg_interactions_per_contact": round(total_interactions / total_contacts, 1) if total_contacts > 0 else 0
        }


class ContactSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contact_manager = ContactManager()
        self.logger.info("ContactSkill initialized.")
    
    async def handle_contact_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle contact management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Add new contact
            if any(keyword in query_lower for keyword in ["add contact", "new contact", "create contact"]):
                return await self._handle_add_contact(user_input, context)
            
            # Find/search contacts
            elif any(keyword in query_lower for keyword in ["find contact", "search contact", "look for", "contact info"]):
                return await self._handle_find_contact(user_input, context)
            
            # Show all contacts
            elif any(keyword in query_lower for keyword in ["show contacts", "list contacts", "all contacts", "my contacts"]):
                return await self._handle_list_contacts(user_input, context)
            
            # Log interaction
            elif any(keyword in query_lower for keyword in ["log call", "log meeting", "log email", "contacted"]):
                return await self._handle_log_interaction(user_input, context)
            
            # Update contact
            elif any(keyword in query_lower for keyword in ["update contact", "edit contact", "change contact"]):
                return await self._handle_update_contact(user_input, context)
            
            # Delete contact
            elif any(keyword in query_lower for keyword in ["delete contact", "remove contact"]):
                return await self._handle_delete_contact(user_input, context)
            
            # Show contact history
            elif any(keyword in query_lower for keyword in ["contact history", "interaction history", "communication history"]):
                return await self._handle_contact_history(user_input, context)
            
            # Groups and tags
            elif any(keyword in query_lower for keyword in ["group", "tag"]):
                return await self._handle_groups_tags(user_input, context)
            
            # Birthdays
            elif any(keyword in query_lower for keyword in ["birthday", "birthdays"]):
                return await self._handle_birthdays(user_input, context)
            
            # Overdue contacts
            elif any(keyword in query_lower for keyword in ["overdue contact", "follow up", "need to contact"]):
                return await self._handle_overdue_contacts()
            
            # Contact statistics
            elif any(keyword in query_lower for keyword in ["contact stats", "contact statistics"]):
                return await self._handle_contact_stats()
            
            # Default help
            else:
                return await self._handle_contact_help()
                
        except Exception as e:
            self.logger.error(f"Error handling contact query: {e}")
            return "I'm having trouble with contact management right now. Please try again!"
    
    async def _handle_add_contact(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle adding a new contact"""
        # Basic parsing - could be enhanced with more sophisticated NLP
        input_lower = user_input.lower()
        
        # Extract name (simplified parsing)
        name_part = input_lower
        for keyword in ["add contact", "new contact", "create contact"]:
            name_part = name_part.replace(keyword, "").strip()
        
        if not name_part:
            return ("📱 **Add New Contact**\n\n"
                   "Please provide contact details. Example:\n"
                   "'Add contact: John Smith, email: john@example.com, phone: 555-0123'\n\n"
                   "**Required:** Name\n"
                   "**Optional:** Email, phone, company, title")
        
        # Parse contact details
        details = {"first_name": "", "last_name": "", "email": "", "phone": "", 
                  "company": "", "title": "", "notes": ""}
        
        # Split by common separators
        parts = re.split(r'[,;]', name_part)
        
        # First part is usually the name
        if parts:
            name_parts = parts[0].strip().split()
            details["first_name"] = name_parts[0] if name_parts else ""
            details["last_name"] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        # Extract other details
        for part in parts[1:]:
            part = part.strip().lower()
            if "email" in part:
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', part)
                if email_match:
                    details["email"] = email_match.group()
            elif "phone" in part:
                phone_match = re.search(r'[\d\-\(\)\s]+', part)
                if phone_match:
                    details["phone"] = phone_match.group().strip()
            elif "company" in part:
                details["company"] = part.replace("company", "").replace(":", "").strip()
            elif "title" in part:
                details["title"] = part.replace("title", "").replace(":", "").strip()
        
        if not details["first_name"]:
            return "❌ **Error:** Contact name is required. Please specify at least a first name."
        
        try:
            contact_id = await self.contact_manager.add_contact(
                first_name=details["first_name"],
                last_name=details["last_name"],
                email=details["email"],
                phone=details["phone"],
                company=details["company"],
                title=details["title"],
                notes=f"Added via: {user_input}"
            )
            
            response = f"✅ **Contact Added Successfully!**\n\n"
            response += f"**Name:** {details['first_name']} {details['last_name']}\n"
            response += f"**Contact ID:** {contact_id}\n"
            
            if details["email"]:
                response += f"**Email:** {details['email']}\n"
            if details["phone"]:
                response += f"**Phone:** {details['phone']}\n"
            if details["company"]:
                response += f"**Company:** {details['company']}\n"
            if details["title"]:
                response += f"**Title:** {details['title']}\n"
            
            response += f"\n💡 **Next Steps:**\n"
            response += f"• 'Update contact: {details['first_name']}' to add more details\n"
            response += f"• 'Log interaction' to track communications\n"
            response += f"• 'Find contact: {details['first_name']}' to view info"
            
            return response
            
        except ValueError as e:
            return f"❌ **Error:** {str(e)}"
    
    async def _handle_find_contact(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle finding/searching contacts"""
        # Extract search query
        query = user_input.lower()
        for keyword in ["find contact", "search contact", "look for", "contact info"]:
            query = query.replace(keyword, "").strip()
        
        if not query:
            return ("🔍 **Search Contacts**\n\n"
                   "Please specify what to search for. Examples:\n"
                   "• 'Find contact: John'\n"
                   "• 'Search contact: @company.com'\n"
                   "• 'Look for: Smith'")
        
        results = await self.contact_manager.find_contacts(query)
        
        if not results:
            return f"🔍 **No contacts found** for '{query}'\n\nTry a different search term or check spelling."
        
        response = f"🔍 **Search Results** for '{query}' ({len(results)} found)\n\n"
        
        for contact in results[:5]:  # Show top 5 results
            response += f"👤 **{contact.display_name}**\n"
            
            if contact.email:
                response += f"   📧 {contact.email}\n"
            if contact.phone:
                response += f"   📞 {contact.phone}\n"
            if contact.company:
                response += f"   🏢 {contact.company}"
                if contact.title:
                    response += f" - {contact.title}"
                response += "\n"
            
            if contact.tags:
                response += f"   🏷️ Tags: {', '.join(contact.tags)}\n"
            
            # Last contact info
            if contact.last_contact:
                try:
                    last_date = datetime.fromisoformat(contact.last_contact)
                    days_ago = (datetime.now() - last_date).days
                    response += f"   📅 Last contact: {days_ago} days ago\n"
                except:
                    pass
            
            response += f"   🆔 ID: {contact.id}\n\n"
        
        if len(results) > 5:
            response += f"... and {len(results) - 5} more results.\n\n"
        
        response += "💡 Use contact ID or name for detailed operations like updating or viewing history."
        
        return response
    
    async def _handle_list_contacts(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle listing all contacts"""
        contacts = self.contact_manager.contacts
        
        if not contacts:
            return ("📱 **No Contacts Found**\n\n"
                   "You haven't added any contacts yet.\n"
                   "Use 'Add contact: [name]' to get started!")
        
        # Sort contacts by name
        contacts.sort(key=lambda c: c.display_name.lower())
        
        response = f"📱 **Your Contacts** ({len(contacts)} total)\n\n"
        
        # Group by first letter
        current_letter = ""
        for contact in contacts:
            first_letter = contact.display_name[0].upper()
            if first_letter != current_letter:
                response += f"**{first_letter}**\n"
                current_letter = first_letter
            
            response += f"• {contact.display_name}"
            
            if contact.company:
                response += f" ({contact.company})"
            
            if contact.phone:
                response += f" - {contact.phone}"
            
            # Importance indicator
            if contact.importance == "high":
                response += " ⭐"
            
            response += "\n"
        
        response += f"\n📊 **Quick Stats:**\n"
        stats = self.contact_manager.get_contact_stats()
        response += f"• Total contacts: {stats['total_contacts']}\n"
        response += f"• High priority: {stats['importance_breakdown']['high']}\n"
        response += f"• Total groups: {stats['total_groups']}\n"
        response += f"• Recent interactions: {stats['recent_interactions']}\n\n"
        
        response += "💡 Use 'Find contact: [name]' for detailed info or 'Contact stats' for full overview."
        
        return response
    
    async def _handle_log_interaction(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle logging contact interaction"""
        # Basic parsing for demonstration
        input_lower = user_input.lower()
        
        # Extract interaction type
        interaction_type = "other"
        if "call" in input_lower:
            interaction_type = "call"
        elif "email" in input_lower:
            interaction_type = "email"
        elif "meeting" in input_lower:
            interaction_type = "meeting"
        elif "text" in input_lower:
            interaction_type = "text"
        
        # For demo, use a simple format
        return ("📞 **Log Contact Interaction**\n\n"
               "Feature coming soon! This will allow you to:\n\n"
               "• Track all communications with contacts\n"
               "• Log call duration and outcomes\n"
               "• Set follow-up reminders\n"
               "• View interaction history\n\n"
               "Example usage:\n"
               "'Log call with John Smith - discussed project timeline'")
    
    async def _handle_update_contact(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle updating contact information"""
        return ("✏️ **Update Contact**\n\n"
               "Feature in development! This will allow you to:\n\n"
               "• Modify contact details\n"
               "• Add/remove tags and groups\n"
               "• Update company information\n"
               "• Change importance levels\n\n"
               "Use 'Find contact: [name]' to view current information.")
    
    async def _handle_delete_contact(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle deleting a contact"""
        # Extract contact identifier
        contact_id = user_input.lower()
        for keyword in ["delete contact", "remove contact"]:
            contact_id = contact_id.replace(keyword, "").strip()
        
        if not contact_id:
            return "Please specify which contact to delete. Example: 'Delete contact: John Smith'"
        
        success = await self.contact_manager.delete_contact(contact_id)
        
        if success:
            return f"🗑️ **Contact Deleted**\n\nContact '{contact_id}' has been permanently removed from your address book."
        else:
            return f"❌ **Contact not found:** '{contact_id}'\n\nUse 'Find contact: [name]' to check available contacts."
    
    async def _handle_contact_history(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle viewing contact interaction history"""
        return ("📈 **Contact History**\n\n"
               "Feature coming soon! This will show:\n\n"
               "• Complete interaction timeline\n"
               "• Communication frequency analysis\n"
               "• Follow-up reminders\n"
               "• Relationship strength indicators\n\n"
               "Use contact ID or name to view specific history.")
    
    async def _handle_groups_tags(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle groups and tags operations"""
        stats = self.contact_manager.get_contact_stats()
        
        response = f"🏷️ **Contact Organization**\n\n"
        
        if stats['groups']:
            response += f"**📁 Groups ({len(stats['groups'])}):**\n"
            for group in sorted(stats['groups']):
                group_contacts = await self.contact_manager.get_contacts_by_group(group)
                response += f"• {group} ({len(group_contacts)} contacts)\n"
            response += "\n"
        else:
            response += "**📁 Groups:** None created yet\n\n"
        
        if stats['tags']:
            response += f"**🏷️ Tags ({len(stats['tags'])}):**\n"
            for tag in sorted(stats['tags']):
                tag_contacts = await self.contact_manager.get_contacts_by_tag(tag)
                response += f"• #{tag} ({len(tag_contacts)} contacts)\n"
            response += "\n"
        else:
            response += "**🏷️ Tags:** None created yet\n\n"
        
        response += "💡 **Organization Tips:**\n"
        response += "• Use groups for categories: Family, Work, Friends\n"
        response += "• Use tags for attributes: VIP, Local, Client\n"
        response += "• Organize for easier searching and management"
        
        return response
    
    async def _handle_birthdays(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle birthday-related queries"""
        upcoming = await self.contact_manager.get_upcoming_birthdays(30)
        
        if not upcoming:
            return ("🎂 **Upcoming Birthdays**\n\n"
                   "No birthdays in the next 30 days.\n"
                   "Add birthday information to contacts to see upcoming celebrations!")
        
        response = f"🎂 **Upcoming Birthdays** (Next 30 days - {len(upcoming)} contacts)\n\n"
        
        today = datetime.now().date()
        
        for contact in upcoming:
            try:
                if "/" in contact.birthday:
                    month, day = map(int, contact.birthday.split("/"))
                elif "-" in contact.birthday:
                    month, day = map(int, contact.birthday.split("-"))
                else:
                    continue
                
                birthday_this_year = today.replace(month=month, day=day)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                days_until = (birthday_this_year - today).days
                
                if days_until == 0:
                    response += f"🎉 **TODAY** - {contact.display_name}\n"
                elif days_until == 1:
                    response += f"📅 **Tomorrow** - {contact.display_name}\n"
                else:
                    response += f"📅 **{birthday_this_year.strftime('%m/%d')}** ({days_until} days) - {contact.display_name}\n"
                
                if contact.phone:
                    response += f"   📞 {contact.phone}\n"
                if contact.email:
                    response += f"   📧 {contact.email}\n"
                response += "\n"
                
            except Exception:
                continue
        
        response += "💡 Set reminders to wish them happy birthday and strengthen relationships!"
        
        return response
    
    async def _handle_overdue_contacts(self) -> str:
        """Handle showing overdue contacts that need follow-up"""
        overdue = await self.contact_manager.get_overdue_contacts()
        
        if not overdue:
            return ("✅ **All Caught Up!**\n\n"
                   "You're up to date with all your important contacts.\n"
                   "Great job maintaining your relationships!")
        
        response = f"⏰ **Contacts Needing Follow-up** ({len(overdue)} contacts)\n\n"
        
        for contact in overdue[:10]:  # Show top 10
            days_overdue = 0
            if contact.last_contact:
                try:
                    last_date = datetime.fromisoformat(contact.last_contact)
                    days_overdue = (datetime.now() - last_date).days
                except:
                    pass
            else:
                created_date = datetime.fromisoformat(contact.created_at)
                days_overdue = (datetime.now() - created_date).days
            
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(contact.importance, "⚪")
            
            response += f"{priority_emoji} **{contact.display_name}**\n"
            response += f"   ⏰ {days_overdue} days since last contact"
            
            if contact.company:
                response += f" | 🏢 {contact.company}"
            
            response += f"\n   📞 {contact.phone}" if contact.phone else ""
            response += f"   📧 {contact.email}" if contact.email else ""
            response += "\n\n"
        
        if len(overdue) > 10:
            response += f"... and {len(overdue) - 10} more contacts\n\n"
        
        response += "💡 **Suggestions:**\n"
        response += "• Prioritize high importance contacts (🔴)\n"
        response += "• Send a quick message or make a call\n"
        response += "• Log interactions to track follow-ups"
        
        return response
    
    async def _handle_contact_stats(self) -> str:
        """Handle contact statistics request"""
        stats = self.contact_manager.get_contact_stats()
        
        response = f"📊 **Contact Management Statistics**\n\n"
        
        response += f"**📈 Overview:**\n"
        response += f"• Total contacts: {stats['total_contacts']}\n"
        response += f"• Total interactions: {stats['total_interactions']}\n"
        response += f"• Groups: {stats['total_groups']}\n"
        response += f"• Tags: {stats['total_tags']}\n"
        response += f"• Avg interactions per contact: {stats['avg_interactions_per_contact']}\n\n"
        
        response += f"**🎯 By Importance:**\n"
        response += f"• High priority: {stats['importance_breakdown']['high']} contacts\n"
        response += f"• Medium priority: {stats['importance_breakdown']['medium']} contacts\n"
        response += f"• Low priority: {stats['importance_breakdown']['low']} contacts\n\n"
        
        if stats['interaction_types']:
            response += f"**📞 Interaction Types:**\n"
            for interaction_type, count in stats['interaction_types'].items():
                response += f"• {interaction_type.title()}: {count}\n"
            response += "\n"
        
        response += f"**📅 Recent Activity:**\n"
        response += f"• Interactions this week: {stats['recent_interactions']}\n\n"
        
        # Calculate relationship health
        overdue = await self.contact_manager.get_overdue_contacts()
        upcoming_birthdays = await self.contact_manager.get_upcoming_birthdays(7)
        
        response += f"**🎯 Relationship Health:**\n"
        response += f"• Contacts needing follow-up: {len(overdue)}\n"
        response += f"• Birthdays this week: {len(upcoming_birthdays)}\n"
        
        if len(overdue) == 0:
            response += f"• Status: Excellent relationship maintenance! ✅\n"
        elif len(overdue) <= 5:
            response += f"• Status: Good - just a few follow-ups needed 🟡\n"
        else:
            response += f"• Status: Needs attention - many overdue contacts 🔴\n"
        
        response += "\n💡 **Insights:**\n"
        response += "• Regular communication strengthens relationships\n"
        response += "• Use tags and groups for better organization\n"
        response += "• Track interactions to identify patterns"
        
        return response
    
    async def _handle_contact_help(self) -> str:
        """Provide contact management help"""
        response = f"📱 **Contact Management Help**\n\n"
        
        response += f"**👤 Managing Contacts:**\n"
        response += f"• 'Add contact: John Smith, email: john@email.com'\n"
        response += f"• 'Find contact: John' - Search by name, email, etc.\n"
        response += f"• 'Show all contacts' - List all contacts\n"
        response += f"• 'Delete contact: John Smith'\n\n"
        
        response += f"**📞 Communication Tracking:**\n"
        response += f"• 'Log call with John Smith'\n"
        response += f"• 'Contact history: John'\n"
        response += f"• 'Need to contact' - Show overdue follow-ups\n\n"
        
        response += f"**🏷️ Organization:**\n"
        response += f"• 'Show groups' - View contact groups\n"
        response += f"• 'Show tags' - View contact tags\n"
        response += f"• 'Contacts by group: Work'\n\n"
        
        response += f"**🎂 Special Occasions:**\n"
        response += f"• 'Upcoming birthdays' - Next 30 days\n"
        response += f"• 'Birthdays this week'\n\n"
        
        response += f"**📊 Analytics:**\n"
        response += f"• 'Contact stats' - Overview and insights\n"
        response += f"• 'Overdue contacts' - Need follow-up\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Add complete contact info for better organization\n"
        response += f"• Use tags for quick filtering (VIP, Local, Client)\n"
        response += f"• Set contact frequency for relationship maintenance\n"
        response += f"• Log interactions to track communication patterns"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_contact_skill():
        skill = ContactSkill()
        
        test_queries = [
            "add contact: John Smith, email: john@example.com",
            "find contact: john",
            "show all contacts",
            "upcoming birthdays",
            "contact stats"
        ]
        
        print("🧪 Testing Contact Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_contact_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_contact_skill())
