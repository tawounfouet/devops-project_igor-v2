from django.contrib import admin
from .models import WeatherSearch

# Celery task result imports - just for customization, not re-registration
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask


@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "temperature", "description", "searched_at")
    list_filter = ("city", "country", "searched_at")
    search_fields = ("city", "country", "description")
    readonly_fields = ("searched_at",)
    fieldsets = (
        ("Location", {"fields": ("city", "country")}),
        (
            "Weather Data",
            {
                "fields": (
                    "temperature",
                    "humidity",
                    "wind_speed",
                    "pressure",
                    "description",
                    "icon",
                )
            },
        ),
        ("Metadata", {"fields": ("searched_at",)}),
    )


# Note: TaskResult and PeriodicTask are already registered by django_celery_results and django_celery_beat
# Their admin interfaces are automatically available in the Django admin panel
