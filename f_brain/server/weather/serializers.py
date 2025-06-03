from rest_framework import serializers
from .models import WeatherSearch


class WeatherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSearch
        fields = [
            "id",
            "city",
            "temperature",
            "humidity",
            "wind_speed",
            "pressure",
            "description",
            "icon",
            "country",
            "searched_at",
        ]
