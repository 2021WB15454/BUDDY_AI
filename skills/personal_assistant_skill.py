#!/usr/bin/env python3
"""
Personal Assistant Skill - Comprehensive personal assistance information
Handles personal assistant concepts, capabilities, and educational topics
"""
import logging
from typing import Dict, Any, Optional, List
import re

class PersonalAssistantSkill:
    """Skill for handling personal assistant and educational queries"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.knowledge_base = self._build_knowledge_base()
        
    def _build_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive knowledge base for personal assistant topics"""
        return {
            "personal_assistant": {
                "name": "Personal Assistant",
                "definition": "A personal assistant is a software application or AI system designed to help users with various tasks, information retrieval, scheduling, and daily activities.",
                "types": [
                    "Virtual Personal Assistants (AI-powered)",
                    "Digital Assistants (smartphone/computer-based)",
                    "Smart Home Assistants (voice-activated devices)",
                    "Chatbot Assistants (text-based)",
                    "Executive Assistants (human professionals)"
                ],
                "capabilities": [
                    "Task management and scheduling",
                    "Information retrieval and research",
                    "Email and communication management",
                    "Appointment setting and calendar management",
                    "Reminder and notification services",
                    "Travel planning and booking",
                    "Document preparation and organization",
                    "Contact management",
                    "Simple automation tasks",
                    "Entertainment and content recommendations"
                ],
                "popular_examples": [
                    "Apple Siri - Voice assistant for iOS devices",
                    "Google Assistant - Multi-platform AI assistant",
                    "Amazon Alexa - Smart home voice assistant", 
                    "Microsoft Cortana - Windows-based assistant",
                    "Samsung Bixby - Samsung device assistant",
                    "IBM Watson Assistant - Enterprise AI assistant"
                ],
                "benefits": [
                    "Increased productivity and efficiency",
                    "24/7 availability for assistance",
                    "Hands-free operation capability",
                    "Quick information access",
                    "Task automation and time-saving",
                    "Personalized user experience",
                    "Multi-language support",
                    "Integration with multiple services"
                ]
            },
            "bits": {
                "name": "BITS (Multiple Meanings)",
                "definitions": [
                    {
                        "context": "Education",
                        "full_form": "Birla Institute of Technology and Science",
                        "description": "BITS is a prestigious private technical university in India with campuses in Pilani, Goa, Hyderabad, and Dubai. Known for engineering, science, and management programs.",
                        "established": "1964",
                        "notable_features": [
                            "Practice School Program (industry internships)",
                            "No entrance exam (admission based on BITSAT)",
                            "High academic standards and industry connections",
                            "Strong alumni network in technology sectors"
                        ]
                    },
                    {
                        "context": "Computing",
                        "full_form": "Binary Digits",
                        "description": "Bits are the fundamental units of information in computing, representing binary values (0 or 1).",
                        "details": [
                            "8 bits = 1 byte",
                            "Used to measure data storage and transmission",
                            "Foundation of all digital computing",
                            "CPU architecture often described in bits (32-bit, 64-bit)"
                        ]
                    },
                    {
                        "context": "Cryptocurrency",
                        "full_form": "Bitcoin units",
                        "description": "Informal reference to Bitcoin cryptocurrency or small fractions of Bitcoin."
                    }
                ]
            },
            "ai_assistant": {
                "name": "AI Assistant",
                "definition": "An artificial intelligence-powered software designed to understand natural language and assist users with various tasks through conversation and automated actions.",
                "key_technologies": [
                    "Natural Language Processing (NLP)",
                    "Machine Learning and Deep Learning",
                    "Speech Recognition and Text-to-Speech",
                    "Knowledge Graphs and Databases",
                    "API Integrations and Cloud Computing",
                    "Conversational AI and Dialog Management"
                ],
                "applications": [
                    "Customer service and support",
                    "Personal productivity assistance",
                    "Educational tutoring and learning",
                    "Healthcare information and guidance",
                    "Smart home automation",
                    "Business process automation",
                    "Content creation and writing assistance",
                    "Language translation and interpretation"
                ],
                "limitations": [
                    "Context understanding challenges",
                    "Lack of real-world experience",
                    "Potential bias in responses",
                    "Limited emotional intelligence",
                    "Dependence on training data quality",
                    "Privacy and security concerns"
                ]
            },
            "virtual_assistant": {
                "name": "Virtual Assistant",
                "definition": "A software agent that can perform tasks or services for an individual based on commands or questions.",
                "evolution": [
                    "1960s: Early command-line interfaces",
                    "1990s: Desktop assistants (Microsoft Clippy)",
                    "2000s: Web-based virtual assistants",
                    "2010s: Mobile voice assistants (Siri, Google Now)",
                    "2020s: Advanced AI assistants with conversational abilities"
                ],
                "features": [
                    "Voice and text interaction",
                    "Multi-device synchronization",
                    "Personalization and user preferences",
                    "Third-party app integration",
                    "Continuous learning from interactions",
                    "Proactive suggestions and notifications"
                ]
            },
            "chatbot": {
                "name": "Chatbot",
                "definition": "A computer program designed to simulate conversation with human users through text or voice interactions.",
                "types": [
                    "Rule-based chatbots (scripted responses)",
                    "AI-powered chatbots (machine learning)",
                    "Hybrid chatbots (combination approach)",
                    "Voice-enabled chatbots",
                    "Social media chatbots"
                ],
                "use_cases": [
                    "Customer support automation",
                    "Lead generation and sales",
                    "FAQ and information retrieval",
                    "Entertainment and engagement",
                    "Educational assistance",
                    "Healthcare preliminary screening",
                    "E-commerce shopping assistance"
                ]
            }
        }
    
    def _find_relevant_topic(self, query: str) -> Optional[str]:
        """Find the most relevant topic based on the query"""
        query_lower = query.lower().strip()
        
        # Direct keyword matching
        if any(keyword in query_lower for keyword in ["personal assistant", "personal assitant", "personal assistants"]):
            return "personal_assistant"
        elif "bits" in query_lower and any(context in query_lower for context in ["college", "university", "institute", "education", "pilani"]):
            return "bits"
        elif "bits" in query_lower and any(context in query_lower for context in ["computer", "computing", "binary", "data"]):
            return "bits"
        elif "bits" in query_lower:
            return "bits"  # Default to educational context
        elif any(keyword in query_lower for keyword in ["ai assistant", "artificial intelligence assistant", "ai-powered assistant"]):
            return "ai_assistant"
        elif any(keyword in query_lower for keyword in ["virtual assistant", "virtual assistants", "digital assistant"]):
            return "virtual_assistant"
        elif any(keyword in query_lower for keyword in ["chatbot", "chat bot", "conversational ai"]):
            return "chatbot"
        
        # Educational patterns for general topics
        educational_patterns = [
            r'\bwhat is\b', r'\bwhat are\b', r'\bdefine\b', r'\bexplain\b',
            r'\btell me about\b', r'\bwho is\b', r'\bhow does\b', r'\bwhy\b'
        ]
        
        for pattern in educational_patterns:
            if re.search(pattern, query_lower):
                if "assistant" in query_lower:
                    return "personal_assistant"
                elif "bits" in query_lower:
                    return "bits"
                elif "ai" in query_lower:
                    return "ai_assistant"
                elif "virtual" in query_lower:
                    return "virtual_assistant"
                elif "chatbot" in query_lower or "chat bot" in query_lower:
                    return "chatbot"
        
        return None
    
    def _format_response(self, topic_key: str, topic_data: Dict[str, Any]) -> str:
        """Format the response for a given topic"""
        response_lines = []
        
        if topic_key == "bits":
            response_lines.append(f"**{topic_data['name']} - Educational Information**\n")
            
            for definition in topic_data['definitions']:
                response_lines.append(f"**{definition['context']} Context:**")
                response_lines.append(f"• Full Form: {definition['full_form']}")
                response_lines.append(f"• Description: {definition['description']}")
                
                if 'established' in definition:
                    response_lines.append(f"• Established: {definition['established']}")
                
                if 'notable_features' in definition:
                    response_lines.append("• Notable Features:")
                    for feature in definition['notable_features']:
                        response_lines.append(f"  - {feature}")
                
                if 'details' in definition:
                    response_lines.append("• Details:")
                    for detail in definition['details']:
                        response_lines.append(f"  - {detail}")
                
                response_lines.append("")  # Add spacing between definitions
                
        else:
            response_lines.append(f"**{topic_data['name']} - Comprehensive Information**\n")
            
            if 'definition' in topic_data:
                response_lines.append(f"**Definition:**")
                response_lines.append(f"{topic_data['definition']}\n")
            
            if 'types' in topic_data:
                response_lines.append("**Types:**")
                for item_type in topic_data['types']:
                    response_lines.append(f"• {item_type}")
                response_lines.append("")
            
            if 'capabilities' in topic_data:
                response_lines.append("**Key Capabilities:**")
                for capability in topic_data['capabilities']:
                    response_lines.append(f"• {capability}")
                response_lines.append("")
            
            if 'features' in topic_data:
                response_lines.append("**Key Features:**")
                for feature in topic_data['features']:
                    response_lines.append(f"• {feature}")
                response_lines.append("")
            
            if 'key_technologies' in topic_data:
                response_lines.append("**Key Technologies:**")
                for tech in topic_data['key_technologies']:
                    response_lines.append(f"• {tech}")
                response_lines.append("")
            
            if 'applications' in topic_data:
                response_lines.append("**Applications:**")
                for app in topic_data['applications']:
                    response_lines.append(f"• {app}")
                response_lines.append("")
            
            if 'use_cases' in topic_data:
                response_lines.append("**Common Use Cases:**")
                for use_case in topic_data['use_cases']:
                    response_lines.append(f"• {use_case}")
                response_lines.append("")
            
            if 'popular_examples' in topic_data:
                response_lines.append("**Popular Examples:**")
                for example in topic_data['popular_examples']:
                    response_lines.append(f"• {example}")
                response_lines.append("")
            
            if 'benefits' in topic_data:
                response_lines.append("**Benefits:**")
                for benefit in topic_data['benefits']:
                    response_lines.append(f"• {benefit}")
                response_lines.append("")
            
            if 'evolution' in topic_data:
                response_lines.append("**Evolution Timeline:**")
                for evolution in topic_data['evolution']:
                    response_lines.append(f"• {evolution}")
                response_lines.append("")
            
            if 'limitations' in topic_data:
                response_lines.append("**Limitations:**")
                for limitation in topic_data['limitations']:
                    response_lines.append(f"• {limitation}")
                response_lines.append("")
        
        # Add educational disclaimer
        response_lines.extend([
            "**📚 Educational Information:**",
            "This information is provided for educational and informational purposes. For the most current and detailed information, especially for academic institutions or technical specifications, please refer to official sources and documentation.",
            "",
            "**💡 Need More Help?**",
            "I can also assist you with:",
            "• Weather information and forecasts",
            "• Health and medical information",
            "• Technology recommendations",
            "• General conversation and questions",
            "• Jokes and inspirational quotes"
        ])
        
        return "\n".join(response_lines)
    
    async def handle_personal_assistant_query(self, user_input: str, context: Dict[str, Any]) -> str:
        """
        Handle personal assistant and educational queries
        
        Args:
            user_input: The user's query
            context: Additional context information
            
        Returns:
            Formatted response with personal assistant information
        """
        try:
            self.logger.info(f"Processing personal assistant query: {user_input}")
            
            # Find relevant topic
            topic_key = self._find_relevant_topic(user_input)
            
            if topic_key and topic_key in self.knowledge_base:
                topic_data = self.knowledge_base[topic_key]
                return self._format_response(topic_key, topic_data)
            
            # General personal assistant information if no specific topic found
            return self._get_general_assistant_info()
            
        except Exception as e:
            self.logger.error(f"Error handling personal assistant query: {e}")
            return self._get_fallback_response()
    
    def _get_general_assistant_info(self) -> str:
        """Get general personal assistant information"""
        return """**Personal Assistant - General Information**

**What is a Personal Assistant?**
A personal assistant is designed to help you with various tasks and provide information on demand. Modern personal assistants use artificial intelligence to understand and respond to your needs.

**How I Can Help You:**
• **Weather Information** - Get current weather and forecasts for any location
• **Health Information** - Access medical information and health tips (educational purposes)
• **Technology Advice** - Get recommendations for smartphones, laptops, and gadgets
• **General Knowledge** - Ask questions about various topics and concepts
• **Entertainment** - Request jokes, inspirational quotes, and casual conversation
• **Learning Assistance** - Get explanations and educational information

**Popular Personal Assistant Types:**
• Voice Assistants (Siri, Google Assistant, Alexa)
• Chatbot Assistants (like me!)
• Smart Home Assistants
• Business and Productivity Assistants

**My Capabilities:**
• Natural language understanding
• Context-aware responses
• Multi-topic knowledge base
• Real-time weather data
• Health and medical information
• Technology recommendations
• Conversational interaction

**📱 Try These Commands:**
• "What's the weather in [city]?"
• "Tell me about [health topic]"
• "Recommend a good smartphone"
• "Tell me a joke"
• "Give me an inspirational quote"

Feel free to ask me anything - I'm here to help!"""
    
    def _get_fallback_response(self) -> str:
        """Get fallback response for errors"""
        return """**Personal Assistant Information**

I'm here to help you with various tasks! While I encountered an issue processing your specific query, I can assist you with:

• **Weather Updates** - Current conditions and forecasts
• **Health Information** - Medical information and health tips  
• **Technology Advice** - Product recommendations and tech info
• **General Questions** - Educational topics and explanations
• **Entertainment** - Jokes, quotes, and conversation

Please try rephrasing your question or ask me about any of these topics. I'm designed to be your helpful personal assistant!"""

# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_personal_assistant():
        skill = PersonalAssistantSkill()
        
        test_queries = [
            "What is a personal assistant?",
            "Personal assistant",
            "what is BITS",
            "Tell me about BITS Pilani",
            "AI assistant",
            "virtual assistant capabilities",
            "chatbot information",
            "How can personal assistants help?"
        ]
        
        print("Testing Personal Assistant Skill:")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 30)
            response = await skill.handle_personal_assistant_query(query, {})
            print(response[:200] + "..." if len(response) > 200 else response)
    
    asyncio.run(test_personal_assistant())
