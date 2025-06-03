# filepath: /Users/awf/Projects/drafts/03Devops-2025/f_brain/server/weather/tasks.py
from celery import shared_task
import time
import logging
from django.utils import timezone
from django.db.models import Q, Count, Avg, Max, Min
from .models import WeatherSearch

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def test_celery_task(self, message="Hello from Celery!"):
    """
    Tâche de test simple pour vérifier que Celery fonctionne
    """
    try:
        logger.info(f"Tâche Celery démarrée: {message}")

        # Simulation d'un travail
        time.sleep(2)

        result = {
            "message": message,
            "task_id": self.request.id,
            "timestamp": timezone.now().isoformat(),
            "status": "completed",
        }

        logger.info(f"Tâche Celery terminée: {result}")
        return result

    except Exception as e:
        logger.error(f"Erreur dans la tâche Celery: {e}")
        raise


@shared_task(bind=True)
def async_weather_processing(self, search_data):
    """
    Tâche pour traiter les recherches météo de manière asynchrone
    """
    try:
        logger.info(f"Traitement asynchrone des données météo: {search_data}")

        # Ici on pourrait ajouter du traitement lourd comme:
        # - Analyse des tendances météo
        # - Notifications
        # - Mise en cache avancée
        # - Intégration avec d'autres APIs

        # Simulation d'un traitement
        time.sleep(1)

        # Exemple: mettre à jour les statistiques
        city = search_data.get("city", "")
        if city:
            # Compter les recherches pour cette ville
            search_count = WeatherSearch.objects.filter(city__icontains=city).count()

            result = {
                "city": city,
                "search_count": search_count,
                "processed_at": timezone.now().isoformat(),
                "task_id": self.request.id,
            }

            logger.info(f"Traitement météo terminé: {result}")
            return result

    except Exception as e:
        logger.error(f"Erreur dans le traitement météo asynchrone: {e}")
        raise


@shared_task
def cleanup_old_searches():
    """
    Tâche de nettoyage des anciennes recherches météo
    """
    try:
        # Supprimer les recherches de plus de 30 jours
        from datetime import timedelta

        cutoff_date = timezone.now() - timedelta(days=30)

        deleted_count, _ = WeatherSearch.objects.filter(
            searched_at__lt=cutoff_date
        ).delete()

        logger.info(f"Nettoyage terminé: {deleted_count} recherches supprimées")
        return {"deleted_count": deleted_count, "cutoff_date": cutoff_date.isoformat()}

    except Exception as e:
        logger.error(f"Erreur lors du nettoyage: {e}")
        raise


# ================================
# NOUVELLES TÂCHES CELERY AVANCÉES
# ================================


@shared_task
def generate_weather_statistics():
    """
    Génère des statistiques sur les recherches météo
    """
    try:
        from django.db.models import Count, Avg, Max, Min
        from collections import Counter

        # Statistiques générales
        total_searches = WeatherSearch.objects.count()

        # Top 10 des villes les plus recherchées
        top_cities = (
            WeatherSearch.objects.values("city", "country")
            .annotate(search_count=Count("id"))
            .order_by("-search_count")[:10]
        )

        # Statistiques de température
        temp_stats = WeatherSearch.objects.aggregate(
            avg_temp=Avg("temperature"),
            max_temp=Max("temperature"),
            min_temp=Min("temperature"),
        )

        # Recherches par jour des 7 derniers jours
        from datetime import timedelta

        last_week = timezone.now() - timedelta(days=7)
        daily_searches = (
            WeatherSearch.objects.filter(searched_at__gte=last_week)
            .extra(select={"day": "date(searched_at)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        result = {
            "total_searches": total_searches,
            "top_cities": list(top_cities),
            "temperature_stats": temp_stats,
            "daily_searches_last_week": list(daily_searches),
            "generated_at": timezone.now().isoformat(),
        }

        logger.info(
            f"Statistiques météo générées: {total_searches} recherches analysées"
        )
        return result

    except Exception as e:
        logger.error(f"Erreur lors de la génération des statistiques: {e}")
        raise


@shared_task(bind=True)
def bulk_weather_update(self, cities_list):
    """
    Mise à jour en masse des données météo pour une liste de villes
    """
    try:
        import requests
        import os

        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            logger.warning("API key OpenWeather manquante")
            return {"error": "API key manquante"}

        updated_cities = []
        errors = []

        for i, city_data in enumerate(cities_list):
            try:
                city = city_data.get("city", "")
                country = city_data.get("country", "")

                # Appel API OpenWeather
                url = "http://api.openweathermap.org/data/2.5/weather"
                params = {"q": f"{city},{country}", "appid": api_key, "units": "metric"}

                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    # Créer ou mettre à jour la recherche
                    weather_search = WeatherSearch.objects.create(
                        city=data["name"],
                        country=data["sys"]["country"],
                        temperature=data["main"]["temp"],
                        humidity=data["main"]["humidity"],
                        wind_speed=data.get("wind", {}).get("speed", 0),
                        pressure=data["main"]["pressure"],
                        description=data["weather"][0]["description"],
                        icon=data["weather"][0]["icon"],
                    )

                    updated_cities.append(
                        {
                            "city": weather_search.city,
                            "temperature": weather_search.temperature,
                            "id": weather_search.id,
                        }
                    )

                    # Mettre à jour le progrès de la tâche
                    self.update_state(
                        state="PROGRESS",
                        meta={"current": i + 1, "total": len(cities_list)},
                    )

                else:
                    errors.append(f"{city}: HTTP {response.status_code}")

                # Pause entre les appels API
                time.sleep(0.5)

            except Exception as e:
                errors.append(f"{city}: {str(e)}")

        result = {
            "updated_cities": updated_cities,
            "errors": errors,
            "total_processed": len(cities_list),
            "successful": len(updated_cities),
            "failed": len(errors),
            "processed_at": timezone.now().isoformat(),
        }

        logger.info(
            f"Mise à jour en masse terminée: {len(updated_cities)} succès, {len(errors)} erreurs"
        )
        return result

    except Exception as e:
        logger.error(f"Erreur dans la mise à jour en masse: {e}")
        raise


@shared_task
def send_weather_alerts():
    """
    Envoie des alertes pour les conditions météo extrêmes
    """
    try:
        # Rechercher les conditions extrêmes des dernières 24h
        from datetime import timedelta

        last_24h = timezone.now() - timedelta(hours=24)

        extreme_conditions = (
            WeatherSearch.objects.filter(searched_at__gte=last_24h)
            .filter(
                # Conditions extrêmes
                Q(temperature__gte=40)  # Très chaud
                | Q(temperature__lte=-10)  # Très froid
                | Q(wind_speed__gte=15)  # Vent fort
                | Q(humidity__gte=90)  # Humidité très élevée
            )
            .distinct()
        )

        alerts = []
        for condition in extreme_conditions:
            alert_type = []
            if condition.temperature >= 40:
                alert_type.append("Chaleur extrême")
            if condition.temperature <= -10:
                alert_type.append("Froid extrême")
            if condition.wind_speed >= 15:
                alert_type.append("Vent fort")
            if condition.humidity >= 90:
                alert_type.append("Humidité élevée")

            alerts.append(
                {
                    "city": condition.city,
                    "country": condition.country,
                    "temperature": condition.temperature,
                    "wind_speed": condition.wind_speed,
                    "humidity": condition.humidity,
                    "alert_types": alert_type,
                    "searched_at": condition.searched_at.isoformat(),
                }
            )

        # Ici, on pourrait envoyer des emails, des notifications push, etc.
        if alerts:
            logger.warning(
                f"Alertes météo générées: {len(alerts)} conditions extrêmes détectées"
            )

        return {
            "alerts_count": len(alerts),
            "alerts": alerts,
            "checked_at": timezone.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Erreur lors de la vérification des alertes: {e}")
        raise


@shared_task
def database_maintenance():
    """
    Maintenance de la base de données (optimisation, nettoyage, indexation)
    """
    try:
        from django.db import connection

        maintenance_results = []

        # 1. Analyser les tables (PostgreSQL)
        with connection.cursor() as cursor:
            cursor.execute("ANALYZE weather_weathersearch;")
            maintenance_results.append("Table weather_weathersearch analysée")

        # 2. Nettoyer les recherches dupliquées (même ville, même heure)
        duplicates = []
        searches = (
            WeatherSearch.objects.values("city", "searched_at__date")
            .annotate(count=Count("id"))
            .filter(count__gt=5)
        )  # Plus de 5 recherches le même jour pour la même ville

        for search_group in searches:
            city = search_group["city"]
            date = search_group["searched_at__date"]

            # Garder seulement les 3 plus récentes
            old_searches = WeatherSearch.objects.filter(
                city=city, searched_at__date=date
            ).order_by("-searched_at")[3:]

            deleted_count = len(old_searches)
            for search in old_searches:
                search.delete()

            if deleted_count > 0:
                duplicates.append(
                    f"{city} ({date}): {deleted_count} recherches supprimées"
                )

        # 3. Vérifier la cohérence des données
        inconsistent_data = WeatherSearch.objects.filter(
            Q(temperature__lt=-50)  # Température irréaliste
            | Q(temperature__gt=60)
            | Q(humidity__lt=0)
            | Q(humidity__gt=100)
            | Q(pressure__lt=800)
            | Q(pressure__gt=1100)
        )

        cleaned_count = inconsistent_data.count()
        if cleaned_count > 0:
            inconsistent_data.delete()
            maintenance_results.append(
                f"{cleaned_count} entrées avec données incohérentes supprimées"
            )

        result = {
            "maintenance_actions": maintenance_results,
            "duplicates_cleaned": duplicates,
            "inconsistent_data_cleaned": cleaned_count,
            "maintenance_date": timezone.now().isoformat(),
        }

        logger.info(
            f"Maintenance base de données terminée: {len(maintenance_results)} actions"
        )
        return result

    except Exception as e:
        logger.error(f"Erreur lors de la maintenance: {e}")
        raise


@shared_task
def export_weather_data(export_format="json"):
    """
    Exporte les données météo dans différents formats
    """
    try:
        from django.core import serializers
        import json
        import csv
        import io

        # Récupérer toutes les données
        weather_data = WeatherSearch.objects.all().order_by("-searched_at")

        if export_format.lower() == "json":
            serialized_data = serializers.serialize("json", weather_data)
            data = json.loads(serialized_data)

        elif export_format.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)

            # En-têtes
            writer.writerow(
                [
                    "City",
                    "Country",
                    "Temperature",
                    "Humidity",
                    "Wind Speed",
                    "Pressure",
                    "Description",
                    "Icon",
                    "Searched At",
                ]
            )

            # Données
            for search in weather_data:
                writer.writerow(
                    [
                        search.city,
                        search.country,
                        search.temperature,
                        search.humidity,
                        search.wind_speed,
                        search.pressure,
                        search.description,
                        search.icon,
                        search.searched_at.isoformat(),
                    ]
                )

            data = output.getvalue()
            output.close()

        else:
            raise ValueError(f"Format d'export non supporté: {export_format}")

        # Sauvegarder le fichier (ici on retourne juste les données)
        result = {
            "format": export_format,
            "records_count": weather_data.count(),
            "exported_at": timezone.now().isoformat(),
            "data_preview": (
                str(data)[:500] + "..." if len(str(data)) > 500 else str(data)
            ),
        }

        logger.info(
            f"Export terminé: {weather_data.count()} enregistrements en format {export_format}"
        )
        return result

    except Exception as e:
        logger.error(f"Erreur lors de l'export: {e}")
        raise
