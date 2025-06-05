# Services et composants

## Introduction aux services

Le projet F_BRAIN est composé de plusieurs services interconnectés, chacun ayant un rôle spécifique dans l'architecture globale. Cette séparation en services distincts suit le principe de la conception microservices, permettant une meilleure modularité, évolutivité et maintenabilité.

## Liste des services

Voici un aperçu des services principaux qui composent l'application F_BRAIN :

### 1. Frontend (Client)

- **Technologie** : React.js avec Vite comme bundler
- **Conteneur** : Basé sur Node.js Alpine
- **Port** : 4173 (exposé à travers le proxy Nginx)
- **Rôle** : Interface utilisateur de l'application

### 2. Backend (Serveur Django)

- **Technologie** : Django (Python)
- **Conteneur** : Basé sur Python 3.11
- **Port** : 8000
- **Rôle** : Serveur d'API RESTful, logique métier et accès aux données

### 3. Proxy (Nginx)

- **Technologie** : Nginx
- **Conteneur** : Basé sur Nginx Alpine
- **Ports** : 80, 443
- **Rôle** : Routage des requêtes, load balancing, terminaison SSL

### 4. Base de données (PostgreSQL)

- **Technologie** : PostgreSQL
- **Conteneur** : Image PostgreSQL officielle
- **Port** : 5435:5432
- **Rôle** : Stockage persistant des données

### 5. File de messages (RabbitMQ)

- **Technologie** : RabbitMQ
- **Conteneur** : Image RabbitMQ officielle avec plugin de management
- **Port** : 15672 (interface de gestion)
- **Rôle** : Messagerie asynchrone entre services

### 6. Celery Worker

- **Technologie** : Celery (Python)
- **Conteneur** : Même base que le serveur Django
- **Rôle** : Exécution des tâches asynchrones et planifiées

### 7. Prometheus

- **Technologie** : Prometheus
- **Conteneur** : Image Prometheus officielle
- **Port** : 9090
- **Rôle** : Collecte et stockage de métriques

### 8. Grafana

- **Technologie** : Grafana
- **Conteneur** : Image Grafana officielle
- **Port** : 3003:3000
- **Rôle** : Visualisation des métriques et tableaux de bord

## Dépendances entre services

Les services de l'application sont interconnectés et ont des dépendances les uns envers les autres :

1. **Proxy (Nginx)**
   - Dépend de : Frontend, Backend
   - Nécessaire pour : Accès utilisateur

2. **Frontend**
   - Dépend de : Backend (indirectement via le proxy)
   - Nécessaire pour : Interface utilisateur

3. **Backend (Django)**
   - Dépend de : Base de données, RabbitMQ
   - Nécessaire pour : Celery, Frontend

4. **Celery Worker**
   - Dépend de : Backend, RabbitMQ
   - Nécessaire pour : Exécution des tâches asynchrones

5. **Base de données**
   - Dépend de : Aucun
   - Nécessaire pour : Backend, Celery

6. **RabbitMQ**
   - Dépend de : Aucun
   - Nécessaire pour : Backend, Celery

7. **Prometheus**
   - Dépend de : Services à surveiller
   - Nécessaire pour : Grafana

8. **Grafana**
   - Dépend de : Prometheus
   - Nécessaire pour : Visualisation du monitoring

## Santé et résilience des services

Le projet implémente plusieurs mécanismes pour assurer la santé et la résilience des services :

1. **Healthchecks** : Configurés pour PostgreSQL et RabbitMQ pour vérifier périodiquement leur état.
2. **Redémarrage automatique** : Les services critiques sont configurés avec `restart: unless-stopped`.
3. **Dépendances orchestrées** : Les services démarrent dans l'ordre approprié grâce aux directives `depends_on`.

## Pour en savoir plus

Pour des informations détaillées sur chaque service, veuillez consulter les pages dédiées dans la section "Services et composants" :

- [Frontend (Client)](./services/01-frontend.md)
- [Backend (Serveur Django)](./services/02-backend.md)
- [Proxy (Nginx)](./services/03-proxy-nginx.md)
- [Base de données (PostgreSQL)](./services/04-base-donnees.md)
- [File de messages (RabbitMQ)](./services/05-rabbitmq.md)
- [Tâches asynchrones (Celery)](./services/06-celery.md)
- [Surveillance et monitoring](./services/07-monitoring.md)
  - [Prometheus](./services/07a-prometheus.md)
  - [Grafana](./services/07b-grafana.md)
