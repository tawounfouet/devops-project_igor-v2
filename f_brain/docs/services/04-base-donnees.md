# Base de données (PostgreSQL)

## Aperçu

La base de données PostgreSQL est le système de stockage persistant pour l'application F_BRAIN. Elle stocke toutes les données structurées de l'application, y compris les informations utilisateur, les données métier et les paramètres système. PostgreSQL a été choisi pour sa fiabilité, ses performances et ses fonctionnalités avancées par rapport à d'autres systèmes de gestion de bases de données relationnelles.

## Caractéristiques techniques

- **Technologie** : PostgreSQL
- **Image Docker** : PostgreSQL officielle (dernière version)
- **Port exposé** : 5435 (mappage vers 5432 en interne)
- **Volumes** : `pgdata:/var/lib/postgresql/data` - Volume persistant pour les données
- **Healthcheck** : Vérification périodique de la disponibilité avec `pg_isready`

## Configuration dans docker-compose.yml

```yaml
db:
  image: postgres:latest
  env_file: .env
  environment:
    POSTGRES_DB: ${POSTGRES_DB}
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  ports:
    - "5435:5432"
  volumes:
    - pgdata:/var/lib/postgresql/data
  networks: [backend]
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
    interval: 10s
    timeout: 5s
    retries: 5
```

Cette configuration dans docker-compose.yml définit le service de base de données PostgreSQL. Elle utilise l'image officielle PostgreSQL, configure les variables d'environnement, expose le port PostgreSQL, attache un volume pour la persistance des données et définit un healthcheck pour s'assurer que la base de données est prête avant que les services dépendants ne démarrent.

## Variables d'environnement

Les variables d'environnement suivantes sont définies dans le fichier `.env` :

```
POSTGRES_DB=devops_db
POSTGRES_USER=devops_user
POSTGRES_PASSWORD=devops_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
USE_POSTGRES=true
```

Ces variables configurent la base de données et permettent sa connexion depuis d'autres services.

## Schéma de base de données

Dans le cadre de l'application F_BRAIN, PostgreSQL stocke les données pour diverses entités, notamment :

1. **Utilisateurs** - Comptes et authentification
2. **Données métier** - Informations spécifiques au domaine d'application
3. **Configuration système** - Paramètres et configurations
4. **Tâches et planifications** - Informations sur les tâches Celery et leur statut

Le schéma exact dépend des modèles Django définis dans le service backend.

## Persistance des données

Les données PostgreSQL sont stockées dans un volume Docker nommé `pgdata`. Ce volume persiste même si les conteneurs sont arrêtés ou supprimés, assurant ainsi que les données ne sont pas perdues entre les redémarrages.

## Connexion depuis le backend

Le service backend Django se connecte à PostgreSQL en utilisant les paramètres définis dans `settings.py` :

```python
if os.getenv("USE_POSTGRES", "False").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "devops_db"),
            "USER": os.getenv("POSTGRES_USER", "devops_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "devops_pass"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    # Configuration SQLite pour le développement
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

Cette configuration permet au backend d'utiliser soit PostgreSQL (en production ou en mode Docker Compose), soit SQLite (en développement local).

## Sauvegardes et restauration

### Création d'une sauvegarde

Pour sauvegarder la base de données, vous pouvez utiliser `pg_dump` :

```bash
docker-compose exec db pg_dump -U devops_user -d devops_db > backup.sql
```

### Restauration depuis une sauvegarde

Pour restaurer une base de données à partir d'une sauvegarde :

```bash
cat backup.sql | docker-compose exec -T db psql -U devops_user -d devops_db
```

## Migrations de schéma

Les migrations de schéma sont gérées par Django. Lors du démarrage du service backend, les migrations sont automatiquement appliquées :

```bash
python manage.py migrate
```

Pour créer une nouvelle migration après modification des modèles :

```bash
python manage.py makemigrations
```

## Bonnes pratiques

1. **Sauvegardes régulières** - Planifier des sauvegardes automatiques
2. **Monitoring des performances** - Surveiller les métriques clés comme l'utilisation du CPU, de la mémoire et de l'espace disque
3. **Indexation** - Créer des index pour optimiser les requêtes fréquentes
4. **Optimisation des requêtes** - Analyser et optimiser les requêtes lentes
5. **Sécurité** - Utiliser des mots de passe forts et limiter l'accès réseau

## Dépannage courant

### La base de données ne démarre pas
- Vérifier les logs : `docker-compose logs db`
- S'assurer que les permissions sur le volume sont correctes
- Vérifier qu'il y a assez d'espace disque disponible

### Erreurs de connexion depuis le backend
- Vérifier que les variables d'environnement sont correctes
- S'assurer que le service db est accessible sur le réseau backend
- Contrôler les logs pour des erreurs d'authentification

### Performances lentes
- Vérifier si des requêtes longues sont en cours : `docker-compose exec db psql -U devops_user -d devops_db -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"`
- Analyser l'utilisation des ressources du conteneur
- Considérer l'optimisation des paramètres PostgreSQL dans un fichier `postgresql.conf` personnalisé

## Ressources additionnelles

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Guide PostgreSQL avec Docker](https://hub.docker.com/_/postgres/)
- [Documentation Django sur les migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)
