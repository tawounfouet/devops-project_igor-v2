import os
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WeatherSearch
from .serializers import WeatherSearchSerializer
from .tasks import async_weather_processing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY", "ee56bd2e1c87bf3900aa88cfd2cee8ac"
)


@api_view(["GET"])
def get_weather(request):
    """
    Endpoint pour obtenir les données météo d'une ville
    et les enregistrer dans la base de données
    """
    city = request.query_params.get("city")
    if not city:
        return Response(
            {"error": "Le paramètre 'city' est requis"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Call OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()

        weather_data = response.json()

        # Enregistrement des données dans la base de données
        weather_record = WeatherSearch(
            city=weather_data["name"],
            temperature=weather_data["main"]["temp"],
            humidity=weather_data["main"]["humidity"],
            wind_speed=weather_data["wind"]["speed"],
            pressure=weather_data["main"]["pressure"],
            description=weather_data["weather"][0]["description"],
            icon=weather_data["weather"][0]["icon"],
            country=weather_data["sys"]["country"],
        )
        weather_record.save()

        # Traitement asynchrone des données météo
        async_weather_processing.delay(
            {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "description": weather_data["weather"][0]["description"],
                "country": weather_data["sys"]["country"],
            }
        )

        # Transformer en format sérialisé
        serializer = WeatherSearchSerializer(weather_record)

        return Response({"data": weather_data, "saved_record": serializer.data})

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except KeyError as e:
        return Response(
            {"error": f"Données de l'API incorrectes: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_weather_history(request):
    """
    Endpoint pour récupérer l'historique des recherches météo
    """
    limit = int(request.query_params.get("limit", 10))
    history = WeatherSearch.objects.all()[:limit]

    serializer = WeatherSearchSerializer(history, many=True)
    return Response(serializer.data)
