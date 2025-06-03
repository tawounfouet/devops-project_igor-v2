

## 🔍 Vue d’ensemble du projet Devops
Il s'agit d'un projet DevOps de type microservices avec Docker, Prometheus, Grafana, RabbitMQ, PostgreSQL, etc. Il semble être organisé autour d'une architecture avec plusieurs conteneurs Docker :

## 📦 Architecture des conteneurs (vue en haut du tableau)
- C:client → contient un Dockerfile
- C:server → contient un Dockerfile
- C:monitoring → contient prometheus.yml
- C:proxy → contient une config Nginx nginx.conf
- Le tout est orchestré avec un fichier docker-compose.yml.

## 🔌 Ports exposés
- 8000 → API (backend Django)
- 5134 → client
- 3000 → metrics (Grafana)
- 9090 (implicite) → Prometheus
- 80 → proxy (Nginx)

## 📚 Technologies utilisées
- Backend : Django + Celery
- Queue : RabbitMQ
- Base de données : PostgreSQL
- Frontend : probablement JS/React (non mentionné mais sous-entendu)
- Monitoring : Prometheus + Grafana
- Reverse Proxy : Nginx
- Gestion des dépendances : poetry (Python)


## 📈 Vue conceptuelle (diagramme)
- Frontend parle à Backend
- Backend utilise Celery pour lancer des tâches async
- Celery met les tâches dans RabbitMQ
- RabbitMQ communique avec Backend (workers)
- Prometheus scrape les métriques de Celery/Backend
- Grafana affiche ces métriques


## 🎯 Objectifs et TODO list
- ⚠ Commit/push chaque avancement sur Git (code + Dockerfiles)
- ⚠ Chaque container doit être accessible depuis un navigateur web
- ⚠ Tous les services doivent fonctionner ensemble (interopérabilité)
- ✅ Si possible, publier les images Docker sur GitHub Container Registry (ou Docker Hub)

## ✅ Ce qui est déjà défini
- Structure des services (client, server, monitoring, proxy)
- Technologies à utiliser
- Port mapping

## Vue d’architecture générale

Besoin de metrics via Prometheus et visualisation avec Grafana

## ❗ Ce qu’il reste à faire

### Docker et orchestration
- Écrire les Dockerfiles pour chaque service (client, server, monitoring, proxy)
- Créer le fichier docker-compose.yml avec les bons volumes, réseaux, services, ports
- Ajouter une configuration nginx.conf pour faire le reverse proxy vers les services internes

### Backend & tâches
- Implémenter l’API Django
- Connecter Celery avec RabbitMQ
- Ajouter des métriques exportables (via prometheus_client)
- Associer PostgreSQL comme base de données backend

### Monitoring
- Écrire un fichier prometheus.yml pour configurer le scrape des services
- Configurer Grafana (datasource Prometheus, dashboards pour Celery, backend, etc.)

### Documentation & Git
- Rédiger une documentation claire (README.md)
- Ajouter des instructions de build et de déploiement
- Automatiser le push des images Docker
- Organiser les dossiers par service : client/, server/, monitoring/, proxy/, etc.