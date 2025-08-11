import logging

class SkillManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.skills = []

    async def initialize(self):
        self.logger.info("SkillManager initialized.")
        from skills.weather_skill import WeatherSkill
        from skills.forecast_skill import ForecastSkill
        from skills.joke_skill import JokeSkill
        from skills.quote_skill import QuoteSkill
        from skills.learning_skill import LearningSkill
        from skills.identity_skill import IdentitySkill
        from skills.health_skill import handle_skill as health_handle_skill
        from skills.personal_assistant_skill import PersonalAssistantSkill
        from skills.datetime_skill import DateTimeSkill
        from skills.task_management_skill import TaskSkill
        from skills.notes_management_skill import NotesSkill
        from skills.calendar_skill import CalendarSkill
        from skills.contact_skill import ContactSkill
        from skills.file_management_skill import FileManagementSkill
        from skills.communication_skill import CommunicationSkill
        from skills.research_skill import ResearchSkill
        from skills.automotive_skill import AutomotiveSkill
        
        # Initialize skills with proper interfaces
        self.skills = {
            "weather": WeatherSkill(self.config),
            "forecast": ForecastSkill(self.config),
            "joke": JokeSkill(self.config),
            "quote": QuoteSkill(self.config),
            "learning": LearningSkill(self.config),
            "identity": IdentitySkill(),
            "personal_assistant": PersonalAssistantSkill(),
            "datetime": DateTimeSkill(),
            "task_management": TaskSkill(),
            "notes_management": NotesSkill(),
            "calendar": CalendarSkill(),
            "contact_management": ContactSkill(),
            "file_management": FileManagementSkill(),
            "communication": CommunicationSkill(),
            "research": ResearchSkill(),
            "automotive": AutomotiveSkill(self.config),
        }
        
        # Add health skill with different interface
        self.health_handle = health_handle_skill

    async def get_available_skills(self):
        return list(self.skills.keys()) + ["health"]

    async def handle_skill(self, skill_name, nlp_result, context):
        if skill_name == "health":
            return await self.health_handle(skill_name, nlp_result, context)
        elif skill_name == "personal_assistant":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_personal_assistant_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "datetime":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_datetime_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "task_management":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_task_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "notes_management":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_notes_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "calendar":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_calendar_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "contact_management":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_contact_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "file_management":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_file_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "communication":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_communication_query(user_input, context)
                return {"success": True, "response": response}
        elif skill_name == "research":
            skill = self.skills.get(skill_name)
            if skill:
                user_input = nlp_result.get('text', '')
                response = await skill.handle_research_query(user_input, context)
                return {"success": True, "response": response}
        
        skill = self.skills.get(skill_name)
        if skill:
            return await skill.handle(nlp_result, context)
        return {"success": False, "response": f"Skill '{skill_name}' not found."}
