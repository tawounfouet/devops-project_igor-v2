
🚀 Projet DevOps Complet : README.md
Yo frérot ! Si tu lis ça, c'est que t'es prêt à envoyer du lourd avec un setup complet DevOps en mode React + Django + Celery + Docker + Nginx + Grafana + Prometheus + RabbitMQ. Accroche-toi, on y va étape par étape ! 💪

📁 Étape 1 : Structure de base
D'abord, ouvre ton terminal et fais ça proprement :

mkdir f_brain
cd f_brain

# Crée les dossiers
mkdir client server proxy
⚛️ Étape 2 : Setup du client React avec Yarn
On commence par React :

cd client
yarn create vite . --template react

# installe les dépendances
yarn
Ajoute un fichier Dockerfile simple dans ce dossier (client/Dockerfile) :

FROM node:alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
Voilà, le front c'est fait pour le moment.

🐍 Étape 3 : Setup du serveur Django avec Poetry
Dans le dossier racine :

cd ..
poetry init -n
poetry add django celery django-prometheus django-celery-results django-celery-beat psycopg2-binary

# Crée le projet Django (directement dans le dossier)
poetry run django-admin startproject server_config .
Tu obtiens :

server/
├── manage.py
├── server_config/
│   ├── _init_.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
Configure Celery
Crée server_config/celery.py (prends le template de Celery Django).

Dans serverconfig/_init_.py :

from .celery import app as celery_app

_all_ = ('celery_app',)
Dans server_config/settings.py ajoute :
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

INSTALLED_APPS += [
    'django_prometheus',
    'django_celery_results',
    'django_celery_beat',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'devops_db'),
        'USER': os.getenv('POSTGRES_USER', 'devops_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'devops_pass'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': 5432,
    }
}
Dockerfile Django
Ajoute dans server/Dockerfile :

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y build-essential gcc libpq-dev \
    && pip install poetry==2.1.2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .
🌐 Étape 4 : Setup du Proxy Nginx
Dans le dossier proxy ajoute :

Un Dockerfile :
FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
default.conf :
server {
    listen 80;

    location / {
        proxy_pass http://client:5173;
    }

    location /api/ {
        proxy_pass http://server:8000;
    }
    { ... }
}
🐳 Étape 5 : Docker Compose
À la racine du projet (f_brain/docker-compose.yml) :

networks:
  backend:
    driver: bridge # isolation du trafic inter-services

volumes:
  pgdata:
  prometheus_data:
  grafana_data:

services:
  nginx:
    build:
      context: ./proxy
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    networks: [backend]
    depends_on:
      - frontend
      - web

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

  grafana:
    image: grafana/grafana:latest
    env_file: .env
    restart: always
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: ${GF_SECURITY_ADMIN_USER:-admin}
      GF_SECURITY_ADMIN_PASSWORD: ${GF_SECURITY_ADMIN_PASSWORD:-admin}
    volumes:
      - ./grafana.ini:/etc/grafana/grafana.ini:ro
      - grafana_data:/var/lib/grafana
    networks: [backend]
    depends_on:
      prometheus:
        condition: service_healthy

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "wget --spider http://localhost:9090/-/ready"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:latest
    env_file: .env
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myuser -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: ./server
      dockerfile: Dockerfile
    env_file: .env
    command: >
      sh -c "
        python manage.py migrate &&
        gunicorn server_config.wsgi:application --bind 0.0.0.0:8000
      "
    networks: [backend]
    expose:
      - "8000"
    depends_on:
      db:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy

  celery:
    build:
      context: ./server
      dockerfile: Dockerfile
    env_file: .env
    command: celery -A server_config worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydb
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    networks: [backend]
    depends_on: [web, rabbitmq]

  frontend:
    build:
      context: ./client
      dockerfile: Dockerfile
    expose:
      - "4173"
    networks: [backend]

🔑 Étape 6 : Fichier .env
À la racine crée .env :

POSTGRES_DB=devops_db
POSTGRES_USER=devops_user
POSTGRES_PASSWORD=devops_pass
POSTGRES_HOST=db
DJANGO_SECRET_KEY=un_secret_costaud
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
DJANGO_DEBUG=True
🚦 Lancer tout ça
docker compose up --build
Va sur localhost pour voir ton app React, et teste localhost/api pour Django.