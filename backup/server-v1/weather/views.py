from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WeatherSearch
from datetime import datetime

@csrf_exempt
def save_weather(request):
    if request.method == "POST":
        data = json.loads(request.body)
        weather = WeatherSearch.objects.create(
            city=data["city"],
            temperature=data["temperature"],
            description=data["description"]
        )
        return JsonResponse({"status": "saved", "id": weather.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_history(request):
    if request.method == "GET":
        history = WeatherSearch.objects.order_by("-searched_at")[:10]
        results = [
            {
                "city": entry.city,
                "temperature": entry.temperature,
                "description": entry.description,
                "date": entry.searched_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for entry in history
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)
