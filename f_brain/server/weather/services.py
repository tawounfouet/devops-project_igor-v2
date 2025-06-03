import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
#OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', 'ee56bd2e1c87bf3900aa88cfd2cee8ac')
OPENWEATHERMAP_API_KEY = 'ee56bd2e1c87bf3900aa88cfd2cee8ac'



def get_weather_from_api(city):
    """
    Fetch weather data from OpenWeatherMap API
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get('message', 'Unknown error')
        raise Exception(f"OpenWeatherMap API error: {error_message}")

def get_forecast_from_api(city):
    """
    Fetch 5-day forecast data from OpenWeatherMap API
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get('message', 'Unknown error')
        raise Exception(f"OpenWeatherMap API error: {error_message}")