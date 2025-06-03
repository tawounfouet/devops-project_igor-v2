# devops-project_igor
projet DevOps de type microservices avec Docker, Prometheus, Grafana, RabbitMQ, PostgreSQL, etc. Le projet est organisé autour d'une architecture avec plusieurs conteneurs Docker 



## 🧭 1. Organisation du Projet
📁 Arborescence recommandée
```sh
devops-project-root/
├── client/               # Frontend (JS/React)
│   └── Dockerfile
├── server/               # Backend Django + Celery
│   ├── Dockerfile
│   ├── manage.py
│   └── ...
├── monitoring/           # Prometheus + Grafana
│   ├── prometheus.yml
│   └── Dockerfile (optionnel pour Grafana/Prometheus config)
├── proxy/                # Nginx Reverse Proxy
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## ⚙️ 2. Docker et Orchestration
📄 docker-compose.yml (extrait de base à enrichir)
```yaml
version: '3.8'
...
...
```


## Backend (Django + DRF) Setup
Commençons par mettre en place un projet Django + Django REST Framework (DRF) pour une application de blogging, de manière propre et prête à être containerisée ensuite dans le projet DevOps.

### 🚀 Étape 1 : Créer le projet Django avec DRF
1. 📁 Structure cible

```sh	
server/
├── server_config/  # Config Django
├── weather/       # Weather app   
├── manage.py
├── requirements.txt
├── Dockerfile
├── .env
```

### 🛠️ Étape 2 : Initialisation du project
Depuis le dossier server/ :

```bash
mkdir server
cd server


# Mise en place de l'environnement virtuel
python3 -m venv .venv

# Activation de l'environnement virtuel
# Linux/Mac 
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Installation de Django et DRF
pip install django djangorestframework psycopg2-binary
pip freeze > requirements.txt

# Création du projet Django
django-admin startproject core .
django-admin startapp blog
```

### 📝 Étape 3 : Configuration de Django

#### 1. Ajouter DRF et blog à INSTALLED_APPS
Dans `server_config/settings.py`, ajoutez les applications à la liste `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'weather',  # Nom de l'application créée
]
```
#### 2. Configurer la base de données PostgreSQL

