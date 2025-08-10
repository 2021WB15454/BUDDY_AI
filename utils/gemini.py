import os
from dotenv import load_dotenv
from utils.api_client import api_client

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Updated Gemini API endpoint (as of 2025)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def ask_gemini(prompt: str) -> str:
    """
    Ask Gemini API a question with robust error handling and retry logic.
    
    Args:
        prompt: The question or prompt to send to Gemini
        
    Returns:
        The response from Gemini or a user-friendly error message
    """
    if not GEMINI_API_KEY:
        return "I need an API key to access my knowledge base. Please ask me about weather, jokes, or quotes instead!"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}
    
    # Use the robust API client with exponential backoff
    response = api_client.make_request(
        method="POST",
        url=GEMINI_API_URL,
        params=params,
        headers=headers,
        json_data=data,
        timeout=15,  # Slightly longer timeout for AI responses
        custom_error_message="I'm having trouble accessing my knowledge base right now"
    )
    
    # If response is a string, it's an error message
    if isinstance(response, str):
        return f"{response}. You can ask me about weather updates, jokes, or inspirational quotes instead!"
    
    # Parse successful response
    try:
        return response["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as e:
        return "I received an unexpected response format. Please try asking your question again, or ask me about weather, jokes, or quotes!"
