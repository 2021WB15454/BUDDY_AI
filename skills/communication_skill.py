"""
Email & Communication Assistant Module for BUDDY AI Assistant
Handles email management, templates, communication tracking, and message composition
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
class EmailTemplate:
    """Email template structure"""
    id: str
    name: str
    subject: str
    body: str
    category: str  # professional, personal, sales, support, etc.
    variables: List[str]  # List of placeholder variables like {name}, {company}
    usage_count: int
    created_at: str
    last_used: str
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class CommunicationLog:
    """Communication log entry"""
    id: str
    communication_type: str  # email, call, meeting, text, letter
    contact_name: str
    contact_email: str
    subject: str
    content: str
    direction: str  # sent, received, planned
    status: str  # draft, sent, received, failed
    priority: str  # high, medium, low
    date: str
    follow_up_needed: bool
    follow_up_date: str
    tags: List[str]
    notes: str
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().isoformat()


@dataclass
class EmailDraft:
    """Email draft structure"""
    id: str
    to_email: str
    cc_emails: List[str]
    bcc_emails: List[str]
    subject: str
    body: str
    template_id: str
    priority: str
    send_at: str  # Scheduled send time
    attachments: List[str]
    created_at: str
    status: str  # draft, scheduled, sent
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class CommunicationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates_file = "learning_data/email_templates.json"
        self.communications_file = "learning_data/communications.json"
        self.drafts_file = "learning_data/email_drafts.json"
        self.templates = self._load_templates()
        self.communications = self._load_communications()
        self.drafts = self._load_drafts()
        self.logger.info("CommunicationManager initialized.")
    
    def _load_templates(self) -> List[EmailTemplate]:
        """Load email templates from file"""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                templates_data = json.load(f)
                return [EmailTemplate(**template) for template in templates_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return self._create_default_templates()
    
    def _load_communications(self) -> List[CommunicationLog]:
        """Load communication logs from file"""
        try:
            with open(self.communications_file, 'r', encoding='utf-8') as f:
                comms_data = json.load(f)
                return [CommunicationLog(**comm) for comm in comms_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _load_drafts(self) -> List[EmailDraft]:
        """Load email drafts from file"""
        try:
            with open(self.drafts_file, 'r', encoding='utf-8') as f:
                drafts_data = json.load(f)
                return [EmailDraft(**draft) for draft in drafts_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_templates(self):
        """Save email templates to file"""
        try:
            os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                templates_data = [asdict(template) for template in self.templates]
                json.dump(templates_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving templates: {e}")
    
    def _save_communications(self):
        """Save communication logs to file"""
        try:
            os.makedirs(os.path.dirname(self.communications_file), exist_ok=True)
            with open(self.communications_file, 'w', encoding='utf-8') as f:
                comms_data = [asdict(comm) for comm in self.communications]
                json.dump(comms_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving communications: {e}")
    
    def _save_drafts(self):
        """Save email drafts to file"""
        try:
            os.makedirs(os.path.dirname(self.drafts_file), exist_ok=True)
            with open(self.drafts_file, 'w', encoding='utf-8') as f:
                drafts_data = [asdict(draft) for draft in self.drafts]
                json.dump(drafts_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving drafts: {e}")
    
    def _create_default_templates(self) -> List[EmailTemplate]:
        """Create default email templates"""
        defaults = [
            {
                "name": "Meeting Request",
                "subject": "Meeting Request: {subject}",
                "body": "Hi {name},\n\nI hope this email finds you well. I would like to schedule a meeting to discuss {topic}.\n\nWould you be available for a {duration} meeting sometime {timeframe}? I'm flexible with timing and can accommodate your schedule.\n\nPlease let me know what works best for you.\n\nBest regards,\n{sender_name}",
                "category": "professional",
                "variables": ["name", "subject", "topic", "duration", "timeframe", "sender_name"]
            },
            {
                "name": "Follow-up Email",
                "subject": "Following up on {topic}",
                "body": "Hi {name},\n\nI wanted to follow up on our previous conversation about {topic}.\n\n{follow_up_content}\n\nPlease let me know if you have any questions or if there's anything I can help clarify.\n\nLooking forward to hearing from you.\n\nBest regards,\n{sender_name}",
                "category": "professional",
                "variables": ["name", "topic", "follow_up_content", "sender_name"]
            },
            {
                "name": "Thank You Note",
                "subject": "Thank you for {reason}",
                "body": "Dear {name},\n\nI wanted to take a moment to thank you for {reason}. {specific_thanks}\n\nYour {quality} is truly appreciated, and I'm grateful for {what_grateful_for}.\n\nThanks again!\n\nWarm regards,\n{sender_name}",
                "category": "personal",
                "variables": ["name", "reason", "specific_thanks", "quality", "what_grateful_for", "sender_name"]
            },
            {
                "name": "Project Update",
                "subject": "Project Update: {project_name}",
                "body": "Hi {name},\n\nI wanted to provide you with an update on the {project_name} project.\n\n**Current Status:** {status}\n**Completed:** {completed_items}\n**In Progress:** {in_progress_items}\n**Next Steps:** {next_steps}\n**Timeline:** {timeline}\n\nPlease let me know if you have any questions or concerns.\n\nBest regards,\n{sender_name}",
                "category": "professional",
                "variables": ["name", "project_name", "status", "completed_items", "in_progress_items", "next_steps", "timeline", "sender_name"]
            },
            {
                "name": "Apology Email",
                "subject": "Apology for {issue}",
                "body": "Dear {name},\n\nI am writing to sincerely apologize for {issue}. I understand that {impact} and take full responsibility for this situation.\n\n{explanation}\n\nTo make this right, I will {corrective_action}. I am committed to ensuring this doesn't happen again by {prevention_measures}.\n\nThank you for your patience and understanding.\n\nSincerely,\n{sender_name}",
                "category": "professional",
                "variables": ["name", "issue", "impact", "explanation", "corrective_action", "prevention_measures", "sender_name"]
            }
        ]
        
        templates = []
        for template_data in defaults:
            template = EmailTemplate(
                id=str(uuid.uuid4())[:8],
                name=template_data["name"],
                subject=template_data["subject"],
                body=template_data["body"],
                category=template_data["category"],
                variables=template_data["variables"],
                usage_count=0,
                created_at=datetime.now().isoformat(),
                last_used=""
            )
            templates.append(template)
        
        self.templates = templates
        self._save_templates()
        return templates
    
    def _extract_variables(self, text: str) -> List[str]:
        """Extract variables from template text (e.g., {name}, {company})"""
        return re.findall(r'\{([^}]+)\}', text)
    
    async def create_template(self, name: str, subject: str, body: str, 
                            category: str = "general") -> str:
        """Create a new email template"""
        
        # Check for duplicate names
        for template in self.templates:
            if template.name.lower() == name.lower():
                raise ValueError(f"Template name already exists: {name}")
        
        # Extract variables from subject and body
        variables = list(set(self._extract_variables(subject) + self._extract_variables(body)))
        
        template = EmailTemplate(
            id=str(uuid.uuid4())[:8],
            name=name,
            subject=subject,
            body=body,
            category=category.lower(),
            variables=variables,
            usage_count=0,
            created_at=datetime.now().isoformat(),
            last_used=""
        )
        
        self.templates.append(template)
        self._save_templates()
        
        self.logger.info(f"Email template created: {name}")
        return template.id
    
    async def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        """Get template by ID or name"""
        for template in self.templates:
            if template.id == template_id or template.name.lower() == template_id.lower():
                return template
        return None
    
    async def use_template(self, template_id: str, variables: Dict[str, str]) -> Dict[str, str]:
        """Use a template with provided variables"""
        template = await self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Replace variables in subject and body
        subject = template.subject
        body = template.body
        
        for var, value in variables.items():
            placeholder = f"{{{var}}}"
            subject = subject.replace(placeholder, value)
            body = body.replace(placeholder, value)
        
        # Update usage stats
        template.usage_count += 1
        template.last_used = datetime.now().isoformat()
        self._save_templates()
        
        return {"subject": subject, "body": body}
    
    async def create_draft(self, to_email: str, subject: str, body: str,
                          cc_emails: List[str] = None, bcc_emails: List[str] = None,
                          priority: str = "medium", send_at: str = "",
                          template_id: str = "") -> str:
        """Create an email draft"""
        
        draft = EmailDraft(
            id=str(uuid.uuid4())[:8],
            to_email=to_email,
            cc_emails=cc_emails or [],
            bcc_emails=bcc_emails or [],
            subject=subject,
            body=body,
            template_id=template_id,
            priority=priority.lower(),
            send_at=send_at,
            attachments=[],
            created_at=datetime.now().isoformat(),
            status="draft"
        )
        
        self.drafts.append(draft)
        self._save_drafts()
        
        self.logger.info(f"Email draft created: {subject}")
        return draft.id
    
    async def log_communication(self, communication_type: str, contact_name: str,
                              contact_email: str, subject: str, content: str,
                              direction: str, status: str = "completed",
                              priority: str = "medium", tags: List[str] = None,
                              notes: str = "") -> str:
        """Log a communication"""
        
        comm = CommunicationLog(
            id=str(uuid.uuid4())[:8],
            communication_type=communication_type.lower(),
            contact_name=contact_name,
            contact_email=contact_email,
            subject=subject,
            content=content,
            direction=direction.lower(),
            status=status.lower(),
            priority=priority.lower(),
            date=datetime.now().isoformat(),
            follow_up_needed=False,
            follow_up_date="",
            tags=tags or [],
            notes=notes
        )
        
        self.communications.append(comm)
        self._save_communications()
        
        self.logger.info(f"Communication logged: {communication_type} with {contact_name}")
        return comm.id
    
    async def get_templates_by_category(self, category: str) -> List[EmailTemplate]:
        """Get all templates in a specific category"""
        return [t for t in self.templates if t.category.lower() == category.lower()]
    
    async def search_templates(self, query: str) -> List[EmailTemplate]:
        """Search templates by name, subject, or body content"""
        query = query.lower()
        results = []
        
        for template in self.templates:
            if (query in template.name.lower() or
                query in template.subject.lower() or
                query in template.body.lower() or
                query in template.category.lower()):
                results.append(template)
        
        # Sort by usage count and relevance
        results.sort(key=lambda t: (
            t.usage_count,
            0 if query in t.name.lower() else 1
        ), reverse=True)
        
        return results
    
    async def get_communication_history(self, contact_email: str = "", 
                                      days: int = 30) -> List[CommunicationLog]:
        """Get communication history for a contact or recent communications"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        communications = []
        for comm in self.communications:
            try:
                comm_date = datetime.fromisoformat(comm.date)
                if comm_date >= cutoff_date:
                    if not contact_email or comm.contact_email.lower() == contact_email.lower():
                        communications.append(comm)
            except:
                continue
        
        communications.sort(key=lambda c: c.date, reverse=True)
        return communications
    
    async def get_follow_ups_needed(self) -> List[CommunicationLog]:
        """Get communications that need follow-up"""
        now = datetime.now()
        follow_ups = []
        
        for comm in self.communications:
            if comm.follow_up_needed:
                if comm.follow_up_date:
                    try:
                        follow_up_date = datetime.fromisoformat(comm.follow_up_date)
                        if follow_up_date <= now:
                            follow_ups.append(comm)
                    except:
                        follow_ups.append(comm)
                else:
                    follow_ups.append(comm)
        
        follow_ups.sort(key=lambda c: c.follow_up_date or c.date)
        return follow_ups
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics"""
        total_comms = len(self.communications)
        total_templates = len(self.templates)
        total_drafts = len(self.drafts)
        
        # Communication types
        comm_types = {}
        for comm in self.communications:
            comm_types[comm.communication_type] = comm_types.get(comm.communication_type, 0) + 1
        
        # Template usage
        template_usage = sum(t.usage_count for t in self.templates)
        most_used_template = max(self.templates, key=lambda t: t.usage_count) if self.templates else None
        
        # Recent activity
        now = datetime.now()
        recent_comms = len([c for c in self.communications 
                           if (now - datetime.fromisoformat(c.date)).days <= 7])
        
        # Follow-ups needed
        follow_ups = len([c for c in self.communications if c.follow_up_needed])
        
        return {
            "total_communications": total_comms,
            "total_templates": total_templates,
            "total_drafts": total_drafts,
            "communication_types": comm_types,
            "template_usage": template_usage,
            "most_used_template": most_used_template.name if most_used_template else None,
            "recent_communications": recent_comms,
            "follow_ups_needed": follow_ups
        }


class CommunicationSkill:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.comm_manager = CommunicationManager()
        self.logger.info("CommunicationSkill initialized.")
    
    async def handle_communication_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle communication and email management queries"""
        try:
            query_lower = user_input.lower().strip()
            
            # Email templates
            if any(keyword in query_lower for keyword in ["email template", "create template", "use template"]):
                return await self._handle_email_templates(user_input, context)
            
            # Compose email/draft
            elif any(keyword in query_lower for keyword in ["compose email", "write email", "draft email"]):
                return await self._handle_compose_email(user_input, context)
            
            # Communication log
            elif any(keyword in query_lower for keyword in ["log communication", "log email", "log call"]):
                return await self._handle_log_communication(user_input, context)
            
            # Communication history
            elif any(keyword in query_lower for keyword in ["communication history", "email history", "conversation history"]):
                return await self._handle_communication_history(user_input, context)
            
            # Follow-ups
            elif any(keyword in query_lower for keyword in ["follow up", "follow-up", "pending follow"]):
                return await self._handle_follow_ups()
            
            # Email suggestions
            elif any(keyword in query_lower for keyword in ["email suggestion", "help write", "email help"]):
                return await self._handle_email_suggestions(user_input, context)
            
            # Communication stats
            elif any(keyword in query_lower for keyword in ["communication stats", "email stats"]):
                return await self._handle_communication_stats()
            
            # Default help
            else:
                return await self._handle_communication_help()
                
        except Exception as e:
            self.logger.error(f"Error handling communication query: {e}")
            return "I'm having trouble with communication management right now. Please try again!"
    
    async def _handle_email_templates(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle email template operations"""
        query_lower = user_input.lower()
        
        if "create template" in query_lower:
            return ("📝 **Create Email Template**\n\n"
                   "Feature in development! This will allow you to:\n\n"
                   "• Create custom email templates\n"
                   "• Use variables like {name}, {company}\n"
                   "• Organize templates by category\n"
                   "• Track template usage\n\n"
                   "Example usage:\n"
                   "'Create template: Meeting Request'")
        
        elif "use template" in query_lower or "email template" in query_lower:
            # Show available templates
            templates = self.comm_manager.templates
            
            if not templates:
                return ("📧 **No Email Templates Found**\n\n"
                       "You don't have any email templates yet.\n"
                       "Default templates will be created automatically when you start using the system!")
            
            response = f"📧 **Available Email Templates** ({len(templates)} templates)\n\n"
            
            # Group by category
            categories = {}
            for template in templates:
                if template.category not in categories:
                    categories[template.category] = []
                categories[template.category].append(template)
            
            for category, cat_templates in categories.items():
                response += f"**📁 {category.title()}:**\n"
                for template in cat_templates:
                    response += f"• **{template.name}**\n"
                    response += f"  Subject: {template.subject[:50]}...\n"
                    response += f"  Used: {template.usage_count} times\n"
                    if template.variables:
                        response += f"  Variables: {', '.join(template.variables)}\n"
                    response += f"  ID: {template.id}\n\n"
            
            response += "💡 Use 'Use template: [name]' to compose an email from a template."
            
            return response
        
        else:
            return await self._handle_communication_help()
    
    async def _handle_compose_email(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle email composition"""
        return ("✉️ **Email Composition**\n\n"
               "Feature coming soon! This will help you:\n\n"
               "• Compose professional emails quickly\n"
               "• Use templates with smart variable replacement\n"
               "• Save drafts for later editing\n"
               "• Schedule emails for optimal sending times\n"
               "• Suggest improvements to email content\n\n"
               "Example usage:\n"
               "'Compose email to john@company.com using meeting request template'\n"
               "'Draft email: subject: Project Update, body: ...'")
    
    async def _handle_log_communication(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle logging communications"""
        return ("📞 **Communication Logging**\n\n"
               "Feature in development! This will track:\n\n"
               "• All email communications\n"
               "• Phone calls and their outcomes\n"
               "• Meeting discussions and decisions\n"
               "• Follow-up requirements and reminders\n\n"
               "Example usage:\n"
               "'Log call with John Smith about project budget'\n"
               "'Log email sent to team about meeting changes'")
    
    async def _handle_communication_history(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle communication history requests"""
        history = await self.comm_manager.get_communication_history(days=30)
        
        if not history:
            return ("📋 **Communication History**\n\n"
                   "No recent communications found in the last 30 days.\n"
                   "Start logging your communications to track interaction patterns!")
        
        response = f"📋 **Recent Communication History** ({len(history)} communications)\n\n"
        
        # Group by contact
        contacts = {}
        for comm in history:
            if comm.contact_name not in contacts:
                contacts[comm.contact_name] = []
            contacts[comm.contact_name].append(comm)
        
        for contact, comms in list(contacts.items())[:5]:  # Show top 5 contacts
            response += f"👤 **{contact}**\n"
            
            for comm in comms[:3]:  # Show recent 3 communications per contact
                try:
                    comm_date = datetime.fromisoformat(comm.date)
                    days_ago = (datetime.now() - comm_date).days
                    
                    type_emoji = {
                        "email": "📧", "call": "📞", "meeting": "🤝", 
                        "text": "💬", "letter": "📮"
                    }.get(comm.communication_type, "💬")
                    
                    direction_emoji = {"sent": "➡️", "received": "⬅️", "planned": "📅"}.get(comm.direction, "")
                    
                    response += f"   {type_emoji} {direction_emoji} {comm.subject[:40]}...\n"
                    response += f"     📅 {days_ago} days ago | {comm.status.title()}\n"
                    
                    if comm.follow_up_needed:
                        response += f"     ⚠️ Follow-up needed\n"
                except:
                    continue
            
            response += "\n"
        
        if len(contacts) > 5:
            response += f"... and {len(contacts) - 5} more contacts\n\n"
        
        response += "💡 Use 'Log communication' to track new interactions and maintain relationship history."
        
        return response
    
    async def _handle_follow_ups(self) -> str:
        """Handle follow-up requests"""
        follow_ups = await self.comm_manager.get_follow_ups_needed()
        
        if not follow_ups:
            return ("✅ **All Caught Up!**\n\n"
                   "No pending follow-ups at the moment.\n"
                   "Great job staying on top of your communications!")
        
        response = f"⏰ **Pending Follow-ups** ({len(follow_ups)} items)\n\n"
        
        for follow_up in follow_ups[:10]:  # Show top 10
            try:
                comm_date = datetime.fromisoformat(follow_up.date)
                days_ago = (datetime.now() - comm_date).days
                
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(follow_up.priority, "⚪")
                
                response += f"{priority_emoji} **{follow_up.contact_name}**\n"
                response += f"   📧 {follow_up.contact_email}\n"
                response += f"   💬 {follow_up.subject}\n"
                response += f"   📅 Original: {days_ago} days ago\n"
                
                if follow_up.follow_up_date:
                    try:
                        follow_date = datetime.fromisoformat(follow_up.follow_up_date)
                        if follow_date < datetime.now():
                            response += f"   ⚠️ Overdue since {follow_date.strftime('%m/%d')}\n"
                        else:
                            response += f"   📅 Due: {follow_date.strftime('%m/%d')}\n"
                    except:
                        response += f"   📅 Follow-up needed\n"
                
                if follow_up.notes:
                    response += f"   📝 {follow_up.notes[:50]}...\n"
                
                response += "\n"
                
            except Exception:
                continue
        
        if len(follow_ups) > 10:
            response += f"... and {len(follow_ups) - 10} more follow-ups\n\n"
        
        response += "💡 **Suggestions:**\n"
        response += "• Prioritize high-priority follow-ups (🔴)\n"
        response += "• Set specific follow-up dates for better tracking\n"
        response += "• Use email templates for quick responses"
        
        return response
    
    async def _handle_email_suggestions(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle email writing suggestions"""
        
        # Extract the type of email or situation
        query_lower = user_input.lower()
        
        suggestions = {
            "meeting": {
                "subject": "Use clear, specific subjects like 'Meeting Request: Project Planning - Week of [Date]'",
                "opening": "Start with a friendly greeting and brief context",
                "body": "Include purpose, proposed times, duration, and agenda items",
                "closing": "End with flexibility and appreciation"
            },
            "follow": {
                "subject": "Reference previous interaction: 'Following up on [specific topic]'",
                "opening": "Acknowledge previous conversation or meeting",
                "body": "Summarize key points and add new information or questions",
                "closing": "Include clear next steps or call to action"
            },
            "apology": {
                "subject": "Be direct: 'Apology for [specific issue]'",
                "opening": "Take immediate responsibility without excuses",
                "body": "Explain briefly, show understanding of impact, outline corrective actions",
                "closing": "Reaffirm commitment to improvement"
            },
            "thank": {
                "subject": "Be specific: 'Thank you for [specific action/help]'",
                "opening": "Express genuine gratitude immediately",
                "body": "Mention specific actions and their positive impact",
                "closing": "Offer reciprocal help or future collaboration"
            }
        }
        
        # Determine email type
        email_type = "general"
        for key in suggestions.keys():
            if key in query_lower:
                email_type = key
                break
        
        response = "✍️ **Email Writing Suggestions**\n\n"
        
        if email_type in suggestions:
            suggestion = suggestions[email_type]
            response += f"**📧 {email_type.title()} Email Guidelines:**\n\n"
            response += f"**📝 Subject Line:**\n{suggestion['subject']}\n\n"
            response += f"**👋 Opening:**\n{suggestion['opening']}\n\n"
            response += f"**📄 Body:**\n{suggestion['body']}\n\n"
            response += f"**🎯 Closing:**\n{suggestion['closing']}\n\n"
        else:
            response += "**📧 General Email Best Practices:**\n\n"
            response += "**📝 Subject Line:**\n• Be clear, specific, and actionable\n• Include relevant dates, names, or projects\n• Avoid vague terms like 'Question' or 'FYI'\n\n"
            response += "**👋 Opening:**\n• Use appropriate greeting for relationship level\n• Add context if it's been a while since last contact\n• Get to the point quickly but politely\n\n"
            response += "**📄 Body:**\n• Use short paragraphs and bullet points\n• Lead with the most important information\n• Be specific about requests and deadlines\n• Include all necessary details upfront\n\n"
            response += "**🎯 Closing:**\n• Summarize key action items\n• Specify response timeline if needed\n• Use professional but warm sign-off\n\n"
        
        response += "**💡 Pro Tips:**\n"
        response += "• Read your email aloud before sending\n"
        response += "• Check that the tone matches your relationship\n"
        response += "• Use 'Reply All' sparingly\n"
        response += "• Double-check recipient addresses\n"
        response += "• Consider calling for complex or sensitive topics"
        
        return response
    
    async def _handle_communication_stats(self) -> str:
        """Handle communication statistics request"""
        stats = self.comm_manager.get_communication_stats()
        
        response = f"📊 **Communication Statistics**\n\n"
        
        response += f"**📈 Overview:**\n"
        response += f"• Total communications: {stats['total_communications']}\n"
        response += f"• Email templates: {stats['total_templates']}\n"
        response += f"• Draft emails: {stats['total_drafts']}\n"
        response += f"• Template usage: {stats['template_usage']} times\n"
        response += f"• Recent activity (7 days): {stats['recent_communications']}\n\n"
        
        if stats['communication_types']:
            response += f"**📞 By Communication Type:**\n"
            for comm_type, count in sorted(stats['communication_types'].items(), key=lambda x: x[1], reverse=True):
                response += f"• {comm_type.title()}: {count}\n"
            response += "\n"
        
        if stats['most_used_template']:
            response += f"**⭐ Most Used Template:**\n"
            response += f"• {stats['most_used_template']}\n\n"
        
        response += f"**⚠️ Action Items:**\n"
        response += f"• Follow-ups needed: {stats['follow_ups_needed']}\n\n"
        
        # Communication insights
        response += f"**💡 Communication Insights:**\n"
        if stats['total_communications'] == 0:
            response += f"• Start logging communications to track patterns\n"
        elif stats['recent_communications'] == 0:
            response += f"• No recent activity - consider reaching out to important contacts\n"
        else:
            response += f"• Good communication activity level\n"
        
        response += f"• Use templates to save time on common emails\n"
        response += f"• Regular follow-ups improve relationship management\n"
        response += f"• Track communications to identify trends and opportunities"
        
        return response
    
    async def _handle_communication_help(self) -> str:
        """Provide communication management help"""
        response = f"📧 **Communication & Email Management Help**\n\n"
        
        response += f"**📝 Email Templates:**\n"
        response += f"• 'Email templates' - View available templates\n"
        response += f"• 'Create template: [name]' - Make new template\n"
        response += f"• 'Use template: [name]' - Compose with template\n\n"
        
        response += f"**✉️ Email Composition:**\n"
        response += f"• 'Compose email to [recipient]' - Create new email\n"
        response += f"• 'Draft email: [subject]' - Save draft for later\n"
        response += f"• 'Email suggestions for [type]' - Writing tips\n\n"
        
        response += f"**📋 Communication Tracking:**\n"
        response += f"• 'Log communication with [contact]' - Record interaction\n"
        response += f"• 'Communication history' - Recent interactions\n"
        response += f"• 'Follow-ups needed' - Pending actions\n\n"
        
        response += f"**📊 Analytics:**\n"
        response += f"• 'Communication stats' - Overview and insights\n"
        response += f"• 'Email history with [contact]' - Contact-specific history\n\n"
        
        response += f"**💡 Pro Tips:**\n"
        response += f"• Use templates for consistent, professional messaging\n"
        response += f"• Log important communications for relationship tracking\n"
        response += f"• Set follow-up reminders for better relationship management\n"
        response += f"• Review communication patterns to improve efficiency\n"
        response += f"• Use clear, specific subject lines for better organization"
        
        return response


# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_communication_skill():
        skill = CommunicationSkill()
        
        test_queries = [
            "email templates",
            "email suggestions for meeting",
            "communication history",
            "follow-ups needed",
            "communication stats"
        ]
        
        print("🧪 Testing Communication Management Skill")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            response = await skill.handle_communication_query(query, {})
            print(f"Response: {response[:200]}...")
            print("-" * 40)
    
    asyncio.run(test_communication_skill())
