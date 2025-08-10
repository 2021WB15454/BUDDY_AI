import logging
from utils.weather_service import weather_service
from utils.adaptive_learning import adaptive_learning

class ForecastSkill:
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
            from utils.weather import extract_location
            location = extract_location(user_input)
        
        # Learn user's location preferences for forecasts
        if location:
            adaptive_learning.learn_location_preference(location)
        
        if location:
            try:
                # Learn user's preferred forecast length
                days = adaptive_learning.get_preferred_forecast_days(user_input)
                forecast_data = await self.weather_service.get_forecast(location, days=days)
                
                if forecast_data.get('success'):
                    forecasts = forecast_data.get('forecasts', [])
                    if forecasts:
                        # Format based on user's temperature preference
                        temp_pref = adaptive_learning.get_temperature_preference()
                        
                        response_parts = [f"{days}-day forecast for {forecast_data['location']}:"]
                        for forecast in forecasts:
                            if temp_pref == "fahrenheit":
                                temp_min_f = round(forecast['temperature_min'] * 9/5 + 32)
                                temp_max_f = round(forecast['temperature_max'] * 9/5 + 32)
                                summary = f"{forecast['date']}: {temp_min_f}°F to {temp_max_f}°F, {forecast['description']}"
                            else:
                                summary = forecast['summary']
                            response_parts.append(summary)
                        
                        response = "\n".join(response_parts)
                        adaptive_learning.learn_from_interaction(user_input, "forecast", response)
                        return {"success": True, "response": response}
                
                elif forecast_data.get('needs_clarification'):
                    suggestions = forecast_data.get('spelling_suggestions', [])
                    if suggestions:
                        response = f"Did you mean: {', '.join(suggestions[:3])}?"
                        adaptive_learning.learn_from_interaction(user_input, "forecast_clarification", response)
                        return {"success": False, "response": response}
                
                # Fallback to current weather if forecast fails
                weather_data = await self.weather_service.get_current_weather(location)
                if weather_data.get('success'):
                    temp_c = weather_data['temperature']['celsius']
                    temp_f = weather_data['temperature']['fahrenheit']
                    desc = weather_data['description']
                    humidity = weather_data['humidity']
                    
                    temp_pref = adaptive_learning.get_temperature_preference()
                    if temp_pref == "fahrenheit":
                        response = f"Forecast unavailable, but current weather in {weather_data['location']}: {desc}, {temp_f}°F, {humidity}% humidity"
                    else:
                        response = f"Forecast unavailable, but current weather in {weather_data['location']}: {desc}, {temp_c}°C, {humidity}% humidity"
                    
                    adaptive_learning.learn_from_interaction(user_input, "forecast_fallback", response)
                    return {"success": True, "response": response}
                
            except Exception as e:
                self.logger.error(f"Forecast service error: {e}")
                response = "Sorry, I couldn't get the forecast right now. Please try again later."
                adaptive_learning.learn_from_interaction(user_input, "forecast_error", response)
                return {"success": False, "response": response}
        
        # Suggest user's frequently used locations
        frequent_locations = adaptive_learning.get_frequent_locations()
        if frequent_locations:
            response = f"Please specify a location for the forecast. You often ask about: {', '.join(frequent_locations[:3])}. Or try 'forecast for London'."
        else:
            response = "Please specify a location for the forecast. For example: 'forecast for London'."
        
        adaptive_learning.learn_from_interaction(user_input, "forecast_no_location", response)
        return {"success": False, "response": response}
