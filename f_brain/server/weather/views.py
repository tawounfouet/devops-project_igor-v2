from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
import os
from dotenv import load_dotenv
from .models import WeatherSearch

# Load environment variables
load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', 'ee56bd2e1c87bf3900aa88cfd2cee8ac')

@csrf_exempt
def get_weather(request):
    if request.method == "GET":
        city = request.GET.get('city')
        if not city:
            return JsonResponse({"error": "City parameter is required"}, status=400)
        
        # Call OpenWeatherMap API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
            
            # Save search to database
            search = WeatherSearch.objects.create(
                city=weather_data["city"],
                country=weather_data["country"],
                temperature=weather_data["temperature"],
                humidity=weather_data["humidity"],
                wind_speed=weather_data["wind_speed"],
                pressure=weather_data["pressure"],
                description=weather_data["description"],
                icon=weather_data["icon"]
            )
            
            weather_data["id"] = search.id
            return JsonResponse(weather_data)
        else:
            return JsonResponse({"error": f"Could not retrieve weather data: {response.json()['message']}"}, status=response.status_code)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def get_history(request):
    if request.method == "GET":
        limit = int(request.GET.get('limit', 10))
        history = WeatherSearch.objects.all()[:limit]
        
        results = [
            {
                "id": entry.id,
                "city": entry.city,
                "country": entry.country,
                "temperature": entry.temperature,
                "humidity": entry.humidity,
                "description": entry.description,
                "icon": entry.icon,
                "searched_at": entry.searched_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for entry in history
        ]
        return JsonResponse(results, safe=False)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def get_weather_by_id(request, search_id):
    try:
        search = WeatherSearch.objects.get(pk=search_id)
        weather_data = {
            "id": search.id,
            "city": search.city,
            "country": search.country,
            "temperature": search.temperature,
            "humidity": search.humidity,
            "wind_speed": search.wind_speed,
            "pressure": search.pressure,
            "description": search.description,
            "icon": search.icon,
            "searched_at": search.searched_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(weather_data)
    except WeatherSearch.DoesNotExist:
        return JsonResponse({"error": "Weather search not found"}, status=404)

def dashboard(request):
    return render(request, 'weather/dashboard.html')