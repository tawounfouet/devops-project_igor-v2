from django.urls import path
from . import api_views

urlpatterns = [
    path("weather/", api_views.get_weather, name="api_get_weather"),
    path("history/", api_views.get_weather_history, name="api_get_history"),
]
