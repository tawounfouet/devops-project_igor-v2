# Backend (Serveur Django)

## Aperçu

Le backend est le cœur de l'application F_BRAIN. Il s'agit d'un serveur web Django qui fournit une API RESTful pour le frontend, gère la logique métier, communique avec la base de données et orchestre les tâches asynchrones via Celery. Ce service est responsable du traitement des données et de l'implémentation des fonctionnalités principales de l'application.

## Caractéristiques techniques

- **Langage de programmation** : Python 3.11
- **Framework** : Django
- **Gestion des dépendances** : Poetry
- **Image Docker** : Python 3.11 slim
- **Port exposé** : 8000
- **Volumes** : `./server:/app` - Montage du code source pour le développement

## Fichiers importants

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y build-essential gcc libpq-dev \
    && pip install poetry==2.1.3 \
    && pip install gunicorn \
    && pip install django-admin \
    && pip install python-dotenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

# Le COPY est remplacé par un volume dans docker-compose.yml

# Default command - will be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Ce Dockerfile crée un environnement de développement pour le backend Django. Il utilise Python 3.11 comme image de base, installe les dépendances système nécessaires, Poetry pour la gestion des dépendances Python, et configure l'environnement de développement.

### Structure du projet

```
server/
├── Dockerfile
├── manage.py                # Script Django pour la gestion du projet
├── poetry.lock              # Verrouillage des versions des dépendances
├── pyproject.toml           # Configuration du projet et dépendances
├── requirements.txt         # Dépendances Python alternatives à Poetry
├── update-poetry-lock.sh    # Script pour mettre à jour poetry.lock
├── server_config/           # Configuration principale du serveur Django
│   ├── __init__.py
│   ├── asgi.py              # Configuration ASGI pour le déploiement
│   ├── celery.py            # Configuration de Celery
│   ├── settings.py          # Paramètres Django
│   ├── urls.py              # Configuration des URLs principales
│   └── wsgi.py              # Configuration WSGI pour le déploiement
├── static/                  # Fichiers statiques
├── staticfiles/             # Fichiers statiques collectés
└── weather/                 # Application Django exemple
    ├── __init__.py
    ├── admin.py             # Configuration de l'interface d'administration
    ├── api_urls.py          # URLs de l'API
    ├── api_views.py         # Vues de l'API
    ├── apps.py              # Configuration de l'application
    ├── models.py            # Modèles de données
    ├── serializers.py       # Sérialiseurs pour l'API REST
    ├── services.py          # Services métier
    ├── tasks.py             # Tâches Celery
    ├── tests.py             # Tests unitaires
    ├── urls.py              # URLs de l'application web
    ├── views.py             # Vues de l'application web
    ├── management/          # Commandes personnalisées Django
    ├── migrations/          # Migrations de base de données
    └── templates/           # Templates HTML
```

## Configuration dans docker-compose.yml

```yaml
web:
  build:
    context: ./server
    dockerfile: Dockerfile
  env_file: .env
  command: >
    sh -c "
      python manage.py collectstatic --noinput &&
      python manage.py migrate &&
      echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell &&
      python manage.py runserver 0.0.0.0:8000
    "
  networks: [backend]
  expose:
    - "8000"
  ports:
  - "8000:8000"
  volumes:
    - ./server:/app
  environment:
    - USE_POSTGRES=true
    - DJANGO_SETTINGS_MODULE=server_config.settings
    - PYTHONDONTWRITEBYTECODE=1
    - PYTHONUNBUFFERED=1
  depends_on:
    db:
      condition: service_healthy
    rabbitmq:
      condition: service_healthy
```

Cette configuration dans le docker-compose.yml définit le service backend. Elle utilise le Dockerfile situé dans le répertoire `./server`, configure les variables d'environnement, monte le code source en tant que volume pour permettre le développement en temps réel, et spécifie les dépendances sur d'autres services.

## Configuration Django (settings.py)

Le fichier `settings.py` contient la configuration Django, notamment :

- Base de données (PostgreSQL ou SQLite en fonction de la variable d'environnement)
- Configuration de sécurité
- Applications installées
- Intergiciels (middlewares)
- Configuration de Celery
- Gestion des fichiers statiques et média
- Configuration des URLs et internationalisation

## API RESTful

Le backend expose une API RESTful utilisée par le frontend. Cette API est construite à l'aide de Django REST Framework et suit les conventions REST :

- Endpoints organisés par ressources
- Utilisation appropriée des méthodes HTTP (GET, POST, PUT, DELETE)
- Formats de réponse standard (généralement JSON)
- Authentification et autorisation

## Intégration avec Celery

Django est intégré avec Celery pour le traitement des tâches asynchrones et planifiées. La configuration de Celery se trouve dans `server_config/celery.py` et les tâches sont définies dans les fichiers `tasks.py` des applications Django.

## Base de données

Par défaut, le backend est configuré pour utiliser PostgreSQL comme base de données principale, mais il peut également utiliser SQLite en mode développement. La configuration de la base de données est gérée via des variables d'environnement.

## Bonnes pratiques

1. **Architecture en couches** : Séparation claire entre modèles, vues, services et tâches
2. **Tests** : Mise en place de tests unitaires et d'intégration
3. **Documentation de l'API** : Documentation claire des endpoints, paramètres et réponses
4. **Gestion des erreurs** : Traitement uniforme et informatif des erreurs
5. **Migrations** : Gestion propre des migrations de base de données

## Dépannage courant

### Le serveur ne démarre pas
- Vérifier les logs : `docker-compose logs web`
- S'assurer que la base de données est accessible
- Vérifier les variables d'environnement requises

### Erreurs de migration
- Vérifier l'état des migrations : `docker-compose exec web python manage.py showmigrations`
- Résoudre les conflits de migrations si nécessaire

### Problèmes de performances
- Optimiser les requêtes de base de données
- Utiliser des tâches asynchrones pour les opérations longues
- Mettre en cache les résultats fréquemment utilisés

## Ressources additionnelles

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation Django REST Framework](https://www.django-rest-framework.org/)
- [Documentation Celery](https://docs.celeryproject.org/en/stable/)
