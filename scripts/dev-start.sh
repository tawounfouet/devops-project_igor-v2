#!/bin/bash

# Script de développement pour la synchronisation des fichiers
echo "🚀 Démarrage du mode développement avec synchronisation des fichiers..."

# Arrêt des conteneurs existants
echo "📦 Arrêt des conteneurs existants..."
docker-compose down

# Reconstruction des images sans cache pour s'assurer d'avoir les dernières modifications
echo "🔨 Reconstruction des images..."
docker-compose build --no-cache

# Démarrage des services en mode développement
echo "🎯 Démarrage des services..."
docker-compose up -d

# Affichage des logs en temps réel
echo "📊 Affichage des logs (Ctrl+C pour arrêter l'affichage des logs)..."
docker-compose logs -f web frontend

echo "✅ Services démarrés !"
echo "🌐 Frontend: http://localhost:80"
echo "🔧 API Backend: http://localhost:8000/api/v1/"
echo "📊 Grafana: http://localhost:3003"
echo "🐰 RabbitMQ: http://localhost:15672"
