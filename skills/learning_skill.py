"""
Learning Commands Skill for BUDDY AI Assistant
Handles commands related to learning and self-improvement
"""
import logging
from utils.adaptive_learning import adaptive_learning

class LearningSkill:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def handle(self, nlp_result, context):
        user_input = nlp_result.get('text', '') if isinstance(nlp_result, dict) else str(nlp_result)
        user_input_lower = user_input.lower()
        
        # Handle different learning commands
        if any(phrase in user_input_lower for phrase in ['show your stats', 'learning stats', 'what have you learned']):
            stats = adaptive_learning.get_stats()
            response = f"""📊 My Learning Stats:
• Jokes learned from users: {stats['learned_jokes']}
• Conversation patterns: {stats['conversation_patterns']}
• Feedback entries: {stats['feedback_entries']}
• Most used feature: {stats['most_used_intent']}

I'm constantly learning from our conversations to serve you better!"""
            return {"success": True, "response": response}
        
        elif any(phrase in user_input_lower for phrase in ['forget that', 'delete that', 'remove that']):
            # Handle requests to forget information
            response = "I understand you'd like me to forget something. Could you be more specific about what you'd like me to forget? For example: 'forget my jokes' or 'reset my preferences'."
            return {"success": True, "response": response}
        
        elif any(phrase in user_input_lower for phrase in ['learn this', 'remember this', 'save this']):
            # Handle general learning requests
            if 'joke' in user_input_lower:
                if adaptive_learning.learn_user_joke(user_input):
                    response = "Great! I've learned that joke and will remember it. Thanks for teaching me!"
                else:
                    response = "I'd love to learn that joke! Try saying 'Here's a joke: [your joke]' to help me understand it better."
            else:
                response = "I'm listening! What would you like me to learn? I can learn jokes, conversation patterns, and preferences from our interactions."
            return {"success": True, "response": response}
        
        elif any(phrase in user_input_lower for phrase in ['good job', 'well done', 'that was good', 'nice response', 'perfect']):
            # Positive feedback
            adaptive_learning.provide_feedback(user_input, "positive", "User expressed satisfaction")
            response = "Thank you! I appreciate the positive feedback. It helps me learn what you like!"
            return {"success": True, "response": response}
        
        elif any(phrase in user_input_lower for phrase in ['that was bad', 'wrong answer', 'not good', 'try again', 'incorrect']):
            # Negative feedback
            adaptive_learning.provide_feedback(user_input, "negative", "User expressed dissatisfaction")
            response = "I apologize for that response. I'm learning from your feedback to do better next time!"
            return {"success": True, "response": response}
        
        else:
            # Default learning response
            response = """🧠 I'm constantly learning! Here's what I can do:

• **Learn Jokes**: Say "Here's a joke: [your joke]" to teach me
• **Get Stats**: Ask "show your stats" to see what I've learned
• **Give Feedback**: Tell me "good job" or "try again" to help me improve
• **Learn Patterns**: I automatically learn from our conversations

I adapt to your preferences and improve over time!"""
            return {"success": True, "response": response}
