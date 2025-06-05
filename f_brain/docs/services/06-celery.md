# Tâches asynchrones (Celery)

## Aperçu

Celery est un système de files d'attente distribué utilisé dans l'application F_BRAIN pour exécuter des tâches asynchrones et planifiées. Il permet d'améliorer les performances et la réactivité de l'application en déchargeant les opérations longues ou intensives en ressources du thread principal du serveur web. Dans l'architecture de F_BRAIN, Celery fonctionne en tandem avec RabbitMQ qui sert de broker de messages.

## Caractéristiques techniques

- **Langage de programmation** : Python 3.11
- **Framework** : Celery
- **Broker** : RabbitMQ
- **Backend de résultats** : Django DB (stockage des résultats dans la base de données Django)
- **Image Docker** : Même base que le serveur Django
- **Volumes** : `./server:/app` - Montage du code source pour le développement

## Configuration dans docker-compose.yml

```yaml
celery:
  build:
    context: ./server
    dockerfile: Dockerfile
  env_file: .env
  command: celery -A server_config worker --loglevel=info
  environment:
    USE_POSTGRES: "true"
    POSTGRES_DB: ${POSTGRES_DB:-devops_db}
    POSTGRES_USER: ${POSTGRES_USER:-devops_user}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-devops_pass}
    POSTGRES_HOST: db
    POSTGRES_PORT: 5432
    RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    PYTHONDONTWRITEBYTECODE: 1
    PYTHONUNBUFFERED: 1
  volumes:
    - ./server:/app
  networks: [backend]
  depends_on: [web, rabbitmq]
```

Cette configuration dans docker-compose.yml définit le service Celery. Elle utilise le même Dockerfile que le serveur Django, configure les variables d'environnement, exécute la commande Celery worker, et spécifie les dépendances sur les services web et RabbitMQ.

## Configuration Celery

La configuration principale de Celery se trouve dans `server_config/celery.py` :

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_config.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Ce code initialise l'application Celery, configure les paramètres à partir de Django, et découvre automatiquement les tâches définies dans les applications Django.

Dans `settings.py`, des paramètres supplémentaires pour Celery sont définis :

```python
# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
```

## Types de tâches

Dans l'application F_BRAIN, Celery est utilisé pour plusieurs types de tâches :

### 1. Tâches asynchrones à la demande

Ces tâches sont déclenchées par une action utilisateur ou un événement système, mais exécutées en arrière-plan pour ne pas bloquer la réponse HTTP. Exemple de définition :

```python
# Dans weather/tasks.py
@app.task
def fetch_weather_data(city_id):
    # Code pour récupérer les données météo
    # potentiellement longue opération
    pass
```

### 2. Tâches périodiques (planifiées)

Ces tâches sont exécutées à intervalles réguliers selon une planification définie :

```python
# Dans settings.py
CELERY_BEAT_SCHEDULE = {
    "update_weather_data": {
        "task": "weather.tasks.update_all_weather_data",
        "schedule": crontab(minute="0", hour="*/3"),  # Toutes les 3 heures
    },
    "cleanup_old_data": {
        "task": "weather.tasks.cleanup_old_weather_data",
        "schedule": crontab(minute="0", hour="1"),  # Tous les jours à 1h du matin
    },
}
```

### 3. Tâches chaînées

Celery permet de chaîner des tâches pour créer des workflows complexes :

```python
from celery import chain

# Exemple d'utilisation dans une vue
def process_data_view(request):
    chain(
        extract_data.s(),
        transform_data.s(),
        load_data.s()
    ).delay()
    return HttpResponse("Processing started")
```

## Définition et utilisation des tâches

Les tâches Celery sont typiquement définies dans des fichiers `tasks.py` au sein des applications Django :

```python
# Dans weather/tasks.py
from server_config.celery import app
from .models import City, WeatherData
from .services import WeatherService

@app.task(bind=True, max_retries=3)
def fetch_weather_for_city(self, city_id):
    try:
        city = City.objects.get(id=city_id)
        service = WeatherService()
        data = service.get_weather(city.name)
        
        # Sauvegarder les données
        WeatherData.objects.create(
            city=city,
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"]
        )
        
    except Exception as exc:
        # Retry task in case of error
        self.retry(exc=exc, countdown=60)  # retry after 1 minute
```

Pour appeler cette tâche de manière asynchrone depuis une vue Django :

```python
# Dans weather/views.py
from .tasks import fetch_weather_for_city

def update_weather_view(request, city_id):
    # Lancer la tâche en arrière-plan
    fetch_weather_for_city.delay(city_id)
    return HttpResponse("Update scheduled")
```

## Surveillance et monitoring

Pour surveiller l'exécution des tâches Celery, plusieurs approches sont possibles :

### 1. Logs Celery

Les logs Celery peuvent être consultés avec :

```bash
docker-compose logs celery
```

### 2. Interface Flower (non installée par défaut)

[Flower](https://flower.readthedocs.io/) est une interface web pour Celery qui peut être ajoutée au projet pour une surveillance plus conviviale.

### 3. Inspection programmatique

Celery fournit des API pour inspecter l'état des tâches :

```python
from celery.result import AsyncResult

# Vérifier l'état d'une tâche
task_result = AsyncResult(task_id)
status = task_result.status  # 'PENDING', 'SUCCESS', 'FAILURE', etc.
```

## Bonnes pratiques

1. **Idempotence** - Concevoir les tâches pour qu'elles puissent être exécutées plusieurs fois sans effets secondaires indésirables.
2. **Gestion des erreurs** - Implémenter une logique de retry appropriée et gérer les exceptions.
3. **Tâches atomiques** - Garder les tâches simples et centrées sur une seule responsabilité.
4. **Surveillance** - Mettre en place un monitoring des queues et des workers.
5. **Optimisation des ressources** - Ajuster le nombre de workers selon les besoins et la charge.

## Dépannage courant

### Les tâches ne sont pas exécutées
- Vérifier que le worker Celery est en cours d'exécution : `docker-compose ps`
- Examiner les logs : `docker-compose logs celery`
- S'assurer que RabbitMQ est accessible et fonctionne correctement

### Tâches bloquées ou lentes
- Vérifier si des tâches consomment trop de ressources
- Considérer l'augmentation des ressources allouées au conteneur
- Envisager de diviser les grandes tâches en tâches plus petites

### Tâches périodiques non déclenchées
- Vérifier que Celery Beat est en cours d'exécution (si utilisé)
- S'assurer que la configuration `CELERY_BEAT_SCHEDULE` est correcte
- Vérifier le fuseau horaire configuré dans Celery

## Ressources additionnelles

- [Documentation Celery](https://docs.celeryproject.org/)
- [Documentation Django Celery](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
- [Flower - Monitoring Celery](https://flower.readthedocs.io/)
- [Guide des bonnes pratiques Celery](https://denibertovic.com/posts/celery-best-practices/)
