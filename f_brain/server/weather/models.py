from django.db import models

class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.IntegerField(default=0)
    wind_speed = models.FloatField(default=0)
    pressure = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"
    
    class Meta:
        ordering = ['-searched_at']