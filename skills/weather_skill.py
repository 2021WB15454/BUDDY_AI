import logging
from utils.weather import get_weather_forecast, extract_location
from utils.weather_service import weather_service
from utils.adaptive_learning import adaptive_learning

class WeatherSkill:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.weather_service = weather_service

    async def handle(self, nlp_result, context):
        # Try to get location from NLP entities first
        location = None
        if isinstance(nlp_result, dict):
            location = nlp_result.get('entities', {}).get('location')
            user_input = nlp_result.get('input', nlp_result.get('text', ''))
        else:
            user_input = str(nlp_result)
        
        if not location:
            location = extract_location(user_input)
        
        # Learn user's location preferences
        if location:
            adaptive_learning.learn_location_preference(location)
        
        if location:
            # Try the enhanced weather service first
            try:
                weather_data = await self.weather_service.get_current_weather(location)
                
                if weather_data.get('success'):
                    # Format response with detailed information
                    temp_c = weather_data['temperature']['celsius']
                    temp_f = weather_data['temperature']['fahrenheit']
                    desc = weather_data['description']
                    humidity = weather_data['humidity']
                    
                    # Learn user's temperature preference (C vs F)
                    temp_pref = adaptive_learning.get_temperature_preference()
                    if temp_pref == "fahrenheit":
                        response = f"Weather in {weather_data['location']}: {desc}, {temp_f}°F ({temp_c}°C), {humidity}% humidity"
                    else:
                        response = f"Weather in {weather_data['location']}: {desc}, {temp_c}°C ({temp_f}°F), {humidity}% humidity"
                    
                    # Learn from this successful interaction
                    adaptive_learning.learn_from_interaction(user_input, "weather", response)
                    return {"success": True, "response": response}
                
                elif weather_data.get('needs_clarification'):
                    # Handle spelling suggestions
                    suggestions = weather_data.get('spelling_suggestions', [])
                    if suggestions:
                        response = f"Did you mean: {', '.join(suggestions[:3])}?"
                        adaptive_learning.learn_from_interaction(user_input, "weather_clarification", response)
                        return {"success": False, "response": response}
                
                # Fallback to original method if enhanced service fails
                forecast = get_weather_forecast(location)
                adaptive_learning.learn_from_interaction(user_input, "weather", forecast)
                return {"success": True, "response": forecast}
                
            except Exception as e:
                self.logger.error(f"Enhanced weather service error: {e}")
                # Fallback to original method
                forecast = get_weather_forecast(location)
                adaptive_learning.learn_from_interaction(user_input, "weather", forecast)
                return {"success": True, "response": forecast}
        else:
            # Suggest user's frequently used locations
            frequent_locations = adaptive_learning.get_frequent_locations()
            if frequent_locations:
                response = f"Please specify a location. You often ask about: {', '.join(frequent_locations[:3])}. Or try 'weather in London'."
            else:
                response = "Please specify a location to get the weather forecast. For example: 'weather in London'."
            
            adaptive_learning.learn_from_interaction(user_input, "weather_no_location", response)
            return {"success": False, "response": response}
