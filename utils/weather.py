
import os
import re
from dotenv import load_dotenv
from utils.api_client import api_client

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


def extract_location(text):
    # Common location spelling corrections
    location_corrections = {
        "malasiya": "Malaysia",
        "malaysiya": "Malaysia", 
        "kolalampur": "Kuala Lumpur",
        "kualalampur": "Kuala Lumpur",
        "kolalumpur": "Kuala Lumpur",
        "israil": "Israel",
        "isreal": "Israel",
        "singapur": "Singapore",
        "bangalur": "Bangalore",
        "bangaluru": "Bangalore",
        "bengaluru": "Bangalore",
        "mumbay": "Mumbai",
        "kolkatta": "Kolkata",
        "chenai": "Chennai",
        "dilli": "Delhi",
        "hydrabad": "Hyderabad",
        "maduri": "Madurai",
        "madrai": "Madurai",
        "thirunelveli": "Tirunelveli",
        "thiruelveli": "Tirunelveli",
        "tiruvelveli": "Tirunelveli",
        "coimbatur": "Coimbatore",
        "kovai": "Coimbatore"
    }
    
    # Import the global location database for enhanced matching
    try:
        from utils.global_location_database import global_location_db
    except ImportError:
        global_location_db = None
    
    # Try to extract after 'in' or 'for'
    match = re.search(r"(?:in|for)\s+([a-zA-Z\s]+?)(?:\?|$)", text)
    if match:
        location = match.group(1).strip()
    else:
        # If input starts with 'weather' or similar, get the next word(s)
        match2 = re.match(r"\s*(?:weather|wether|wethe|wheather|temperature|forecast|forcast|climate)\s+([a-zA-Z\s]+?)(?:\?|$)", text.lower())
        if match2:
            location = match2.group(1).strip()
        else:
            # NEW: Handle format like "madurai weather" or "chennai temperature"
            weather_at_end = re.search(r"^([a-zA-Z\s]+?)\s+(?:weather|wether|wethe|wheather|temperature|forecast|forcast|climate)$", text.lower().strip())
            if weather_at_end:
                location = weather_at_end.group(1).strip()
            else:
                # NEW: If no weather keywords, check if the entire text is a location name
                text_clean = text.strip()
                # Skip obvious non-location phrases
                if text_clean.lower() in ["what's the weather like", "how's the weather", "weather please", "tell me weather"]:
                    return None
                    
                if global_location_db:
                    best_match, loc_type, confidence, suggestions = global_location_db.find_location(text_clean)
                    if confidence > 0.7:  # High confidence match
                        location = best_match
                    else:
                        return None
                else:
                    # Fallback: if it's a single word that looks like a city name
                    if len(text_clean.split()) <= 2 and text_clean.replace(" ", "").isalpha():
                        location = text_clean
                    else:
                        return None
    
    # Apply spelling corrections
    location_lower = location.lower()
    if location_lower in location_corrections:
        return location_corrections[location_lower]
    
    # Use global location database for enhanced matching
    if global_location_db:
        best_match, loc_type, confidence, suggestions = global_location_db.find_location(location)
        if confidence > 0.7:
            return best_match
    
    return location


def get_weather_forecast(location: str) -> str:
    if not WEATHER_API_KEY:
        return "[Weather API key not set. Please set WEATHER_API_KEY in your environment.]"
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        # Use robust API client with retry logic
        response = api_client.make_request(
            method="GET",
            url=WEATHER_API_URL,
            params=params,
            timeout=10,
            custom_error_message="Weather service temporarily unavailable"
        )
        
        if isinstance(response, str):
            return response  # Error message from API client
            
        if not response or 'weather' not in response:
            return f"Sorry, I couldn't find weather data for {location}."
            
        desc = response['weather'][0]['description'].capitalize()
        temp = response['main']['temp']
        city = response['name']
        country = response['sys']['country']
        return f"Weather in {city}, {country}: {desc}, {temp}°C."
    except Exception as e:
        return f"[Weather API error: {e}]"
