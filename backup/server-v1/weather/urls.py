from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save_weather, name='save_weather'),
    path('history/', views.get_history, name='get_history'),
]
