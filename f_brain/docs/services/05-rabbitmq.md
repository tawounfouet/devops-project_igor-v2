# File de messages (RabbitMQ)

## Aperçu

RabbitMQ est le système de messagerie utilisé dans l'application F_BRAIN pour la communication asynchrone entre services. Il joue un rôle crucial en tant qu'intermédiaire entre le serveur Django et les workers Celery, permettant le traitement des tâches en arrière-plan, les notifications et la communication inter-services. RabbitMQ implémente le protocole AMQP (Advanced Message Queuing Protocol) et offre des fonctionnalités avancées de routage, persistance et distribution des messages.

## Caractéristiques techniques

- **Technologie** : RabbitMQ
- **Image Docker** : RabbitMQ avec plugin de management (rabbitmq:4-management)
- **Port exposé** : 15672 (interface de gestion web)
- **Healthcheck** : Vérification périodique du statut avec `rabbitmqctl status`
- **Crédentiels par défaut** : guest/guest

## Configuration dans docker-compose.yml

```yaml
rabbitmq:
  image: rabbitmq:4-management
  ports:
    - "15672:15672"
  env_file: .env
  networks: [backend]
  environment:
    RABBITMQ_DEFAULT_USER: guest
    RABBITMQ_DEFAULT_PASS: guest
  healthcheck:
    test: ["CMD", "rabbitmqctl", "status"]
    interval: 10s
    timeout: 5s
    retries: 5
```

Cette configuration dans docker-compose.yml définit le service RabbitMQ. Elle utilise l'image officielle RabbitMQ avec le plugin de management, expose le port de l'interface de gestion, configure les variables d'environnement, et définit un healthcheck pour s'assurer que RabbitMQ est disponible avant que les services dépendants ne démarrent.

## Variables d'environnement

Les variables d'environnement suivantes sont définies dans le fichier `.env` :

```
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
```

Ces variables configurent les crédentiels RabbitMQ et les URLs nécessaires pour la connexion depuis Celery et Django.

## Rôle dans l'architecture

RabbitMQ joue plusieurs rôles dans l'architecture de F_BRAIN :

1. **Broker Celery** - Il sert de broker pour les tâches Celery, stockant les messages de tâches jusqu'à ce qu'un worker puisse les traiter.
2. **Communication asynchrone** - Il permet la communication asynchrone entre les différents services.
3. **Découplage des services** - Il aide à découpler les producteurs et les consommateurs de messages.
4. **Persistance des messages** - Il assure que les messages ne sont pas perdus même en cas de redémarrage.
5. **Distribution des charges** - Il contribue à répartir la charge de travail entre plusieurs workers.

## Interface de gestion

RabbitMQ fournit une interface de gestion web accessible à l'adresse `http://localhost:15672` (ou l'adresse IP du serveur hôte). Cette interface permet de :

1. **Surveiller les files d'attente** - Voir l'état des queues, le nombre de messages en attente, etc.
2. **Gérer les échanges** - Créer, modifier et supprimer des échanges.
3. **Administrer les utilisateurs** - Créer et gérer des utilisateurs avec différents niveaux d'accès.
4. **Visualiser les connexions** - Voir quels clients sont connectés et leur consommation.
5. **Inspecter les messages** - Examiner et même publier des messages manuellement.

## Intégration avec Celery

L'intégration entre RabbitMQ et Celery est configurée dans `server_config/celery.py` :

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server_config.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Et dans les paramètres Django (`settings.py`) :

```python
# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
```

## Concepts importants de RabbitMQ

1. **Queue** - Structure de données qui stocke les messages jusqu'à ce qu'ils soient consommés.
2. **Exchange** - Point où les messages sont publiés avant d'être routés vers les queues.
3. **Binding** - Lien entre un exchange et une queue qui définit comment les messages sont routés.
4. **Virtual Host (vhost)** - Partition logique qui isole les applications dans RabbitMQ.
5. **Message** - Unité d'information envoyée entre les producteurs et les consommateurs.

## Types d'exchanges dans RabbitMQ

1. **Direct Exchange** - Route les messages vers les queues basées sur une clé de routage exacte.
2. **Fanout Exchange** - Diffuse tous les messages reçus à toutes les queues liées.
3. **Topic Exchange** - Route les messages vers les queues basées sur des modèles de clés de routage.
4. **Headers Exchange** - Route les messages basés sur les en-têtes plutôt que sur les clés de routage.

## Bonnes pratiques

1. **Sécurité** - Changer les crédentiels par défaut et utiliser des vhosts pour isoler les applications.
2. **Monitoring** - Surveiller les métriques clés comme la longueur des queues et la consommation mémoire.
3. **Persistance** - Configurer la durabilité des messages pour éviter les pertes de données.
4. **Limite de messages** - Définir des limites pour éviter que les queues ne consomment trop de mémoire.
5. **Clustering** - Pour les environnements de production, envisager le clustering pour la haute disponibilité.

## Dépannage courant

### RabbitMQ ne démarre pas
- Vérifier les logs : `docker-compose logs rabbitmq`
- S'assurer qu'il y a assez de mémoire disponible
- Vérifier les permissions sur les répertoires de données

### Les messages ne sont pas consommés
- Vérifier que les workers Celery sont en cours d'exécution
- Examiner les logs des workers pour des erreurs
- Vérifier que les queues sont correctement configurées dans l'interface de gestion

### Problèmes de connexion depuis Celery
- Vérifier que l'URL du broker est correcte
- S'assurer que RabbitMQ est accessible sur le réseau backend
- Contrôler les logs pour des erreurs d'authentification

## Ressources additionnelles

- [Documentation RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Guide RabbitMQ avec Docker](https://hub.docker.com/_/rabbitmq/)
- [Documentation Celery sur RabbitMQ](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html)
