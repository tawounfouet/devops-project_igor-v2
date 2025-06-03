"""
URL configuration for server_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Weather API")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("weather.urls")),
    path("api/v1/", include("weather.api_urls")),  # Nouvelles URLs d'API
    path("", home),
]
