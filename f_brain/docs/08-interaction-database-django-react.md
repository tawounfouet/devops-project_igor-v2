# Interaction Base de Données - Django - React

## 🎯 Objectif de ce document

Ce guide explique comment les données circulent entre la base de données PostgreSQL, le backend Django et le frontend React dans notre application météo. Il est destiné aux étudiants débutants qui souhaitent comprendre et reproduire ce projet.

## 📋 Table des matières

1. [Vue d'ensemble de l'architecture](#vue-densemble-de-larchitecture)
2. [La base de données PostgreSQL](#la-base-de-données-postgresql)
3. [Configuration PostgreSQL avec Django](#configuration-postgresql-avec-django)
4. [Le backend Django](#le-backend-django)
5. [Le frontend React](#le-frontend-react)
6. [Flux de données complet](#flux-de-données-complet)
7. [Exemples pratiques](#exemples-pratiques)
8. [Comment tester l'interaction](#comment-tester-linteraction)
9. [Problèmes courants et solutions](#problèmes-courants-et-solutions)

## 🏗️ Vue d'ensemble de l'architecture

Notre application suit une architecture **3-tiers** classique :

```
┌─────────────────┐    HTTP/API    ┌─────────────────┐    SQL/ORM    ┌─────────────────┐
│                 │   Requests     │                 │   Queries     │                 │
│   React Client  │ ──────────────▶│  Django Server  │ ──────────────▶│   PostgreSQL    │
│   (Frontend)    │                │   (Backend)     │               │   (Database)    │
│                 │◀────────────── │                 │◀────────────── │                 │
└─────────────────┘    JSON        └─────────────────┘    Data       └─────────────────┘
```

### Rôles de chaque composant :

- **React** : Interface utilisateur (ce que voit l'utilisateur)
- **Django** : Logique métier et API (traitement des données)
- **PostgreSQL** : Stockage persistant des données

## 🗃️ La base de données PostgreSQL

### Qu'est-ce que PostgreSQL ?

PostgreSQL est un système de gestion de base de données relationnelle (SGBDR) qui stocke nos données de manière organisée et persistante.

### Structure de notre base de données

Dans notre projet météo, nous avons une table principale :

```sql
-- Table weather_weathersearch
CREATE TABLE weather_weathersearch (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2),
    humidity INTEGER,
    wind_speed DECIMAL(5,2),
    pressure DECIMAL(7,2),
    description VARCHAR(200),
    icon VARCHAR(10),
    country VARCHAR(2),
    searched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Exemple de données stockées :

| id | city  | temperature | humidity | wind_speed | pressure | description | icon | country | searched_at |
|----|-------|-------------|----------|------------|----------|-------------|------|---------|-------------|
| 1  | Paris | 22.5        | 65       | 3.2        | 1013.25  | sunny       | 01d  | FR      | 2025-06-09 10:30:00 |
| 2  | London| 18.0        | 80       | 5.1        | 1008.50  | cloudy      | 02d  | GB      | 2025-06-09 11:15:00 |

## ⚙️ Configuration PostgreSQL avec Django

### Pourquoi PostgreSQL avec Django ?

PostgreSQL est un choix excellent pour Django car :

- **Performance** : Optimisé pour les applications web
- **Fonctionnalités avancées** : Types de données riches, index performants
- **Fiabilité** : ACID compliant, sauvegardes robustes
- **Intégration Django** : Support natif excellent

### Configuration dans Docker Compose

Notre configuration PostgreSQL est définie dans `docker-compose.yml` :

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:latest
    env_file: .env
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5435:5432"  # Port externe:interne
    volumes:
      - pgdata:/var/lib/postgresql/data  # Persistance des données
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Explication des paramètres :**

- `image: postgres:latest` : Utilise la dernière version de PostgreSQL
- `env_file: .env` : Charge les variables d'environnement depuis le fichier `.env`
- `ports: "5435:5432"` : Mappe le port 5432 du conteneur vers le port 5435 de l'hôte
- `volumes: pgdata:/var/lib/postgresql/data` : Persiste les données même si le conteneur est supprimé
- `healthcheck` : Vérifie que PostgreSQL est prêt à accepter des connexions

### Variables d'environnement

Le fichier `.env` contient les informations de connexion :

```bash
# .env
POSTGRES_DB=devops_db
POSTGRES_USER=devops_user
POSTGRES_PASSWORD=devops_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

**Sécurité** : En production, utilisez des mots de passe forts et des secrets sécurisés !

### Configuration Django

Dans `settings.py`, Django est configuré pour utiliser PostgreSQL :

```python
# server/server_config/settings.py

# Configuration de la base de données PostgreSQL
postgres_db = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("POSTGRES_DB", "devops_db"),
    "USER": os.getenv("POSTGRES_USER", "devops_user"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD", "devops_pass"),
    "HOST": os.getenv("POSTGRES_HOST", "db"),
    "PORT": os.getenv("POSTGRES_PORT", "5432"),
    "OPTIONS": {
        "connect_timeout": 5,  # Timeout de connexion
    },
    "CONN_MAX_AGE": 60,  # Connexions persistantes (60 secondes)
}

# Configuration SQLite pour le développement local
sqlite_db = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

# Détection automatique de l'environnement
def is_running_in_docker():
    try:
        socket.gethostbyname("db")  # Teste si le service 'db' est accessible
        return True
    except socket.gaierror:
        return False

# Choix automatique de la base de données
use_postgres = (
    is_running_in_docker() or 
    os.getenv("USE_POSTGRES", "False").lower() == "true"
)

if use_postgres:
    try:
        __import__("psycopg2")  # Vérifier que le driver PostgreSQL est installé
        DATABASES = {"default": postgres_db}
    except ImportError:
        print("WARNING: psycopg2 not found. Falling back to SQLite database")
        DATABASES = {"default": sqlite_db}
else:
    DATABASES = {"default": sqlite_db}
```

### Dépendances Python

Pour que Django puisse communiquer avec PostgreSQL, nous avons besoin du driver `psycopg2` :

```toml
# pyproject.toml
[tool.poetry.dependencies]
psycopg2-binary = "^2.9.9"  # Driver PostgreSQL pour Django
```

Ou dans `requirements.txt` :

```txt
psycopg2-binary==2.9.9
```

### Migrations Django avec PostgreSQL

Les migrations Django créent automatiquement les tables PostgreSQL :

```python
# weather/models.py
class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    # ... autres champs
```

**Création de la migration :**
```bash
python manage.py makemigrations weather
```

**Application de la migration :**
```bash
python manage.py migrate
```

**Ce que ça génère en PostgreSQL :**
```sql
-- Migration automatiquement générée par Django
CREATE TABLE "weather_weathersearch" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "city" varchar(100) NOT NULL,
    "temperature" numeric(5,2),
    "humidity" integer,
    "wind_speed" numeric(5,2),
    "pressure" numeric(7,2),
    "description" varchar(200),
    "icon" varchar(10),
    "country" varchar(2),
    "searched_at" timestamptz NOT NULL
);

-- Index automatique sur la clé primaire
CREATE INDEX "weather_weathersearch_id" ON "weather_weathersearch" ("id");
```

### Avantages de cette configuration

#### 1. **Flexibilité Développement/Production**
```python
# Développement local : SQLite (simple)
# Docker/Production : PostgreSQL (robuste)
```

#### 2. **Connexions Persistantes**
```python
"CONN_MAX_AGE": 60  # Réutilise les connexions pendant 60 secondes
```
**Bénéfice** : Améliore les performances en évitant de rouvrir une connexion à chaque requête.

#### 3. **Gestion des Erreurs**
```python
try:
    __import__("psycopg2")
    DATABASES = {"default": postgres_db}
except ImportError:
    print("WARNING: Falling back to SQLite")
    DATABASES = {"default": sqlite_db}
```
**Bénéfice** : L'application fonctionne même si PostgreSQL n'est pas disponible.

#### 4. **Monitoring de Santé**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
```
**Bénéfice** : Docker Compose attend que PostgreSQL soit prêt avant de démarrer Django.

### Commandes utiles PostgreSQL

#### Se connecter à la base de données

```bash
# Depuis l'hôte (port 5435)
psql -h localhost -p 5435 -U devops_user -d devops_db

# Depuis le conteneur Docker
docker exec -it f_brain-db-1 psql -U devops_user -d devops_db
```

#### Commandes SQL utiles

```sql
-- Lister les tables
\dt

-- Décrire une table
\d weather_weathersearch

-- Voir les données
SELECT * FROM weather_weathersearch ORDER BY searched_at DESC LIMIT 5;

-- Statistiques
SELECT COUNT(*) as total_searches, 
       COUNT(DISTINCT city) as unique_cities 
FROM weather_weathersearch;

-- Recherches par pays
SELECT country, COUNT(*) as searches 
FROM weather_weathersearch 
GROUP BY country 
ORDER BY searches DESC;
```

#### Sauvegardes et restauration

```bash
# Sauvegarde
docker exec f_brain-db-1 pg_dump -U devops_user devops_db > backup.sql

# Restauration
docker exec -i f_brain-db-1 psql -U devops_user devops_db < backup.sql
```

### Configuration avancée

#### Index personnalisés

```python
# weather/models.py
class WeatherSearch(models.Model):
    # ... champs existants
    
    class Meta:
        indexes = [
            models.Index(fields=['city']),  # Index sur la ville
            models.Index(fields=['searched_at']),  # Index sur la date
            models.Index(fields=['city', 'searched_at']),  # Index composé
        ]
```

#### Contraintes de base de données

```python
class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(-100),  # Température minimale
            MaxValueValidator(100)    # Température maximale
        ]
    )
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(humidity__gte=0) & models.Q(humidity__lte=100),
                name='valid_humidity_range'
            )
        ]
```

### Monitoring et Performance

#### Logging des requêtes SQL

```python
# settings.py (pour le développement uniquement)
if DEBUG:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

#### Optimisation des requêtes

```python
# Inefficace : N+1 requêtes
for search in WeatherSearch.objects.all():
    print(search.city)

# Efficace : 1 seule requête
searches = WeatherSearch.objects.only('city')
for search in searches:
    print(search.city)
```

### Troubleshooting PostgreSQL

#### Problème : "relation does not exist"

**Cause** : Les migrations n'ont pas été appliquées.

**Solution** :
```bash
docker exec f_brain-web-1 python manage.py migrate
```

#### Problème : "password authentication failed"

**Cause** : Mauvaises credentials ou base non initialisée.

**Solution** :
```bash
# Vérifier les variables d'environnement
docker exec f_brain-web-1 env | grep POSTGRES

# Recréer la base de données
docker-compose down -v
docker-compose up -d db
```

#### Problème : "connection timed out"

**Cause** : PostgreSQL n'est pas encore prêt.

**Solution** :
```bash
# Vérifier la santé du conteneur
docker exec f_brain-db-1 pg_isready -U devops_user

# Attendre que PostgreSQL soit prêt
docker-compose up --wait db
```

## 🐍 Le backend Django

### Rôle de Django

Django agit comme **intermédiaire** entre React et PostgreSQL. Il :

1. **Reçoit** les requêtes HTTP du frontend
2. **Traite** la logique métier
3. **Interroge** la base de données
4. **Retourne** les données au format JSON

### Les composants clés

#### 1. Models (Modèles)
Les modèles définissent la structure des données :

```python
# weather/models.py
from django.db import models

class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    country = models.CharField(max_length=2)
    searched_at = models.DateTimeField(auto_now_add=True)
```

**Explication** : Ce modèle Django correspond exactement à notre table PostgreSQL. Django utilise l'ORM (Object-Relational Mapping) pour convertir automatiquement entre les objets Python et les tables SQL.

#### 2. Views (Vues/API)
Les vues traitent les requêtes HTTP :

```python
# weather/api_views.py
from django.http import JsonResponse
from .models import WeatherSearch

def get_weather(request):
    city = request.GET.get("city")
    
    # 1. Appel à l'API météo externe
    weather_data = fetch_weather_from_api(city)
    
    # 2. Sauvegarde en base de données
    weather_record = WeatherSearch(
        city=weather_data["name"],
        temperature=weather_data["main"]["temp"],
        # ... autres champs
    )
    weather_record.save()  # ← Ici Django sauvegarde en PostgreSQL
    
    # 3. Retour de la réponse JSON
    return JsonResponse({"data": weather_data})
```

#### 3. URLs (Routage)
Les URLs définissent les points d'accès de l'API :

```python
# weather/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path("weather/", api_views.get_weather, name="api_get_weather"),
    path("history/", api_views.get_weather_history, name="api_get_history"),
]
```

### Comment Django communique avec PostgreSQL

Django utilise l'**ORM** (Object-Relational Mapping) qui traduit automatiquement :

```python
# Code Python (ORM)
weather_record.save()

# Se traduit en SQL
INSERT INTO weather_weathersearch (city, temperature, humidity, ...)
VALUES ('Paris', 22.5, 65, ...);
```

```python
# Code Python (ORM)
WeatherSearch.objects.all()[:10]

# Se traduit en SQL
SELECT * FROM weather_weathersearch ORDER BY id DESC LIMIT 10;
```

## ⚛️ Le frontend React

### Rôle de React

React crée l'**interface utilisateur** et communique avec Django via des **requêtes HTTP**.

### Structure typique d'un composant React

```jsx
// src/components/WeatherApp.jsx
import React, { useState } from 'react';

function WeatherApp() {
    const [weather, setWeather] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchWeather = async (city) => {
        setLoading(true);
        try {
            // Requête HTTP vers Django
            const response = await fetch(`http://localhost:8000/api/weather/?city=${city}`);
            const data = await response.json();
            
            setWeather(data);
        } catch (error) {
            console.error('Erreur:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Entrez une ville"
                onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                        fetchWeather(e.target.value);
                    }
                }}
            />
            {loading && <p>Chargement...</p>}
            {weather && (
                <div>
                    <h2>{weather.data.name}</h2>
                    <p>Température: {weather.data.main.temp}°C</p>
                    <p>Humidité: {weather.data.main.humidity}%</p>
                </div>
            )}
        </div>
    );
}
```

### Comment React communique avec Django

React utilise l'**API Fetch** ou **Axios** pour envoyer des requêtes HTTP :

```javascript
// Requête GET pour obtenir la météo
fetch('http://localhost:8000/api/weather/?city=Paris')
    .then(response => response.json())
    .then(data => console.log(data));

// Requête GET pour l'historique
fetch('http://localhost:8000/api/history/')
    .then(response => response.json())
    .then(history => console.log(history));
```

## 🔄 Flux de données complet

Voici le parcours complet d'une recherche météo :

### 1. Action utilisateur
```
Utilisateur tape "Paris" et appuie sur Entrée
```

### 2. React → Django (Requête HTTP)
```javascript
// React envoie une requête
fetch('http://localhost:8000/api/weather/?city=Paris')
```

### 3. Django traite la requête
```python
# Django reçoit la requête
def get_weather(request):
    city = request.GET.get("city")  # "Paris"
    
    # Appel API météo externe
    weather_data = requests.get(f"https://api.openweathermap.org/...")
    
    # Sauvegarde en base
    weather_record = WeatherSearch(city="Paris", temperature=22.5, ...)
    weather_record.save()  # ← Ici : Django → PostgreSQL
```

### 4. Django → PostgreSQL (Requête SQL)
```sql
-- Django exécute automatiquement :
INSERT INTO weather_weathersearch (city, temperature, humidity, ...)
VALUES ('Paris', 22.5, 65, ...);
```

### 5. PostgreSQL → Django (Données)
```
PostgreSQL confirme l'insertion et retourne l'ID du nouvel enregistrement
```

### 6. Django → React (Réponse JSON)
```json
{
    "data": {
        "name": "Paris",
        "main": {
            "temp": 22.5,
            "humidity": 65
        }
    },
    "saved_record": {
        "id": 123,
        "city": "Paris",
        "temperature": 22.5,
        "searched_at": "2025-06-09T10:30:00Z"
    }
}
```

### 7. React affiche les données
```jsx
// React met à jour l'interface
setWeather(data);  // ← L'utilisateur voit les résultats
```

## 💡 Exemples pratiques

### Exemple 1 : Recherche météo simple

**Frontend (React) :**
```jsx
const handleSearch = async (city) => {
    const response = await fetch(`/api/weather/?city=${city}`);
    const result = await response.json();
    setWeatherData(result.data);
};
```

**Backend (Django) :**
```python
def get_weather(request):
    city = request.GET.get("city")
    
    # Logique métier
    weather_api_data = call_external_weather_api(city)
    
    # Sauvegarde en base
    WeatherSearch.objects.create(
        city=weather_api_data["name"],
        temperature=weather_api_data["main"]["temp"]
    )
    
    return JsonResponse({"data": weather_api_data})
```

**Base de données (PostgreSQL) :**
```sql
-- Nouvelle ligne ajoutée automatiquement
INSERT INTO weather_weathersearch (city, temperature, searched_at)
VALUES ('Paris', 22.5, NOW());
```

### Exemple 2 : Affichage de l'historique

**Frontend (React) :**
```jsx
useEffect(() => {
    fetch('/api/history/')
        .then(response => response.json())
        .then(history => setHistoryData(history));
}, []);
```

**Backend (Django) :**
```python
def get_weather_history(request):
    limit = int(request.GET.get("limit", 10))
    history = WeatherSearch.objects.all()[:limit]
    
    history_data = [
        {
            "city": record.city,
            "temperature": record.temperature,
            "searched_at": record.searched_at.isoformat()
        }
        for record in history
    ]
    
    return JsonResponse(history_data, safe=False)
```

**Base de données (PostgreSQL) :**
```sql
-- Django exécute automatiquement :
SELECT * FROM weather_weathersearch ORDER BY id DESC LIMIT 10;
```

## 🧪 Comment tester l'interaction

### 1. Tester la base de données directement

Connectez-vous à PostgreSQL :
```bash
# Dans le conteneur Docker
docker exec -it f_brain-db-1 psql -U devops_user -d devops_db

# Vérifier les données
SELECT * FROM weather_weathersearch ORDER BY searched_at DESC LIMIT 5;
```

### 2. Tester l'API Django

Utilisez curl ou un navigateur :
```bash
# Test de l'endpoint météo
curl "http://localhost:8000/api/weather/?city=Paris"

# Test de l'historique
curl "http://localhost:8000/api/history/"
```

### 3. Tester l'interface React

Ouvrez `http://localhost:4173` dans votre navigateur et :
1. Entrez une ville
2. Vérifiez que les données s'affichent
3. Vérifiez l'historique

### 4. Vérifier les logs

```bash
# Logs du backend Django
docker logs f_brain-web-1

# Logs de la base de données
docker logs f_brain-db-1

# Logs du frontend React
docker logs f_brain-frontend-1
```

## ⚠️ Problèmes courants et solutions

### Problème 1 : Erreur de connexion à la base de données

**Symptôme :**
```
django.db.utils.OperationalError: could not connect to server
```

**Solution :**
1. Vérifier que PostgreSQL est démarré :
   ```bash
   docker ps | grep postgres
   ```
2. Vérifier les variables d'environnement dans `.env`
3. Vérifier la santé du conteneur :
   ```bash
   docker exec f_brain-db-1 pg_isready
   ```

### Problème 2 : CORS (Cross-Origin Resource Sharing)

**Symptôme :**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:4173' 
has been blocked by CORS policy
```

**Solution :**
Vérifier la configuration CORS dans `settings.py` :
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

### Problème 3 : API externe non accessible

**Symptôme :**
```
requests.exceptions.ConnectionError: HTTPSConnectionPool
```

**Solution :**
1. Vérifier la clé API OpenWeatherMap
2. Vérifier la connexion internet du conteneur
3. Utiliser des données de test si nécessaire

### Problème 4 : Données non sauvegardées

**Symptôme :** L'historique reste vide malgré les recherches

**Solution :**
1. Vérifier les migrations Django :
   ```bash
   docker exec f_brain-web-1 python manage.py showmigrations
   ```
2. Appliquer les migrations si nécessaire :
   ```bash
   docker exec f_brain-web-1 python manage.py migrate
   ```

## 🎓 Pour aller plus loin

### Concepts à approfondir :

1. **ORM Django** : Comment Django traduit les objets Python en SQL
2. **API RESTful** : Principes de conception d'API
3. **Sérialisation JSON** : Comment convertir les données entre formats
4. **État React** : Gestion des données côté frontend
5. **Hooks React** : `useState`, `useEffect` pour la gestion des données

### Exercices pratiques :

1. Ajouter un nouveau champ à la table météo
2. Créer un endpoint pour supprimer des recherches
3. Implémenter une recherche par pays
4. Ajouter une pagination à l'historique
5. Créer des graphiques avec les données historiques

### Ressources recommandées :

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation React](https://react.dev/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)
- [API REST Best Practices](https://restfulapi.net/)

---

**💡 Conseil :** La meilleure façon d'apprendre est de **pratiquer** ! Modifiez le code, cassez quelque chose, puis réparez-le. C'est ainsi qu'on comprend vraiment comment tout fonctionne ensemble.
