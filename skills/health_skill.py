"""
Health Information Skill for BUDDY Personal AI Assistant
Provides educational health information with appropriate disclaimers
"""
import logging
from typing import List, Dict, Any

class HealthSkill:
    """
    Health information skill that provides educational health content
    with appropriate medical disclaimers and professional advice recommendations
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common health topics with basic information
        self.health_info = {
            "dengue": {
                "definition": "A mosquito-borne viral infection that can cause severe flu-like symptoms and, in severe cases, potentially fatal complications.",
                "common_causes": ["Aedes aegypti mosquito bites", "Aedes albopictus mosquito bites", "Dengue virus (DENV) types 1, 2, 3, or 4"],
                "symptoms": ["High fever (40°C/104°F)", "Severe headache", "Eye pain (behind the eyes)", "Muscle and joint pains", "Nausea and vomiting", "Skin rash", "Bleeding (nosebleeds, gum bleeding)", "Bruising easily", "Abdominal pain", "Persistent vomiting"],
                "general_care": ["Rest and bed rest", "Drink plenty of fluids", "Use paracetamol for fever (avoid aspirin)", "Monitor symptoms closely", "Seek immediate medical attention if severe symptoms develop"],
                "see_doctor": "Immediately if experiencing severe abdominal pain, persistent vomiting, bleeding, difficulty breathing, or signs of shock. Dengue can be life-threatening and requires medical supervision."
            },
            "malaria": {
                "definition": "A life-threatening disease caused by parasites transmitted through infected mosquito bites.",
                "common_causes": ["Plasmodium parasites transmitted by Anopheles mosquitoes", "Blood transfusion (rare)", "Shared needles (rare)", "Mother to child transmission"],
                "symptoms": ["Fever and chills", "Headache", "Muscle aches", "Nausea and vomiting", "Diarrhea", "Abdominal pain", "Sweating", "Fatigue", "Anemia", "Jaundice"],
                "general_care": ["Seek immediate medical treatment", "Take prescribed antimalarial medication", "Rest and stay hydrated", "Use mosquito protection measures"],
                "see_doctor": "Immediately - malaria is a medical emergency that requires prompt diagnosis and treatment with prescription antimalarial drugs."
            },
            "viral_fever": {
                "definition": "Fever caused by viral infections, typically lasting 3-7 days with various accompanying symptoms.",
                "common_causes": ["Common cold viruses", "Influenza viruses", "Dengue virus", "Chikungunya virus", "Other viral infections"],
                "symptoms": ["Fever (usually 100.4°F/38°C or higher)", "Body aches", "Headache", "Fatigue", "Runny nose", "Sore throat", "Cough", "Loss of appetite"],
                "general_care": ["Rest and sleep", "Increase fluid intake", "Use paracetamol for fever", "Eat light, nutritious foods", "Avoid unnecessary exertion"],
                "see_doctor": "If fever persists beyond 5 days, is very high (above 103°F/39.4°C), or is accompanied by severe symptoms like difficulty breathing, persistent vomiting, or signs of dehydration."
            },
            "diabetes": {
                "definition": "A group of metabolic disorders characterized by high blood sugar levels over a prolonged period.",
                "common_causes": ["Type 1: Autoimmune destruction of insulin-producing cells", "Type 2: Insulin resistance and lifestyle factors", "Genetics", "Obesity", "Sedentary lifestyle", "Age"],
                "symptoms": ["Increased thirst", "Frequent urination", "Extreme fatigue", "Blurred vision", "Slow-healing wounds", "Frequent infections", "Unexplained weight loss", "Increased hunger"],
                "general_care": ["Monitor blood sugar levels", "Follow prescribed medication regimen", "Maintain healthy diet", "Regular exercise", "Regular medical check-ups"],
                "see_doctor": "For proper diagnosis, blood sugar monitoring, medication management, and to prevent complications. Diabetes requires ongoing medical supervision."
            },
            "hypertension": {
                "definition": "High blood pressure - a condition where blood pressure in the arteries is persistently elevated.",
                "common_causes": ["Primary: Unknown cause", "Secondary: Kidney disease, hormonal disorders", "Lifestyle factors: diet, stress, lack of exercise", "Genetics", "Age", "Obesity"],
                "symptoms": ["Often no symptoms (silent killer)", "Headaches", "Dizziness", "Nosebleeds", "Shortness of breath", "Chest pain", "Vision changes"],
                "general_care": ["Reduce sodium intake", "Regular exercise", "Maintain healthy weight", "Limit alcohol", "Manage stress", "Take prescribed medications"],
                "see_doctor": "For proper diagnosis, blood pressure monitoring, and medication management. Regular check-ups are essential to prevent heart disease and stroke."
            },
            "fever": {
                "definition": "A temporary increase in body temperature, often due to illness.",
                "common_causes": ["Viral infections", "Bacterial infections", "Heat exhaustion", "Certain medications"],
                "symptoms": ["High body temperature (above 100.4°F/38°C)", "Chills", "Sweating", "Headache", "Muscle aches"],
                "general_care": ["Rest", "Stay hydrated", "Use fever-reducing medications if appropriate", "Monitor temperature"],
                "see_doctor": "If fever is above 103°F (39.4°C), lasts more than 3 days, or is accompanied by severe symptoms"
            },
            "headache": {
                "definition": "Pain or discomfort in the head or neck area.",
                "common_causes": ["Tension", "Stress", "Dehydration", "Eye strain", "Certain foods", "Lack of sleep"],
                "symptoms": ["Pain in head, scalp, or neck", "Pressure sensation", "Throbbing or sharp pain"],
                "general_care": ["Rest in a quiet, dark room", "Apply cold or warm compress", "Stay hydrated", "Over-the-counter pain relievers"],
                "see_doctor": "If headaches are severe, frequent, sudden onset, or accompanied by fever, stiff neck, or vision changes"
            },
            "cough": {
                "definition": "A reflex action to clear the airways of irritants and secretions.",
                "common_causes": ["Viral infections", "Allergies", "Dry air", "Smoking", "Acid reflux"],
                "symptoms": ["Dry or productive cough", "Throat irritation", "Chest discomfort"],
                "general_care": ["Stay hydrated", "Use humidifier", "Honey for soothing", "Avoid irritants"],
                "see_doctor": "If cough persists more than 3 weeks, produces blood, or is accompanied by high fever"
            }
        }
    
    async def handle_health_query(self, user_input: str, conversation_context: List[Dict] = None) -> str:
        """
        Handle health-related queries with educational information and appropriate disclaimers
        
        Args:
            user_input: The user's health-related question
            conversation_context: Previous conversation context
            
        Returns:
            Educational health information with disclaimers
        """
        
        self.logger.info(f"Processing health query: {user_input}")
        
        # Check if we have specific information for common topics
        user_lower = user_input.lower()
        
        # Look for specific health topics in our knowledge base with enhanced matching
        topic_info = None
        matched_topic = None
        
        # Direct exact matches first
        for topic, info in self.health_info.items():
            if topic in user_lower:
                topic_info = info
                matched_topic = topic
                break
        
        # If no direct match, try keyword matching
        if not topic_info:
            health_keywords = {
                "dengue": ["dengue fever", "breakbone fever", "aedes", "mosquito fever", "dengue virus"],
                "malaria": ["malaria", "plasmodium", "anopheles", "antimalarial", "mosquito parasite"],
                "viral_fever": ["viral fever", "virus fever", "flu", "influenza", "common cold", "viral infection"],
                "diabetes": ["diabetes", "diabetic", "blood sugar", "glucose", "insulin", "sugar disease"],
                "hypertension": ["hypertension", "high blood pressure", "bp", "blood pressure", "elevated pressure"],
                "fever": ["fever", "temperature", "pyrexia", "febrile", "high temp"],
                "headache": ["headache", "head pain", "migraine", "head ache", "cranial pain"],
                "cough": ["cough", "coughing", "throat", "bronchitis", "respiratory"]
            }
            
            # Check for keyword matches
            for topic, keywords in health_keywords.items():
                for keyword in keywords:
                    if keyword in user_lower:
                        topic_info = self.health_info.get(topic)
                        matched_topic = topic
                        break
                if topic_info:
                    break
        
        # If still no match, try symptom-based matching
        if not topic_info:
            symptom_mapping = {
                "eye pain": "dengue",
                "muscle pain": "dengue",
                "joint pain": "dengue",
                "bleeding": "dengue",
                "bruising": "dengue",
                "abdominal pain": "dengue",
                "chills": "malaria",
                "sweating": "malaria",
                "frequent urination": "diabetes",
                "increased thirst": "diabetes",
                "blurred vision": "diabetes",
                "chest pain": "hypertension"
            }
            
            for symptom, topic in symptom_mapping.items():
                if symptom in user_lower:
                    topic_info = self.health_info.get(topic)
                    matched_topic = topic
                    break
        
        if topic_info and matched_topic:
            response = self._format_health_info(matched_topic, topic_info)
        else:
            # For other health queries, provide general guidance
            response = self._provide_general_health_guidance(user_input)
        
        # Always add medical disclaimer
        response += self._get_medical_disclaimer()
        
        return response
    
    def _format_health_info(self, topic: str, info: Dict[str, Any]) -> str:
        """Format structured health information"""
        
        response = f"**{topic.title()} - Educational Information**\n\n"
        
        response += f"**What is it?**\n{info['definition']}\n\n"
        
        if info.get('common_causes'):
            response += f"**Common Causes:**\n"
            for cause in info['common_causes']:
                response += f"• {cause}\n"
            response += "\n"
        
        if info.get('symptoms'):
            response += f"**Common Symptoms:**\n"
            for symptom in info['symptoms']:
                response += f"• {symptom}\n"
            response += "\n"
        
        if info.get('general_care'):
            response += f"**General Self-Care (for mild cases):**\n"
            for care in info['general_care']:
                response += f"• {care}\n"
            response += "\n"
        
        if info.get('see_doctor'):
            response += f"**When to See a Doctor:**\n{info['see_doctor']}\n\n"
        
        return response
    
    def _provide_general_health_guidance(self, user_input: str) -> str:
        """Provide general health guidance for topics not in our knowledge base"""
        
        response = "**Health Information**\n\n"
        response += "For specific medical questions, I recommend consulting with a qualified healthcare professional who can provide personalized advice based on your individual health situation.\n\n"
        
        response += "**General Health Tips:**\n"
        response += "• Maintain a balanced diet with plenty of fruits and vegetables\n"
        response += "• Stay hydrated by drinking adequate water\n"
        response += "• Get regular exercise appropriate for your fitness level\n"
        response += "• Ensure adequate sleep (7-9 hours for adults)\n"
        response += "• Manage stress through relaxation techniques\n"
        response += "• Schedule regular check-ups with your healthcare provider\n"
        response += "• Follow preventive care guidelines (vaccinations, screenings)\n\n"
        
        return response
    
    def _get_medical_disclaimer(self) -> str:
        """Get standard medical disclaimer"""
        
        disclaimer = "**⚠️ Important Medical Disclaimer:**\n"
        disclaimer += "This information is for educational purposes only and should not be considered as medical advice, diagnosis, or treatment. "
        disclaimer += "Always consult with a qualified healthcare professional for any health concerns, symptoms, or before making any changes to your health regimen. "
        disclaimer += "In case of medical emergencies, contact emergency services immediately.\n\n"
        disclaimer += "For personalized medical advice, please consult:\n"
        disclaimer += "• Your primary care physician\n"
        disclaimer += "• A relevant medical specialist\n"
        disclaimer += "• Your local hospital or clinic\n"
        disclaimer += "• Emergency services (in urgent situations)"
        
        return disclaimer
    
    def get_health_categories(self) -> List[str]:
        """Get list of health categories we can provide information about"""
        return list(self.health_info.keys())
    
    def add_health_info(self, topic: str, info: Dict[str, Any]):
        """Add new health information to the knowledge base"""
        self.health_info[topic] = info
        self.logger.info(f"Added health information for topic: {topic}")

# Skills interface compliance
async def handle_skill(intent: str, nlp_result: Dict[str, Any], conversation_context: List[Dict] = None) -> Dict[str, Any]:
    """
    Handle health skill requests
    
    Args:
        intent: The detected intent
        nlp_result: NLP processing result
        conversation_context: Previous conversation context
        
    Returns:
        Skill response with health information
    """
    
    health_skill = HealthSkill()
    user_input = nlp_result.get('text', '')
    
    try:
        response_text = await health_skill.handle_health_query(user_input, conversation_context)
        return {
            "success": True,
            "response": response_text,
            "source": "health_skill",
            "intent": intent
        }
    except Exception as e:
        logging.error(f"Health skill error: {e}")
        return {
            "success": False,
            "response": "I'm having trouble accessing health information right now. For medical concerns, please consult with a qualified healthcare professional.",
            "source": "health_skill_error",
            "intent": intent
        }
