import logging
import random
from utils.adaptive_learning import adaptive_learning

class QuoteSkill:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The best way to get started is to quit talking and begin doing. - Walt Disney",
            "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
            "Your limitation—it's only your imagination.",
            "Push yourself, because no one else is going to do it for you.",
            "Great things never come from comfort zones.",
            "Dream it. Wish it. Do it.",
            "Success doesn't just find you. You have to go out and get it.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Dream bigger. Do bigger.",
            "Don't stop when you're tired. Stop when you're done.",
            "Wake up with determination. Go to bed with satisfaction.",
            "Do something today that your future self will thank you for.",
            "Little things make big days."
        ]
        
        # Category-based quotes for learning preferences
        self.motivational_quotes = [
            "Success doesn't just find you. You have to go out and get it.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Don't stop when you're tired. Stop when you're done.",
            "Wake up with determination. Go to bed with satisfaction."
        ]
        
        self.inspirational_quotes = [
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Dream it. Wish it. Do it."
        ]
        
        self.success_quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "In the middle of difficulty lies opportunity. - Albert Einstein"
        ]

    async def handle(self, nlp_result, context):
        user_input = nlp_result.get('text', '') if isinstance(nlp_result, dict) else str(nlp_result)
        user_input_lower = user_input.lower()
        
        # Check if user is teaching a new quote
        if adaptive_learning.is_user_teaching_quote(user_input):
            if adaptive_learning.learn_user_quote(user_input):
                response = "Thank you for sharing that inspiring quote! I'll remember it and might share it with others who need inspiration."
                adaptive_learning.learn_from_interaction(user_input, "quote_learning", response)
                return {"success": True, "response": response}
            else:
                response = "I'd love to learn that quote! Try saying something like 'Here's a quote: [your quote]' or 'Remember this quote: [quote]'"
                adaptive_learning.learn_from_interaction(user_input, "quote_learning_help", response)
                return {"success": True, "response": response}
        
        # Get learned quotes from users
        learned_quotes = adaptive_learning.get_learned_quotes()
        
        # Determine quote category based on user input and preferences
        quote_category = adaptive_learning.get_preferred_quote_category(user_input)
        
        if "motivat" in user_input_lower:
            available_quotes = self.motivational_quotes + [q for q in learned_quotes if "motivat" in q.lower()]
            category = "motivational"
        elif "inspir" in user_input_lower:
            available_quotes = self.inspirational_quotes + [q for q in learned_quotes if "inspir" in q.lower()]
            category = "inspirational"
        elif "success" in user_input_lower:
            available_quotes = self.success_quotes + [q for q in learned_quotes if "success" in q.lower()]
            category = "success"
        else:
            # Use user's preferred category or mix all quotes
            if quote_category == "motivational":
                available_quotes = self.motivational_quotes + learned_quotes
                category = "motivational"
            elif quote_category == "inspirational":
                available_quotes = self.inspirational_quotes + learned_quotes
                category = "inspirational"
            elif quote_category == "success":
                available_quotes = self.success_quotes + learned_quotes
                category = "success"
            else:
                # Mix all quotes
                available_quotes = self.quotes + learned_quotes
                category = "mixed"
        
        # Select quote
        if available_quotes:
            quote = random.choice(available_quotes)
        else:
            quote = random.choice(self.quotes)
        
        # Learn user's quote preferences
        adaptive_learning.learn_quote_preference(category, user_input)
        adaptive_learning.learn_from_interaction(user_input, "quote", quote)
        
        return {"success": True, "response": quote}
