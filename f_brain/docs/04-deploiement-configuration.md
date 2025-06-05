# Déploiement et configuration

## Introduction au déploiement

Le déploiement de l'application F_BRAIN est entièrement conteneurisé et orchestré via Docker Compose, ce qui facilite grandement la mise en place et la maintenance de l'environnement. Cette section détaille le processus de déploiement, les configurations nécessaires et les considérations importantes pour différents environnements.

## Prérequis système

Avant de déployer F_BRAIN, assurez-vous que l'environnement cible dispose des éléments suivants :

- **Docker** (v20.10.0 ou supérieur)
- **Docker Compose** (v2.0.0 ou supérieur)
- **Minimum 4 Go de RAM**
- **10 Go d'espace disque** (pour les images Docker et les volumes)
- **Connectivité internet** (pour télécharger les images et les dépendances)

## Structure du déploiement

Le déploiement est structuré autour du fichier `docker-compose.yml` situé à la racine du projet, qui définit l'ensemble des services, réseaux et volumes nécessaires.

```
f_brain/
├── docker-compose.yml    # Définition principale des services
├── .env                  # Variables d'environnement
├── client/              # Code source du frontend
├── server/              # Code source du backend
├── proxy/               # Configuration Nginx
├── grafana.ini          # Configuration Grafana
└── prometheus.yml       # Configuration Prometheus
```

## Configuration via variables d'environnement

L'application est configurée principalement via des variables d'environnement définies dans le fichier `.env` à la racine du projet. Voici les principales variables à configurer :

### Variables de base de données
```
POSTGRES_DB=devops_db
POSTGRES_USER=devops_user
POSTGRES_PASSWORD=devops_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Variables Django
```
DJANGO_SECRET_KEY=un_secret_costaud
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web,frontend
```

### Variables d'API externe
```
OPENWEATHER_API_KEY=your_api_key_here
```

### Variables RabbitMQ et Celery
```
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
```

### Variables Grafana
```
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

## Étapes de déploiement

### 1. Clonage du dépôt

```bash
git clone https://[url-du-depot]/f_brain.git
cd f_brain
```

### 2. Configuration de l'environnement

Créez un fichier `.env` basé sur le modèle fourni :

```bash
cp .env.example .env
# Modifiez le fichier .env avec vos valeurs spécifiques
```

### 3. Construction et démarrage des conteneurs

```bash
docker-compose build
docker-compose up -d
```

### 4. Vérification de l'état des services

```bash
docker-compose ps
```

### 5. Initialisation de la base de données (première exécution)

Cette étape est automatiquement exécutée lors du démarrage du service `web` via la commande définie dans `docker-compose.yml`.

## Environnements de déploiement

### Environnement de développement

L'environnement de développement est configuré pour faciliter le cycle de développement rapide :
- Le mode DEBUG est activé dans Django
- Les volumes sont montés pour permettre le rechargement à chaud du code
- Les ports sont exposés directement pour faciliter le débogage

### Environnement de production

Pour un déploiement en production, plusieurs ajustements sont recommandés :

1. **Variables d'environnement**
```
DJANGO_DEBUG=False
SECRET_KEY=[clé_aléatoire_complexe]
DJANGO_ALLOWED_HOSTS=[liste_des_domaines_autorisés]
```

2. **Sécurité**
- Configurer HTTPS dans Nginx
- Utiliser des mots de passe forts pour la base de données et RabbitMQ
- Limiter l'exposition des ports à l'interface publique

3. **Performances**
- Configurer le nombre de workers Gunicorn pour le serveur Django
- Ajuster les paramètres de mémoire pour PostgreSQL

## Mise à l'échelle

Pour gérer une charge accrue, plusieurs approches de mise à l'échelle sont possibles :

### Mise à l'échelle verticale
- Augmenter les ressources CPU/Mémoire allouées aux conteneurs

### Mise à l'échelle horizontale
- Dupliquer les services frontend et backend
- Configurer le load balancing dans Nginx
- Utiliser un orchestrateur comme Kubernetes pour une mise à l'échelle plus avancée

## Sauvegarde et récupération

### Sauvegarde des données

```bash
# Sauvegarde de la base de données
docker-compose exec db pg_dump -U devops_user -d devops_db > backup_$(date +%Y%m%d).sql

# Sauvegarde des volumes
docker run --rm -v f_brain_pgdata:/source -v $(pwd)/backups:/dest ubuntu tar czvf /dest/pgdata_backup_$(date +%Y%m%d).tar.gz /source
```

### Restauration des données

```bash
# Restauration de la base de données
cat backup_20250101.sql | docker-compose exec -T db psql -U devops_user -d devops_db

# Restauration des volumes
docker run --rm -v $(pwd)/backups:/source -v f_brain_pgdata:/dest ubuntu tar xzvf /source/pgdata_backup_20250101.tar.gz -C /dest
```

## Logs et débogage

### Consulter les logs

```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs web

# Logs en temps réel
docker-compose logs -f web
```

### Connexion à un conteneur

```bash
# Connexion interactive au conteneur backend
docker-compose exec web bash

# Connexion à la base de données
docker-compose exec db psql -U devops_user -d devops_db
```

## Considérations de sécurité

1. **Gestion des secrets**
   - Ne stockez jamais les secrets sensibles dans le dépôt Git
   - Utilisez des solutions comme Docker Secrets ou des gestionnaires de secrets externes pour les environnements critiques

2. **Isolation réseau**
   - L'architecture utilise déjà un réseau bridge isolé
   - En production, limitez davantage l'exposition des ports internes

3. **Mises à jour de sécurité**
   - Maintenez les images Docker à jour avec les correctifs de sécurité
   - Intégrez des scans de sécurité dans votre pipeline CI/CD

## Ressources additionnelles

- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Meilleures pratiques Docker en production](https://docs.docker.com/engine/security/security/)
- [Guide de déploiement Django](https://docs.djangoproject.com/en/stable/howto/deployment/)
