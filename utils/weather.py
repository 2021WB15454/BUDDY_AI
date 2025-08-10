
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
        "bangalor": "Bangalore",
        "bangaluru": "Bangalore",
        "mumbay": "Mumbai",
        "kolkatta": "Kolkata",
        "chenai": "Chennai",
        "dilli": "Delhi",
        "hydrabad": "Hyderabad"
    }
    
    # Try to extract after 'in' or 'for'
    match = re.search(r"(?:in|for)\s+([a-zA-Z\s]+)", text)
    if match:
        location = match.group(1).strip()
    else:
        # If input starts with 'weather' or similar, get the next word(s)
        match2 = re.match(r"\s*(?:weather|wether|wethe|wheather|temperature|forecast|forcast|climate)\s+([a-zA-Z\s]+)", text.lower())
        if match2:
            location = match2.group(1).strip()
        else:
            return None
    
    # Apply spelling corrections
    location_lower = location.lower()
    if location_lower in location_corrections:
        return location_corrections[location_lower]
    
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
