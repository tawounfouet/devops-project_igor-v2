#!/bin/bash

# Script d'arrêt propre pour les conteneurs de développement
echo "🛑 Arrêt des conteneurs de développement..."

# Arrêt des conteneurs
docker-compose down

# Optionnel : nettoyage des volumes et images inutilisées
echo "🧹 Voulez-vous nettoyer les volumes et images inutilisées ? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🗑️  Nettoyage en cours..."
    docker system prune -f
    docker volume prune -f
    echo "✅ Nettoyage terminé !"
fi

echo "✅ Arrêt terminé !"
