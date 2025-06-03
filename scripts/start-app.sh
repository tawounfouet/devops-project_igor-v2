#!/bin/bash
# Script de démarrage pour l'application Weather App avec double accès

echo "🌤️  Weather App - Starting Services..."
echo "======================================="

# Démarrer tous les services Docker
echo "Starting Docker services..."
docker-compose up -d

# Attendre que tous les services soient prêts
echo "Waiting for services to be ready..."
sleep 5

# Vérifier le statut des services
echo
echo "📊 Service Status:"
docker-compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"

echo
echo "🚀 Application Ready!"
echo "===================="
echo
echo "🎯 Development Access (Direct Frontend):"
echo "   URL: http://localhost:4173"
echo "   Use: Frontend development with HMR"
echo "   API: Direct to backend (http://localhost:8000/api/v1)"
echo
echo "🌐 Production Access (Via Nginx):"
echo "   URL: http://localhost"
echo "   Use: Full stack testing"
echo "   API: Through nginx proxy (/api/v1)"
echo
echo "📋 Additional Services:"
echo "   Grafana:    http://localhost:3003 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo "   RabbitMQ:   http://localhost:15672 (guest/guest)"
echo "   Backend:    http://localhost:8000"
echo
echo "🧪 Testing:"
echo "   Run: ./test-dual-access.sh"
echo "   Run: ./test-app.sh"
echo
echo "🛑 To stop all services:"
echo "   Run: docker-compose down"
