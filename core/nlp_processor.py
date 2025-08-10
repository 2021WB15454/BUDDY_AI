import logging
from utils.adaptive_learning import adaptive_learning

class NLPProcessor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.adaptive_learning = adaptive_learning

    async def initialize(self):
        self.logger.info("NLPProcessor with adaptive learning initialized.")

    async def process(self, user_input, conversation_context=None):
        """Enhanced NLP processing with adaptive learning"""
        # Improved intent detection with fuzzy/partial matching
        try:
            from rapidfuzz import fuzz
            def fuzzy(text, choices, threshold=80):
                import re
                for phrase in choices:
                    # Use word boundary matching for short phrases like "hi", "hey", "chat"
                    if len(phrase) <= 4:
                        pattern = r'\b' + re.escape(phrase) + r'\b'
                        if re.search(pattern, text, re.IGNORECASE):
                            return True
                    else:
                        ratio = fuzz.partial_ratio(phrase, text)
                        if ratio >= threshold:
                            return True
                return False
        except Exception:
            def fuzzy(text, choices, threshold=80):
                import re
                for phrase in choices:
                    # Use word boundary matching for short phrases
                    if len(phrase) <= 4:
                        pattern = r'\b' + re.escape(phrase) + r'\b'
                        if re.search(pattern, text, re.IGNORECASE):
                            return True
                    else:
                        if phrase in text:
                            return True
                return False

        text = user_input.lower()

        # Enhanced intent detection with learned patterns
        learned_weather = self.adaptive_learning.get_learned_patterns_for_intent("weather") or []
        learned_jokes = self.adaptive_learning.get_learned_patterns_for_intent("joke") or []
        learned_quotes = self.adaptive_learning.get_learned_patterns_for_intent("quote") or []
        learned_general = self.adaptive_learning.get_learned_patterns_for_intent("general_conversation") or []
        
        # Ensure all learned patterns are strings
        learned_weather = [str(p) for p in learned_weather if p]
        learned_jokes = [str(p) for p in learned_jokes if p]
        learned_quotes = [str(p) for p in learned_quotes if p]
        learned_general = [str(p) for p in learned_general if p]
        
        weather_keywords = ["weather", "wether", "wethe", "wheather", "temperature", "forecast", "forcast", "rain", "sunny", "cloudy", "clody", "climate"] + learned_weather
        forecast_keywords = ["forecast", "forcast", "prediction", "outlook", "tomorrow", "next few days", "week ahead"]
        joke_keywords = ["joke", "jok", "funny", "laugh", "make me laugh", "make me laf", "make me lough"] + learned_jokes
        quote_keywords = ["quote", "qoute", "inspire", "inspaire", "motivate", "motivation", "motive"] + learned_quotes
        learning_keywords = ["learn", "teach", "remember", "forget", "stats", "learning stats", "show stats", "what have you learned", "good job", "well done", "bad", "wrong", "try again"]
        
        # Date and time related keywords - very specific for time/date queries only
        datetime_keywords = [
            # Direct time queries (very specific)
            "what time", "what's the time", "whats the time", "what time is it", "what's the time now", "whats the time now", "what is the time", "current time", "time now", "show time", "tell time", "check time", "get time", "display time",
            
            # Direct date queries (very specific)  
            "what date", "what's the date", "whats the date", "what is the date", "current date", "today's date", "todays date", "show date", "tell date", "check date", "get date",
            
            # Day queries (very specific)
            "what day", "which day", "what day is today", "what day is it", "current day", "show day", "tell day", "what is the day",
            
            # Month queries
            "month", "current month", "this month", "what month", "which month", "month today", "what month is it", "what's the month", "whats the month",
            
            # Year queries
            "year", "current year", "this year", "what year", "which year", "year today", "what year is it", "what's the year", "whats the year",
            
            # Relative date queries
            "tomorrow", "yesterday", "next day", "previous day", "last day", "the day after", "the day before",
            
            # Calendar queries
            "calendar", "week", "weekend", "weekday", "day of week", "day of month", "day of year", "week number", "quarter"
        ]
        
        # Task Management keywords
        task_keywords = [
            "task", "tasks", "todo", "to do", "to-do", "add task", "create task", "new task", "task list", "todo list", "my tasks", "show tasks", "list tasks", "all tasks", "pending tasks", "completed tasks", "complete task", "finish task", "mark task", "task done", "task complete", "delete task", "remove task", "cancel task", "update task", "edit task", "modify task", "task priority", "high priority", "urgent task", "important task", "task deadline", "due task", "overdue task", "task category", "work task", "personal task", "task progress", "task stats", "task statistics", "productivity", "task management"
        ]
        
        # Notes Management keywords  
        notes_keywords = [
            "note", "notes", "add note", "create note", "new note", "write note", "save note", "note down", "take note", "my notes", "show notes", "list notes", "all notes", "find note", "search note", "note search", "delete note", "remove note", "edit note", "update note", "modify note", "note category", "organize notes", "note folder", "favorite note", "important note", "archive note", "recent notes", "note management", "notebook", "notepad", "memo", "reminder note", "quick note", "note taking"
        ]
        
        # Calendar & Scheduling keywords - more specific
        calendar_keywords = [
            "schedule", "my schedule", "show schedule", "calendar", "my calendar", "show calendar", "view calendar", "appointment", "meeting", "event", "book appointment", "schedule meeting", "add event", "create appointment", "new meeting", "today's schedule", "tomorrow's schedule", "schedule today", "schedule tomorrow", "upcoming events", "next events", "cancel event", "cancel appointment", "reschedule", "free slot", "available slot", "when am i free", "busy", "availability", "schedule stats", "calendar stats", "meeting request", "event planning", "booking slot", "agenda", "plan meeting", "set appointment"
        ]
        
        # Contact Management keywords
        contact_keywords = [
            "contact", "contacts", "add contact", "new contact", "create contact", "contact info", "contact details", "find contact", "search contact", "my contacts", "show contacts", "list contacts", "all contacts", "delete contact", "remove contact", "edit contact", "update contact", "contact book", "address book", "phone book", "contact list", "contact management", "birthday", "birthdays", "upcoming birthdays", "contact history", "communication history", "follow up", "overdue contact", "contact stats", "relationship", "network", "professional contacts", "personal contacts"
        ]
        
        # File & Document Management keywords
        file_keywords = [
            "file", "files", "document", "documents", "register document", "track file", "add document", "find document", "search file", "locate document", "my files", "file search", "document search", "organize files", "sort files", "clean up files", "file organization", "backup files", "backup documents", "file backup", "duplicate files", "find duplicates", "storage stats", "file stats", "document stats", "file management", "document management", "file system", "folder", "directory", "archive", "file type", "file size", "file category"
        ]
        
        # Email & Communication keywords
        communication_keywords = [
            "email", "emails", "compose email", "write email", "draft email", "send email", "email template", "email templates", "create template", "use template", "communication", "communicate", "message", "messaging", "log communication", "log email", "log call", "communication history", "email history", "conversation history", "follow up", "follow-up", "pending follow", "email stats", "communication stats", "email suggestions", "email help", "help write", "template usage", "email draft", "email composition", "professional email", "business email"
        ]
        
        # Research & Knowledge keywords
        research_keywords = [
            "research", "research topic", "new research", "research project", "study", "learn", "learning", "knowledge", "add knowledge", "save knowledge", "knowledge base", "find information", "search knowledge", "what do i know about", "learning goal", "study goal", "learn about", "research session", "study session", "log research", "knowledge review", "review knowledge", "what needs review", "research progress", "learning progress", "my research", "research stats", "learning stats", "knowledge stats", "research management", "knowledge management", "study plan", "learning plan", "academic", "education", "information", "insights", "findings"
        ]
        
        # Technology and product recommendation keywords
        tech_keywords = [
            # Mobile/Phone brands and models
            "mobile", "phone", "smartphone", "cellphone", "iphone", "samsung", "poco", "xiaomi", "redmi", "realme", "oppo", "vivo", "oneplus", "huawei", "honor", "google pixel", "nokia", "motorola", "asus", "sony", "lg",
            # Technology categories
            "laptop", "computer", "tablet", "headphones", "earphones", "smartwatch", "fitness tracker", "camera", "gaming", "processor", "graphics card", "ram", "storage", "ssd", "monitor", "keyboard", "mouse",
            # Product recommendation phrases
            "which is good", "which is better", "best mobile", "best phone", "good phone", "recommend", "recommendation", "suggest", "suggestion", "compare", "comparison", "review", "reviews", "buy", "purchase", "price", "cost", "budget", "cheap", "expensive", "features", "specifications", "specs", "performance",
            # General product queries
            "which one", "what to buy", "should i buy", "worth buying", "good choice", "bad choice", "pros and cons", "advantages", "disadvantages", "value for money"
        ]
        
        # Health-related keywords for better health information detection
        health_keywords = [
            # Common diseases and conditions
            "fever", "viral fever", "bacterial fever", "typhoid", "malaria", "dengue", "chikungunya", "covid", "coronavirus", "flu", "influenza", "cold", "cough", "pneumonia", "bronchitis", "asthma", "tuberculosis", "tb", "diabetes", "hypertension", "blood pressure", "heart disease", "stroke", "cancer", "tumor", "arthritis", "migraine", "headache", "depression", "anxiety", "stress", "insomnia", "anemia", "allergy", "skin disease", "eczema", "psoriasis", "acne", "rash", "infection", "bacterial infection", "viral infection", "stomach pain", "diarrhea", "constipation", "nausea", "vomiting", "food poisoning", "gastritis", "ulcer", "kidney stones", "liver disease", "hepatitis", "jaundice",
            
            # Body parts and symptoms
            "pain", "ache", "swelling", "inflammation", "bruise", "cut", "wound", "bleeding", "injury", "fracture", "sprain", "burn", "sore throat", "runny nose", "stuffy nose", "sneezing", "itching", "redness", "discharge", "lump", "growth", "numbness", "tingling", "dizziness", "fainting", "weakness", "fatigue", "tiredness", "chest pain", "back pain", "joint pain", "muscle pain", "abdominal pain", "stomach ache", "heartburn", "acid reflux", "indigestion", "bloating", "gas", "cramps", "period pain", "menstrual cramps",
            
            # Medical terms and treatments
            "medicine", "medication", "drug", "antibiotic", "painkiller", "paracetamol", "ibuprofen", "aspirin", "treatment", "therapy", "surgery", "operation", "injection", "vaccine", "vaccination", "immunization", "prescription", "dose", "dosage", "side effects", "symptoms", "diagnosis", "medical", "health", "healthcare", "doctor", "physician", "specialist", "hospital", "clinic", "emergency", "first aid", "remedy", "cure", "healing", "recovery", "rehabilitation", "preventive", "prevention",
            
            # Health-related questions
            "health tips", "healthy diet", "nutrition", "exercise", "fitness", "weight loss", "weight gain", "vitamins", "minerals", "supplements", "immunity", "immune system", "wellness", "lifestyle", "sleep", "rest", "hydration", "water intake", "balanced diet", "calories", "protein", "carbohydrates", "fats", "fiber", "antioxidants", "mental health", "physical health", "reproductive health", "child health", "elderly health", "women health", "men health",
            
            # Common health queries
            "how to treat", "treatment for", "remedy for", "cure for", "symptoms of", "causes of", "prevention of", "risk factors", "complications", "home remedies", "natural remedies", "ayurvedic treatment", "herbal medicine", "traditional medicine", "when to see doctor", "emergency signs", "warning signs", "serious symptoms", "medical emergency", "health check", "regular checkup", "screening", "blood test", "x ray", "mri", "ct scan", "ultrasound",
            
            # Specific health conditions with common misspellings
            "diabetis", "diabities", "hypertentions", "astma", "pnemonia", "migrane", "diarrhoea", "diarria", "constipations", "anxeity", "depresion", "insomnea", "anemea", "alergy", "infecton", "inflamation", "swellings", "bleedings", "fractur", "sprayn", "bruzes", "hedache", "bckpain", "chestpain", "muscel pain", "stomac ache", "hart burn", "acidity", "gastrik", "ulser", "kidny stone", "livr disease", "hepatites", "jandice"
        ]
        
        # Personal assistant and educational keywords
        personal_assistant_keywords = [
            # Direct personal assistant terms
            "personal assistant", "personal assitant", "personal assistants", "virtual assistant", "virtual assistants", "digital assistant", "digital assistants", "ai assistant", "ai assistants", "artificial intelligence assistant", "smart assistant", "intelligent assistant",
            
            # Educational institutions and concepts
            "bits", "birla institute", "birla institute of technology", "bits pilani", "bits goa", "bits hyderabad", "bits dubai", "college", "university", "institute", "education", "academic", "institution",
            
            # AI and technology concepts
            "chatbot", "chat bot", "conversational ai", "machine learning", "artificial intelligence", "natural language processing", "nlp", "voice assistant", "speech recognition", "automation",
            
            # Assistant capabilities and features
            "assistant capabilities", "assistant features", "how can assistant help", "what can assistant do", "assistant functions", "virtual help", "digital help", "automated assistance", "smart help",
            
            # Technology and computing terms
            "binary", "binary digits", "computing", "computer science", "data storage", "information technology", "software", "application", "program", "algorithm",
            
            # General assistant queries
            "help me with", "assist me with", "can you help", "how to use assistant", "assistant guide", "assistant tutorial", "assistant information", "about assistant", "assistant definition"
        ]
        
        identity_keywords = ["who built you", "who bild you", "who made you", "who created you", "who developed you", "who is your creator", "who is your developer", "who programmed you", "who coded you", "who designed you", "who are you", "who r u", "what are you", "what r u", "tell me about yourself", "introduce yourself", "your name", "what is your name", "whats your name", "buddy", "buddy ai", "buddy ai assistant", "buddy assistant", "about buddy", "tell me about buddy", "what is buddy", "buddy information", "buddy info", "how were you developed", "how do you developed", "how were you made", "how were you created", "how were you built", "development process", "your development", "how you work", "how you were trained", "your training", "your architecture", "what you developed", "what did you develop", "what were you developed for", "what was your development", "how should i develop you", "how can i develop you", "how to develop you", "develop you", "deveop you", "develope you", "developing you", "improve you", "how to improve you", "how can i improve you", "enhance you", "upgrade you", "what did u develop", "what u developed", "how can i develop u", "how to develop u", "develop u", "improve u", "enhance u", "how did u develop", "how did u deveop", "how did you deveop", "how u developed", "how u deveop", "i want u r developer", "i want your developer", "i want ur developer", "want u r developer", "want your developer", "want ur developer", "u r developer", "ur developer", "your developer", "r developer", "the developer", "u r developed by", "you are developed by", "you r developed by", "ur developed by", "developed by", "u developed by", "you developed by", "u r created by", "you are created by", "you r created by", "ur created by", "created by", "u created by", "you created by", "u r built by", "you are built by", "you r built by", "ur built by", "built by", "u built by", "you built by", "code was developed for you by", "code was developed for u by", "your code was developed by", "ur code was developed by", "the code was developed by", "code developed for you by", "code developed for u by", "where is your birthplace", "where is ur birthplace", "where is u r birthplace", "what is your birthplace", "what is ur birthplace", "what is u r birthplace", "your birthplace", "ur birthplace", "u r birthplace", "birthplace", "where were you born", "where were u born", "where r u born", "where are you born", "where r you born", "born", "where you from", "where u from", "where r u from", "where are you from", "where r you from", "when did you born", "when did u born", "when were you born", "when were u born", "when r u born", "when are you born", "when r you born", "when was your birth", "when was ur birth", "when was u r birth", "your birth date", "ur birth date", "u r birth date", "birth date", "birthday", "your birthday", "ur birthday", "u r birthday", "when is your birthday", "when is ur birthday", "when is u r birthday", "birthday of buddy", "birthday of you", "buddy birthday", "buddy's birthday", "buddys birthday", "what is your specialty", "what is your speacility", "what is ur specialty", "what is ur speacility", "what r your specialties", "what are your specialties", "what r ur specialties", "what are ur specialties", "your specialty", "your speacility", "ur specialty", "ur speacility", "your specialties", "ur specialties", "what do you specialize in", "what do u specialize in", "what is your expertise", "what is ur expertise", "your expertise", "ur expertise", "what are you good at", "what r you good at", "what r u good at", "what are u good at", "describe yourself", "describe urself", "describe ur self", "describe u r self", "how can you describe yourself", "how can u describe yourself", "how can u describe urself", "how can u describe ur self", "how can u describe u r self", "how can u describe u r selfs", "how would you describe yourself", "how would u describe yourself", "how would u describe urself", "how would u describe ur self", "how would u describe u r self", "how do you describe yourself", "how do u describe yourself", "how do u describe urself", "how do u describe ur self", "how do u describe u r self", "how do you optimize yourself", "how do u optimize yourself", "how are you optimized", "how r you optimized", "how r u optimized", "how are u optimized", "your optimization", "ur optimization", "self optimization", "self optimisation", "optimize yourself", "optimize urself", "optimize ur self", "how do you get optimized", "how do u get optimized", "optimization process", "optimisation process", "how do you learn", "how do u learn", "your learning", "ur learning", "learning process", "which is your code", "what is your code", "which is ur code", "what is ur code", "your code", "ur code", "show me your code", "show me ur code", "show your code", "show ur code", "source code", "your source code", "ur source code", "code implementation", "implementation details", "your implementation", "ur implementation", "how are you implemented", "how r you implemented", "how r u implemented", "how are u implemented", "programming details", "coding details", "technical details", "system details", "internal workings", "how you function", "how u function", "your functions", "ur functions", "your algorithms", "ur algorithms", "code structure", "program structure", "software structure"]
        conv_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "how are you", "how r u", "how are u", "how's it going", "how do you do", "thank you", "thanks", "thx", "ty", "bye", "goodbye", "see you", "see ya", "later", "help", "what can you do", "how can you help", "assist me", "where are you", "where r u", "what is your location", "your location", "chat", "let's chat", "lets chat", "chatting", "talk", "talking", "let's talk", "lets talk", "conversation", "convo", "favour", "favor", "please", "pls", "plz", "can you", "can u", "could you", "could u", "would you", "would u", "will you", "will u", "okay", "ok", "sure", "yes", "yeah", "yep", "no", "nah", "nope", "maybe", "perhaps", "alright", "all right", "fine", "cool", "great", "awesome", "nice", "good", "bad", "terrible", "awful", "amazing", "wonderful", "excellent", "perfect", "sorry", "apologize", "excuse me", "pardon", "howri", "hiya", "heya", "sup", "wassup", "what's up", "whats up", "yo", "hei", "helo", "hllo", "hellow", "helo", "hy", "hii", "heloo", "helo", "howdy", "greetings", "salutations", "morning", "afternoon", "evening", "night", "hru", "how u", "how r you", "how are ya", "how ya doing", "how u doing", "whats good", "what's good", "how things", "how's things", "how is it", "how's it", "wassup", "wazzup", "sup mate", "hey there", "hi there", "hello there", "good day", "gud morning", "gud afternoon", "gud evening", "gd morning", "gd afternoon", "gd evening"] + learned_general

        from utils.weather import extract_location
        entities = {}
        
        # Detect educational/informational questions and route directly to Gemini
        import re
        educational_patterns = [
            r'\bwhat is\b',
            r'\bwhat are\b', 
            r'\bwhat was\b',
            r'\bwhat were\b',
            r'\bdefine\b',
            r'\bexplain\b',
            r'\bhow does\b',
            r'\bhow do\b',
            r'\bwhy does\b',
            r'\bwhy do\b',
            r'\btell me about\b',
            r'\bwho is\b',
            r'\bwho was\b',
            r'\bwhen did\b',
            r'\bwhen was\b',
            r'\bwhere is\b',
            r'\bwhere was\b'
        ]
        
        is_educational = False
        for pattern in educational_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Skip if it's about BUDDY itself (identity questions)
                if not any(keyword in text for keyword in ["you", "your", "buddy", "yourself"]):
                    is_educational = True
                    break
        
        # Intent detection - specific calendar terms first, then datetime
        if fuzzy(text, ["my calendar", "show calendar", "view calendar", "calendar", "my schedule", "show schedule", "schedule", "appointment", "meeting", "event"]):
            intent = "calendar"  # Route calendar-specific queries first
        elif fuzzy(text, datetime_keywords):
            intent = "datetime"  # Route date/time queries to datetime skill
        elif fuzzy(text, learning_keywords):
            intent = "learning"
        elif fuzzy(text, task_keywords):
            intent = "task_management"  # Route task-related queries to task management skill
        elif fuzzy(text, notes_keywords):
            intent = "notes_management"  # Route notes-related queries to notes management skill
        elif fuzzy(text, calendar_keywords):
            intent = "calendar"  # Route other calendar/scheduling queries
        elif fuzzy(text, contact_keywords):
            intent = "contact_management"  # Route contact-related queries to contact management skill
        elif fuzzy(text, file_keywords):
            intent = "file_management"  # Route file-related queries to file management skill
        elif fuzzy(text, communication_keywords):
            intent = "communication"  # Route communication-related queries to communication skill
        elif fuzzy(text, research_keywords):
            intent = "research"  # Route research/knowledge queries to research skill
        elif fuzzy(text, identity_keywords):
            intent = "identity"
        elif fuzzy(text, health_keywords):
            intent = "health"  # Route health questions to specialized health handling
        elif fuzzy(text, personal_assistant_keywords):
            intent = "personal_assistant"  # Route personal assistant and educational topics locally
        elif fuzzy(text, tech_keywords):
            intent = "openai"  # Route technology/product questions to Gemini
        elif is_educational and not fuzzy(text, health_keywords) and not fuzzy(text, personal_assistant_keywords):
            intent = "openai"  # Route educational questions directly to Gemini (but not health or personal assistant ones)
        elif fuzzy(text, forecast_keywords):
            intent = "forecast"
            location = extract_location(user_input)
            if location:
                entities["location"] = location
        elif fuzzy(text, weather_keywords):
            intent = "weather"
            location = extract_location(user_input)
            if location:
                entities["location"] = location
        elif fuzzy(text, joke_keywords):
            intent = "joke"
        elif fuzzy(text, quote_keywords):
            intent = "quote"
        elif fuzzy(text, conv_keywords, threshold=70):  # Lower threshold for conversation to catch short words
            intent = "general_conversation"
        else:
            intent = "openai"  # Route all unmatched queries to Gemini
        
        result = {"intent": intent, "entities": entities, "text": user_input}
        
        # Learn from this interaction
        self.adaptive_learning.learn_intent_pattern(text, intent)
        
        self.logger.debug(f"Processed: {user_input} -> {intent}")
        return result

    async def get_personalized_patterns(self):
        """Get user's personalized intent patterns"""
        return self.adaptive_learning.get_learned_patterns()

    async def get_stats(self):
        """Get NLP processing statistics with learning data"""
        base_stats = {
            "nlp_processor": "active",
            "adaptive_learning": "enabled"
        }
        
        # Add learning statistics
        learning_stats = self.adaptive_learning.get_stats()
        base_stats.update(learning_stats)
        
        return base_stats
