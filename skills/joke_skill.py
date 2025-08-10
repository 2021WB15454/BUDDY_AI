import logging
import random
from utils.adaptive_learning import adaptive_learning

class JokeSkill:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.jokes = [
            "Why did the AI cross the road? To optimize the chicken!",
            "Why don't robots ever panic? They have amazing circuit breakers!",
            "What do you call a robot who likes to sing? A cyber-crooner!",
            "Why did the computer go to therapy? It had too many bytes of emotional baggage!",
            "What's a robot's favorite type of music? Heavy metal!",
            "Why don't AIs ever get tired? They always run on energy-efficient algorithms!",
            "What do you call an AI that can cook? A chef-bot with great taste algorithms!",
            "Why did the chatbot become a comedian? It had great response time!",
            "What's an AI's favorite snack? Microchips!",
            "Why don't robots ever get lost? They always have their GPS algorithms running!"
        ]
        
        # Add some BUDDY-specific jokes
        self.buddy_jokes = [
            "Why is BUDDY the best assistant? Because I'm programmed to be helpful, not just artificial!",
            "What's BUDDY's favorite hobby? Debugging conversations and optimizing laughs!",
            "Why does BUDDY never get tired? Because I run on pure enthusiasm algorithms!",
            "What makes BUDDY special? I'm not just smart, I'm BUDDY smart!",
            "Why is BUDDY always positive? I was trained on happy data!"
        ]

    async def handle(self, nlp_result, context):
        user_input = nlp_result.get('text', '') if isinstance(nlp_result, dict) else str(nlp_result)
        
        # Check if user is teaching a new joke
        if adaptive_learning.is_user_teaching_joke(user_input):
            if adaptive_learning.learn_user_joke(user_input):
                return {"success": True, "response": "Haha! Thanks for teaching me that joke! I'll remember it and might tell it to others. Want to hear one of mine?"}
            else:
                return {"success": True, "response": "I'd love to learn a new joke from you! Try saying something like 'Here's a joke: [your joke]'"}
        
        # Get learned jokes from users
        learned_jokes = adaptive_learning.get_learned_jokes()
        
        # Check if user wants a joke about BUDDY specifically
        if any(word in user_input.lower() for word in ['about you', 'about buddy', 'about yourself', 'buddy joke']):
            joke = random.choice(self.buddy_jokes)
        else:
            # Combine all available jokes: built-in + BUDDY-specific + user-taught
            all_jokes = self.jokes + self.buddy_jokes + learned_jokes
            joke = random.choice(all_jokes)
        
        # Learn from this interaction
        adaptive_learning.learn_from_interaction(user_input, "joke", joke)
        
        return {"success": True, "response": joke}
