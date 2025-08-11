import logging
import random
from utils.adaptive_learning import adaptive_learning

class DecisionEngine:
    def __init__(self, nlp, skill_manager, memory, learning_engine, config):
        self.nlp = nlp
        self.skill_manager = skill_manager
        self.memory = memory
        self.learning_engine = learning_engine
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.adaptive_learning = adaptive_learning

    async def initialize(self):
        self.logger.info("DecisionEngine with adaptive learning initialized.")

    async def process(self, nlp_result, conversation_context):
        """Enhanced decision processing with adaptive learning"""
        intent = nlp_result.get("intent")
        user_text = nlp_result.get('text', '')
        
        # Debug logging for conversation_context
        self.logger.debug(f"🔍 Decision engine - conversation_context type: {type(conversation_context)}")
        if conversation_context is None:
            self.logger.warning("⚠️ Decision engine received None conversation_context")
            conversation_context = []
        elif not isinstance(conversation_context, list):
            self.logger.warning(f"⚠️ Decision engine received non-list conversation_context: {type(conversation_context)}")
            conversation_context = []
        else:
            self.logger.debug(f"🔍 Decision engine - conversation_context length: {len(conversation_context)}")
        
        # Check for personalized responses only for conversational intents
        # Don't intercept skill-specific intents like joke, weather, etc.
        skill_intents = ["weather", "forecast", "joke", "quote", "learning", "datetime", "identity", 
                        "personal_assistant", "task_management", "notes_management", "calendar", 
                        "contact_management", "file_management", "communication", "research", 
                        "automotive", "openai"]
        
        if intent not in skill_intents:
            self.logger.debug(f"🔍 About to call get_personalized_response for conversational intent: {intent}")
            try:
                personalized_response = self.adaptive_learning.get_personalized_response(intent, None)
                self.logger.debug(f"🔍 get_personalized_response returned: {type(personalized_response)}")
            except Exception as e:
                self.logger.error(f"❌ Error in get_personalized_response: {e}")
                personalized_response = None
                
            if personalized_response:
                self.logger.debug(f"Using personalized response for conversational intent: {intent}")
                return {"success": True, "response": personalized_response, "source": "adaptive_learning"}
        
        self.logger.debug(f"🔍 About to route intent: {intent}")
        
        # Route to appropriate skill with enhanced logic
        if intent == "weather":
            self.logger.debug(f"🔍 Routing to weather skill")
            response = await self.skill_manager.handle_skill("weather", nlp_result, conversation_context)
        elif intent == "forecast":
            self.logger.debug(f"🔍 Routing to forecast skill")
            response = await self.skill_manager.handle_skill("forecast", nlp_result, conversation_context)
        elif intent == "joke":
            self.logger.debug(f"🔍 Routing to joke skill")
            response = await self.skill_manager.handle_skill("joke", nlp_result, conversation_context)
        elif intent == "quote":
            self.logger.debug(f"🔍 Routing to quote skill")
            response = await self.skill_manager.handle_skill("quote", nlp_result, conversation_context)
        elif intent == "learning":
            self.logger.debug(f"🔍 Routing to learning skill")
            response = await self.skill_manager.handle_skill("learning", nlp_result, conversation_context)
        elif intent == "datetime":
            self.logger.debug(f"🔍 Routing to datetime skill")
            response = await self.skill_manager.handle_skill("datetime", nlp_result, conversation_context)
        elif intent == "identity":
            self.logger.debug(f"🔍 Routing to identity skill")
            from skills.identity_skill import IdentitySkill
            identity_skill = IdentitySkill()
            identity_response = await identity_skill.handle_identity(user_text, conversation_context)
            response = {"success": True, "response": identity_response, "source": "identity"}
        elif intent == "health":
            self.logger.debug(f"🔍 Routing to health skill")
            response = await self.skill_manager.handle_skill("health", nlp_result, conversation_context)
        elif intent == "personal_assistant":
            self.logger.debug(f"🔍 Routing to personal assistant skill")
            response = await self.skill_manager.handle_skill("personal_assistant", nlp_result, conversation_context)
        elif intent == "task_management":
            self.logger.debug(f"🔍 Routing to task management skill")
            response = await self.skill_manager.handle_skill("task_management", nlp_result, conversation_context)
        elif intent == "notes_management":
            self.logger.debug(f"🔍 Routing to notes management skill")
            response = await self.skill_manager.handle_skill("notes_management", nlp_result, conversation_context)
        elif intent == "calendar":
            self.logger.debug(f"🔍 Routing to calendar skill")
            response = await self.skill_manager.handle_skill("calendar", nlp_result, conversation_context)
        elif intent == "contact_management":
            self.logger.debug(f"🔍 Routing to contact management skill")
            response = await self.skill_manager.handle_skill("contact_management", nlp_result, conversation_context)
        elif intent == "file_management":
            self.logger.debug(f"🔍 Routing to file management skill")
            response = await self.skill_manager.handle_skill("file_management", nlp_result, conversation_context)
        elif intent == "communication":
            self.logger.debug(f"🔍 Routing to communication skill")
            response = await self.skill_manager.handle_skill("communication", nlp_result, conversation_context)
        elif intent == "research":
            self.logger.debug(f"🔍 Routing to research skill")
            response = await self.skill_manager.handle_skill("research", nlp_result, conversation_context)
        elif intent == "openai":
            self.logger.debug(f"🔍 Routing to Gemini for openai intent")
            # Route all unmatched queries to Gemini
            from utils.gemini import ask_gemini
            try:
                gemini_response = ask_gemini(user_text)
                response = {"success": True, "response": gemini_response, "source": "gemini"}
                self.logger.debug(f"🔍 Gemini response successful")
            except Exception as e:
                self.logger.error(f"❌ Error calling Gemini: {e}")
                response = {"success": False, "response": "Sorry, I couldn't process that request.", "source": "error"}
        else:
            self.logger.debug(f"🔍 Routing to conversational responses for intent: {intent}")
            # Handle conversational responses with adaptive learning
            response = await self._handle_conversational_responses(nlp_result)
        
        # Learn from this interaction
        if response and response.get("response"):
            self.adaptive_learning.learn_from_interaction(user_text, intent, response["response"])
        
        self.logger.debug(f"Decision made: {intent} -> {response.get('source', 'unknown')}")
        return response

    async def _handle_conversational_responses(self, nlp_result):
        """Handle conversational responses with learning integration"""
        user_text = nlp_result.get('text', '').lower()
        
        def fuzzy_match(choices, text, threshold=80):
            try:
                from rapidfuzz import fuzz
                for phrase in choices:
                    if fuzz.partial_ratio(phrase, text) >= threshold:
                        return True
            except Exception:
                for phrase in choices:
                    if phrase in text:
                        return True
            return False

        # Enhanced conversational patterns with learning
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if fuzzy_match(greetings, user_text):
            default_responses = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Need any assistance?",
                "Greetings! How may I assist you?"
            ]
            response = self.adaptive_learning.get_personalized_response("greeting", default_responses)
            return {"success": True, "response": response, "source": "conversation"}

        how_are_you = ["how are you", "how r u", "how are u", "how's it going", "how do you do"]
        if fuzzy_match(how_are_you, user_text):
            responses = [
                "I'm just a bunch of code, but I'm here to help! How are you?",
                "I'm doing great, thanks for asking! How can I help you today?",
                "I'm always ready to assist you!"
            ]
            response = self.adaptive_learning.get_personalized_response("how_are_you", responses)
            return {"success": True, "response": response, "source": "conversation"}

        who_am_i = ["who am i", "who m i", "who is this", "who are you talking to"]
        if fuzzy_match(who_am_i, user_text):
            responses = [
                "You are my favorite user!",
                "You're the boss here!",
                "You're the amazing human chatting with me!"
            ]
            response = self.adaptive_learning.get_personalized_response("who_am_i", responses)
            return {"success": True, "response": response, "source": "conversation"}

        who_are_you = ["who are you", "who r u", "what are you", "what r u", "tell me about yourself", "introduce yourself", "your name", "what is your name", "whats your name"]
        if fuzzy_match(who_are_you, user_text):
            responses = [
                "I'm BUDDY, your AI assistant! I can help with weather, jokes, quotes, and general conversation.",
                "Hi! I'm BUDDY, an AI assistant designed to help and chat with you.",
                "I'm BUDDY - your friendly AI companion here to assist with various tasks and have conversations!"
            ]
            response = self.adaptive_learning.get_personalized_response("identity", responses)
            return {"success": True, "response": response, "source": "conversation"}

        location_questions = ["where are you", "where r u", "what is your location", "your location"]
        if fuzzy_match(location_questions, user_text):
            responses = [
                "I exist in the digital realm, running on your computer to help you!",
                "I'm right here in your computer, ready to assist!",
                "I live in the cloud and on your device, always here when you need me!"
            ]
            response = self.adaptive_learning.get_personalized_response("location", responses)
            return {"success": True, "response": response, "source": "conversation"}

        thanks = ["thank you", "thanks", "thx", "ty"]
        if fuzzy_match(thanks, user_text):
            responses = [
                "You're welcome! If you need anything else, just ask.",
                "No problem! Happy to help.",
                "Anytime!"
            ]
            response = self.adaptive_learning.get_personalized_response("thanks", responses)
            return {"success": True, "response": response, "source": "conversation"}

        farewells = ["bye", "goodbye", "see you", "see ya", "later"]
        if fuzzy_match(farewells, user_text):
            responses = [
                "Goodbye! Have a great day!",
                "See you soon!",
                "Take care!"
            ]
            response = self.adaptive_learning.get_personalized_response("farewell", responses)
            return {"success": True, "response": response, "source": "conversation"}

        help_phrases = ["help", "what can you do", "how can you help", "assist me"]
        if fuzzy_match(help_phrases, user_text):
            response = "You can ask me for a joke, the weather, a quote, or just chat!"
            return {"success": True, "response": response, "source": "conversation"}

        # General request patterns - only for BUDDY's specific capabilities
        general_requests = ["help me with", "assist me with", "what can you do", "how can you help", "what are your capabilities", "what do you offer", "your features", "your skills"]
        if fuzzy_match(general_requests, user_text):
            general_responses = [
                "I'd be happy to help! I can assist you with weather forecasts, tell jokes, share inspirational quotes, or just have a friendly conversation. What would you like to know more about?",
                "Sure! I can help with various things like checking the weather, sharing some humor with jokes, providing motivational quotes, or chatting about different topics. What interests you?",
                "I'm here to assist! I can provide weather updates, make you laugh with jokes, inspire you with quotes, or simply chat. What would you like help with today?",
                "Absolutely! I can help you with weather information, entertaining jokes, uplifting quotes, or general conversation. Just let me know what you're looking for!"
            ]
            response = self.adaptive_learning.get_personalized_response("general_help", general_responses)
            return {"success": True, "response": response, "source": "conversation"}
        
        # Fallback to Gemini for unhandled queries
        try:
            from utils.gemini import ask_gemini
            gemini_response = ask_gemini(nlp_result.get('text', ''))
            if gemini_response.startswith("[Gemini API error"):
                fallback_responses = [
                    "I'm here to help! Ask me about weather, jokes, quotes, or try asking something else.",
                    "That's an interesting question! I can help with weather forecasts, jokes, quotes, and general chat.",
                    "I'm always learning. You can ask me for weather updates, jokes, inspirational quotes, or just chat!",
                    "Let's chat! I can provide weather info, tell jokes, share quotes, or answer questions."
                ]
                response = self.adaptive_learning.get_personalized_response("fallback", fallback_responses)
                return {"success": True, "response": response, "source": "fallback"}
            return {"success": True, "response": gemini_response, "source": "gemini"}
        except Exception as e:
            self.logger.error(f"Gemini API error in decision engine: {e}")
            fallback_responses = [
                "I'm here to help! Ask me about weather, jokes, quotes, or try asking something else.",
                "That's an interesting question! I can help with weather forecasts, jokes, quotes, and general chat.",
                "I'm always learning. You can ask me for weather updates, jokes, inspirational quotes, or just chat!",
                "Let's chat! I can provide weather info, tell jokes, share quotes, or answer questions."
            ]
            response = self.adaptive_learning.get_personalized_response("error_fallback", fallback_responses)
            return {"success": True, "response": response, "source": "error_fallback"}

    async def get_stats(self):
        """Get decision engine statistics with learning data"""
        base_stats = {
            "decision_engine": "active",
            "adaptive_learning": "enabled"
        }
        
        # Add learning statistics
        learning_stats = self.adaptive_learning.get_stats()
        base_stats.update(learning_stats)
        
        return base_stats
