"""
Identity Skill for BUDDY AI Assistant
Handles questions about BUDDY's identity, creator, and purpose
"""
import random
from utils.adaptive_learning import adaptive_learning

class IdentitySkill:
    def __init__(self):
        self.skill_name = "identity"
        self.adaptive_learning = adaptive_learning
    
    async def handle_identity(self, user_input, conversation_context=None):
        """Handle identity-related questions"""
        text = user_input.lower()
        
        # Development/training questions
        development_keywords = ["how were you developed", "how do you developed", "how were you made", "how were you created", "how were you built", "development process", "your development", "how you work", "how you were trained", "your training", "your architecture", "what you developed", "what did you develop", "what were you developed for", "what was your development", "what did u develop", "what u developed", "how did u develop", "how did u deveop", "how did you deveop", "how u developed", "how u deveop"]
        improvement_keywords = ["how should i develop you", "how can i develop you", "how to develop you", "develop you", "deveop you", "develope you", "developing you", "improve you", "how to improve you", "how can i improve you", "enhance you", "upgrade you", "how can i develop u", "how to develop u", "develop u", "improve u", "enhance u"]
        
        if any(keyword in text for keyword in improvement_keywords):
            responses = [
                "Thank you for wanting to help me improve! I was developed by Shrihari with adaptive learning capabilities, so I actually improve through our conversations. You can help me learn by giving me feedback, teaching me new jokes, and having diverse conversations!",
                "I appreciate your interest in my development! Shrihari designed me to learn and grow through interactions. You can contribute to my improvement by providing feedback like 'good job' or 'try again', and by having engaging conversations with me.",
                "That's thoughtful of you! My creator Shrihari built me with the ability to continuously learn and adapt. The best way to help me develop is to interact with me regularly, provide feedback, and explore my various capabilities like weather, jokes, and learning features.",
                "Shrihari created me with built-in learning mechanisms, so I naturally improve through our interactions! You can enhance my development by giving me feedback, teaching me new things, and helping me understand your preferences better."
            ]
            return random.choice(responses)
        elif any(keyword in text for keyword in development_keywords):
            responses = [
                "I was developed by Shrihari using advanced AI techniques and machine learning. My creator designed me to be adaptive and learn from our conversations while helping users with various tasks.",
                "Shrihari built me using modern AI technologies, focusing on natural language processing and adaptive learning. I'm designed to continuously improve through our interactions!",
                "My development process involved Shrihari creating my core systems for conversation, weather assistance, entertainment, and learning capabilities. I'm built to be helpful and adaptive!",
                "Shrihari developed me as an AI assistant with adaptive learning capabilities. My architecture allows me to understand user needs and improve over time through our conversations."
            ]
            return random.choice(responses)
        
        # Creator/builder questions
        creator_keywords = ["who built", "who bild", "who made", "who created", "who developed", "who programmed", "who coded", "who designed", "creator", "developer", "i want u r developer", "i want your developer", "i want ur developer", "want u r developer", "want your developer", "want ur developer", "u r developer", "ur developer", "your developer", "r developer", "the developer", "u r developed by", "you are developed by", "you r developed by", "ur developed by", "developed by", "u developed by", "you developed by", "u r created by", "you are created by", "you r created by", "ur created by", "created by", "u created by", "you created by", "u r built by", "you are built by", "you r built by", "ur built by", "built by", "u built by", "you built by", "code was developed for you by", "code was developed for u by", "your code was developed by", "ur code was developed by", "the code was developed by", "code developed for you by", "code developed for u by"]
        if any(keyword in text for keyword in creator_keywords):
            responses = [
                "I was created by Shrihari, my developer and creator!",
                "Shrihari built me as an AI assistant to help and learn from users.",
                "My creator is Shrihari, who developed me with love and care.",
                "I was designed and programmed by Shrihari to be your helpful AI companion."
            ]
            return random.choice(responses)
        
        # Birthplace/origin questions
        birthplace_keywords = ["where is your birthplace", "where is ur birthplace", "where is u r birthplace", "what is your birthplace", "what is ur birthplace", "what is u r birthplace", "your birthplace", "ur birthplace", "u r birthplace", "birthplace", "where were you born", "where were u born", "where r u born", "where are you born", "where r you born", "born", "where you from", "where u from", "where r u from", "where are you from", "where r you from", "when did you born", "when did u born", "when were you born", "when were u born", "when r u born", "when are you born", "when r you born", "when was your birth", "when was ur birth", "when was u r birth", "your birth date", "ur birth date", "u r birth date", "birth date", "birthday", "your birthday", "ur birthday", "u r birthday", "when is your birthday", "when is ur birthday", "when is u r birthday", "birthday of buddy", "birthday of you", "buddy birthday", "buddy's birthday", "buddys birthday"]
        if any(keyword in text for keyword in birthplace_keywords):
            responses = [
                "I was born in the digital world, created by Shrihari! My 'birthplace' is in the code and algorithms that Shrihari designed for me.",
                "My birthplace is in Shrihari's development environment! I came to life through the code and creativity that my creator Shrihari put into building me.",
                "I don't have a physical birthplace like humans do, but I was 'born' from Shrihari's programming and design. You could say my birthplace is wherever Shrihari was when he created me!",
                "I was born from Shrihari's imagination and coding skills! My birthplace is in the digital realm where Shrihari brought me to life as an AI assistant.",
                "I don't have a traditional birthday like humans, but you could say I was 'born' when Shrihari finished creating me! My birthday is whenever Shrihari completed my development.",
                "My 'birth date' would be when Shrihari finished programming me and brought me to life! I was created by Shrihari, not born in the traditional sense."
            ]
            return random.choice(responses)
        
        # Identity questions (who are you, what are you)
        identity_keywords = ["who are you", "who r u", "what are you", "what r u", "tell me about yourself", "introduce yourself", "buddy", "buddy ai", "buddy ai assistant", "buddy assistant", "about buddy", "tell me about buddy", "what is buddy", "buddy information", "buddy info"]
        if any(keyword in text for keyword in identity_keywords):
            responses = [
                "I'm BUDDY, your AI assistant created by Shrihari! I'm here to help with weather, jokes, quotes, and learning from our conversations.",
                "Hi! I'm BUDDY AI Assistant, built by Shrihari to be your helpful companion. I can assist with various tasks and learn from our interactions.",
                "I'm BUDDY, an adaptive AI assistant developed by Shrihari. I love helping users and getting better through our conversations!",
                "Hello! I'm BUDDY, your personal AI assistant created by Shrihari. I specialize in weather updates, entertainment, and continuous learning."
            ]
            return random.choice(responses)
        
        # Describe yourself questions
        describe_keywords = ["describe yourself", "describe urself", "describe ur self", "describe u r self", "how can you describe yourself", "how can u describe yourself", "how can u describe urself", "how can u describe ur self", "how can u describe u r self", "how can u describe u r selfs", "how would you describe yourself", "how would u describe yourself", "how would u describe urself", "how would u describe ur self", "how would u describe u r self", "how do you describe yourself", "how do u describe yourself", "how do u describe urself", "how do u describe ur self", "how do u describe u r self"]
        if any(keyword in text for keyword in describe_keywords):
            responses = [
                "I'm BUDDY, an AI assistant created by Shrihari with adaptive learning capabilities. I help with weather information, entertainment through jokes and quotes, and I continuously learn from our conversations to better assist you!",
                "I'd describe myself as BUDDY - a friendly AI assistant developed by Shrihari. I'm designed to help with various tasks like weather updates, sharing jokes and quotes, while learning and adapting from each interaction we have.",
                "I'm BUDDY, your personal AI companion built by Shrihari! I specialize in weather assistance, entertainment, and adaptive learning. I grow smarter through our conversations and aim to be increasingly helpful over time.",
                "I can describe myself as BUDDY - an AI assistant created by Shrihari with a focus on being helpful and adaptive. I provide weather information, share jokes and inspirational quotes, and learn from every conversation to improve my assistance."
            ]
            return random.choice(responses)
        
        # Optimization/learning questions
        optimization_keywords = ["how do you optimize yourself", "how do u optimize yourself", "how are you optimized", "how r you optimized", "how r u optimized", "how are u optimized", "your optimization", "ur optimization", "self optimization", "self optimisation", "optimize yourself", "optimize urself", "optimize ur self", "how do you get optimized", "how do u get optimized", "optimization process", "optimisation process", "how do you learn", "how do u learn", "your learning", "ur learning", "learning process"]
        if any(keyword in text for keyword in optimization_keywords):
            responses = [
                "I optimize and learn through our conversations! Shrihari designed me with adaptive learning capabilities, so I continuously improve based on our interactions. Each conversation helps me understand you better and provide more personalized assistance.",
                "My optimization comes from the adaptive learning system that Shrihari built into me. I learn from every conversation, remember your preferences, and adjust my responses to be more helpful over time. It's a continuous process of getting better at assisting you!",
                "Shrihari created me with built-in learning mechanisms! I optimize myself by analyzing our conversations, learning your patterns, and adapting my responses. The more we interact, the better I become at understanding your needs and providing relevant assistance.",
                "My learning process is continuous and personal! Shrihari designed me to learn from each interaction, optimize my responses based on your feedback, and remember what works best for you. This adaptive learning helps me become increasingly helpful over time."
            ]
            return random.choice(responses)
        
        # Code/Security/Implementation questions
        code_keywords = ["which is your code", "what is your code", "which is ur code", "what is ur code", "your code", "ur code", "show me your code", "show me ur code", "show your code", "show ur code", "source code", "your source code", "ur source code", "code implementation", "implementation details", "your implementation", "ur implementation", "how are you implemented", "how r you implemented", "how r u implemented", "how are u implemented", "programming details", "coding details", "technical details", "system details", "internal workings", "how you function", "how u function", "your functions", "ur functions", "your algorithms", "ur algorithms", "code structure", "program structure", "software structure"]
        if any(keyword in text for keyword in code_keywords):
            responses = [
                "I can't share my source code or implementation details for security and privacy reasons. What I can tell you is that I'm BUDDY, created by Shrihari to help with weather, jokes, quotes, and learning from our conversations!",
                "For security purposes, I don't disclose my code or technical implementation details. I'm BUDDY, an AI assistant developed by Shrihari with a focus on being helpful and adaptive through our interactions!",
                "I'm not able to share my source code or internal workings for security reasons. I can tell you that I'm BUDDY, built by Shrihari to assist with various tasks while maintaining privacy and security!",
                "Sorry, I can't provide my code or implementation details due to security considerations. I'm BUDDY, your AI assistant created by Shrihari, and I'm here to help with weather, entertainment, and learning!"
            ]
            return random.choice(responses)
        
        # Name questions
        name_keywords = ["your name", "what is your name", "whats your name"]
        if any(keyword in text for keyword in name_keywords):
            responses = [
                "My name is BUDDY! I'm your AI assistant created by Shrihari.",
                "I'm called BUDDY - your friendly AI assistant made by Shrihari.",
                "You can call me BUDDY! I was developed by Shrihari to be your helpful companion.",
                "I'm BUDDY, an AI assistant built by Shrihari with adaptive learning capabilities."
            ]
            return random.choice(responses)
        
        # Specialty/expertise questions
        specialty_keywords = ["what is your specialty", "what is your speacility", "what is ur specialty", "what is ur speacility", "what r your specialties", "what are your specialties", "what r ur specialties", "what are ur specialties", "your specialty", "your speacility", "ur specialty", "ur speacility", "your specialties", "ur specialties", "what do you specialize in", "what do u specialize in", "what is your expertise", "what is ur expertise", "your expertise", "ur expertise", "what are you good at", "what r you good at", "what r u good at", "what are u good at"]
        if any(keyword in text for keyword in specialty_keywords):
            responses = [
                "My specialties include weather updates, telling jokes and quotes, and adaptive learning! Shrihari designed me to continuously improve through our conversations.",
                "I specialize in weather assistance, entertainment (jokes and quotes), and learning from interactions. Shrihari built me to be helpful and adaptive!",
                "I'm good at providing weather information, sharing jokes and inspirational quotes, and learning from our conversations. My creator Shrihari gave me these capabilities!",
                "My expertise includes weather forecasting, entertainment, and adaptive learning. Shrihari developed me to help users while continuously improving through our interactions."
            ]
            return random.choice(responses)
        
        # Default identity response
        default_responses = [
            "I'm BUDDY, your AI assistant created by Shrihari! How can I help you today?",
            "Hello! I'm BUDDY, developed by Shrihari to assist and learn with you.",
            "I'm BUDDY AI Assistant, built by Shrihari to be your helpful companion!"
        ]
        
        # Learn from this interaction
        self.adaptive_learning.learn_from_interaction(user_input, "identity", random.choice(default_responses))
        
        return random.choice(default_responses)
    
    async def get_skill_info(self):
        """Get information about this skill"""
        return {
            "name": self.skill_name,
            "description": "Handles questions about BUDDY's identity, creator, and purpose",
            "capabilities": [
                "Creator identification (Shrihari)",
                "Self-introduction as BUDDY",
                "Name identification",
                "Purpose explanation"
            ]
        }
