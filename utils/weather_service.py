"""
Weather Service for BUDDY Personal AI Assistant
Provides real-time weather information using OpenWeatherMap API with spell checking
"""
import asyncio
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import json
import sys
import os

# Add utils to path for spell checker and global location database
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.location_spellcheck import location_checker
from utils.global_location_database import global_location_db
from utils.api_client import api_client


class WeatherService:
    """
    Weather service to fetch real-time weather data with location spell checking
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # OpenWeatherMap API (free tier available)
        self.api_key = os.getenv('WEATHER_API_KEY', '')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Default location if none specified
        self.default_location = self.config.get('weather', {}).get('default_location', 'New York')
        
        self.available = bool(self.api_key)
        
        if not self.available:
            self.logger.info("Weather service unavailable - no API key configured")
        else:
            self.logger.info("Weather service initialized with OpenWeatherMap API")
    
    async def get_current_weather(self, location: str = None) -> Dict[str, Any]:
        """Get current weather for a location using the global location database"""
        if not self.available:
            return self._get_fallback_weather(location)

        location = location or self.default_location

        # Step 1: Resolve location using GlobalLocationDatabase
        match, loc_type, confidence, suggestions = global_location_db.find_location(location)
        if confidence >= 0.8 and match:
            location = match
        else:
            if suggestions:
                return {
                    'success': False,
                    'location': location,
                    'spelling_suggestions': suggestions,
                    'message': f"Did you mean: {', '.join(suggestions[:3])}?",
                    'needs_clarification': True,
                    'original_query': location
                }

        # Step 2: Get coordinates
        info = global_location_db.get_location_info(location)
        coords = info.get("data", {}).get("coordinates") if info else None

        if not coords:
            coords = await self._get_coordinates(location)
            if not coords:
                return self._get_fallback_weather(location)

        # Step 3: Fetch current weather
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }

            # Use robust API client with retry logic
            response = api_client.make_request(
                method="GET",
                url=url,
                params=params,
                timeout=10,
                custom_error_message="Weather service temporarily unavailable"
            )

            if isinstance(response, dict) and response.get('main'):
                return self._format_weather_data(response, location)
            else:
                self.logger.error(f"Weather API error: {response}")
                return self._get_fallback_weather(location)

        except Exception as e:
            self.logger.error(f"Weather fetch error: {e}")
            return self._get_fallback_weather(location)
    
    async def get_forecast(self, location: str = None, days: int = 3) -> Dict[str, Any]:
        """Get weather forecast for a location using the global location database"""
        if not self.available:
            return self._get_fallback_forecast(location)

        location = location or self.default_location

        # Step 1: Resolve location
        match, loc_type, confidence, suggestions = global_location_db.find_location(location)
        if confidence >= 0.8 and match:
            location = match
        else:
            if suggestions:
                return {
                    'success': False,
                    'location': location,
                    'spelling_suggestions': suggestions,
                    'message': f"Did you mean: {', '.join(suggestions[:3])}?",
                    'needs_clarification': True,
                    'original_query': location
                }

        # Step 2: Get coordinates
        info = global_location_db.get_location_info(location)
        coords = info.get("data", {}).get("coordinates") if info else None

        if not coords:
            coords = await self._get_coordinates(location)
            if not coords:
                return self._get_fallback_forecast(location)

        # Step 3: Fetch forecast data
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }

            # Use robust API client with retry logic
            response = api_client.make_request(
                method="GET",
                url=url,
                params=params,
                timeout=10,
                custom_error_message="Forecast service temporarily unavailable"
            )

            if isinstance(response, dict) and response.get('list'):
                return self._format_forecast_data(response, location)
            else:
                self.logger.error(f"Forecast API error: {response}")
                return self._get_fallback_forecast(location)

        except Exception as e:
            self.logger.error(f"Forecast fetch error: {e}")
            return self._get_fallback_forecast(location)
    
    def learn_location_correction(self, original: str, corrected: str):
        """Learn a new location correction from user feedback"""
        location_checker.learn_correction(original, corrected)
        self.logger.info(f"Learned location correction: {original} -> {corrected}")
    
    async def _get_coordinates(self, location: str) -> Optional[Dict[str, float]]:
        """Get latitude and longitude for a location"""
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': location,
                'limit': 1,
                'appid': self.api_key
            }
            
            # Use robust API client with retry logic
            response = api_client.make_request(
                method="GET",
                url=url,
                params=params,
                timeout=5,
                custom_error_message="Location lookup service temporarily unavailable"
            )
            
            if isinstance(response, list) and len(response) > 0:
                data = response
                return {
                    'lat': data[0]['lat'],
                        'lon': data[0]['lon']
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Geocoding error: {e}")
            return None
    
    def _format_weather_data(self, data: Dict[str, Any], location: str) -> Dict[str, Any]:
        """Format weather API response"""
        try:
            weather = data['weather'][0]
            main = data['main']
            wind = data.get('wind', {})
            
            # Convert temperature
            temp_c = round(main['temp'])
            temp_f = round(temp_c * 9/5 + 32)
            feels_like_c = round(main['feels_like'])
            feels_like_f = round(feels_like_c * 9/5 + 32)
            
            return {
                'success': True,
                'location': location,
                'temperature': {
                    'celsius': temp_c,
                    'fahrenheit': temp_f
                },
                'feels_like': {
                    'celsius': feels_like_c,
                    'fahrenheit': feels_like_f
                },
                'description': weather['description'].title(),
                'humidity': main['humidity'],
                'pressure': main['pressure'],
                'wind_speed': wind.get('speed', 0),
                'wind_direction': wind.get('deg', 0),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Weather data formatting error: {e}")
            return self._get_fallback_weather(location)
    
    def _format_forecast_data(self, data: Dict[str, Any], location: str) -> Dict[str, Any]:
        """Format forecast API response"""
        try:
            forecasts = []
            
            # Group by day (take one forecast per day, around noon)
            current_date = None
            for item in data['list']:
                forecast_date = datetime.fromtimestamp(item['dt']).date()
                forecast_hour = datetime.fromtimestamp(item['dt']).hour
                
                # Take the forecast closest to noon (12:00)
                if current_date != forecast_date and forecast_hour >= 12:
                    current_date = forecast_date
                    
                    weather = item['weather'][0]
                    main = item['main']
                    
                    temp_min = round(main['temp_min'])
                    temp_max = round(main['temp_max'])
                    
                    forecasts.append({
                        'date': forecast_date.strftime('%A'),
                        'temperature_min': temp_min,
                        'temperature_max': temp_max,
                        'description': weather['description'].title(),
                        'summary': f"{forecast_date.strftime('%A')}: {temp_min}°C to {temp_max}°C, {weather['description'].title()}"
                    })
                    
                    if len(forecasts) >= 3:  # Limit to 3 days
                        break
            
            return {
                'success': True,
                'location': location,
                'forecasts': forecasts,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Forecast data formatting error: {e}")
            return self._get_fallback_forecast(location)
    
    def _get_fallback_weather(self, location: str) -> Dict[str, Any]:
        """Fallback response when weather API is unavailable"""
        return {
            'success': False,
            'location': location or self.default_location,
            'fallback': True,
            'message': f"I'd love to get the current weather for {location or 'your area'}, but I need a weather API key to access real-time data. You can get a free API key from OpenWeatherMap and add it to your configuration."
        }
    
    def _get_fallback_forecast(self, location: str) -> Dict[str, Any]:
        """Fallback response when forecast API is unavailable"""
        return {
            'success': False,
            'location': location or self.default_location,
            'fallback': True,
            'message': f"Weather forecast for {location or 'your area'} requires a weather API key. Get a free one from OpenWeatherMap to enable real-time weather updates!"
        }

# Global instance for compatibility
weather_service = WeatherService()
