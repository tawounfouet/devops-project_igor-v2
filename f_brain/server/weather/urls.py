from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.get_weather, name='get_weather'),
    path('history/', views.get_history, name='get_history'),
    path('history/<int:search_id>/', views.get_weather_by_id, name='get_weather_by_id'),
    path('dashboard/', views.dashboard, name='dashboard'),
]