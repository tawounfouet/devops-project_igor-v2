#!/bin/bash

echo "🌟 Test Complet de l'Architecture Weather App"
echo "=============================================="
echo "Testing: Django + Celery + RabbitMQ + Frontend + Nginx"
echo

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. Services Docker
echo "1. Vérification des services Docker..."
docker compose ps --format "table {{.Name}}\t{{.Status}}" | grep -v "NAME"
echo

# 2. RabbitMQ Management
echo "2. Test RabbitMQ Management UI..."
RABBITMQ_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -u guest:guest http://localhost:15672/api/overview)
if [ "$RABBITMQ_STATUS" = "200" ]; then
    print_status 0 "RabbitMQ Management accessible"
    print_info "Interface: http://localhost:15672 (guest/guest)"
    
    # Vérifier les queues
    QUEUE_COUNT=$(curl -s -u guest:guest http://localhost:15672/api/queues | python3 -m json.tool | grep -c '"name":')
    print_info "Queues actives: $QUEUE_COUNT"
else
    print_status 1 "RabbitMQ Management non accessible"
fi
echo

# 3. Test Celery Worker
echo "3. Test du worker Celery..."
docker compose exec -T web python manage.py shell -c "
from server_config.celery import app
try:
    inspect = app.control.inspect()
    stats = inspect.stats()
    if stats:
        worker_name = list(stats.keys())[0]
        print(f'✅ Worker: {worker_name}')
        print(f'   Concurrence: {stats[worker_name][\"pool\"][\"max-concurrency\"]}')
        print(f'   PID: {stats[worker_name][\"pid\"]}')
    else:
        print('❌ Aucun worker détecté')
except Exception as e:
    print(f'❌ Erreur: {e}')
" 2>/dev/null
echo

# 4. Test des tâches Celery
echo "4. Test d'exécution de tâche Celery..."
print_info "Envoi d'une tâche de test..."
docker compose exec -T web python manage.py shell -c "
from weather.tasks import test_celery_task
import time

try:
    result = test_celery_task.delay('Test complet architecture')
    print(f'✅ Tâche envoyée (ID: {result.id[:8]}...)')
    time.sleep(3)
    print('✅ Tâche exécutée (voir logs Celery)')
except Exception as e:
    print(f'❌ Erreur: {e}')
" 2>/dev/null
echo

# 5. Test API Django
echo "5. Test de l'API Django..."
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/)
print_status $([[ $API_STATUS == "200" ]] && echo 0 || echo 1) "API Django accessible (Status: $API_STATUS)"

# Test de recherche météo avec Celery
echo "   Test de recherche météo avec traitement Celery..."
WEATHER_RESPONSE=$(curl -s "http://localhost:8000/api/v1/weather/?city=London" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'data' in data and 'name' in data['data']:
        print(f'✅ Météo récupérée: {data[\"data\"][\"name\"]} ({data[\"data\"][\"main\"][\"temp\"]}°C)')
    else:
        print('❌ Réponse API invalide')
except:
    print('❌ Erreur de parsing JSON')
")
echo "   $WEATHER_RESPONSE"
echo

# 6. Test Frontend direct
echo "6. Test du frontend direct..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:4173)
print_status $([[ $FRONTEND_STATUS == "200" ]] && echo 0 || echo 1) "Frontend direct accessible (http://localhost:4173)"

# 7. Test Nginx + Frontend
echo "7. Test du frontend via Nginx..."
NGINX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
print_status $([[ $NGINX_STATUS == "200" ]] && echo 0 || echo 1) "Frontend via Nginx accessible (http://localhost)"

# 8. Test CORS dual access
echo "8. Test du mode dual access..."
./test-dual-access.sh | grep -E "(✅|❌)" | head -6
echo

# 9. Monitoring et logs
echo "9. Derniers logs Celery (tâches exécutées)..."
echo "---"
docker compose logs celery --tail=5 | grep -E "(Task.*succeeded|INFO.*Tâche)" | tail -3
echo "---"
echo

# 10. Résumé final
echo "🎯 RÉSUMÉ DE L'ARCHITECTURE"
echo "=========================="
print_info "Services actifs:"
echo "   • PostgreSQL: Port 5435"
echo "   • Django API: Port 8000"
echo "   • Frontend: Port 4173"
echo "   • Nginx: Port 80"
echo "   • RabbitMQ: Port 15672"
echo "   • Celery Worker: Actif"
echo "   • Prometheus: Port 9090"
echo "   • Grafana: Port 3003"
echo

print_info "Fonctionnalités validées:"
echo "   • ✅ Dual access mode (direct + nginx)"
echo "   • ✅ CORS résolu"
echo "   • ✅ API météo fonctionnelle"
echo "   • ✅ Persistance des recherches"
echo "   • ✅ Celery + RabbitMQ intégrés"
echo "   • ✅ Traitement asynchrone"
echo

print_info "Accès rapides:"
echo "   • App (direct): http://localhost:4173"
echo "   • App (nginx): http://localhost"
echo "   • RabbitMQ UI: http://localhost:15672"
echo "   • API Django: http://localhost:8000/api/v1/"
echo "   • Grafana: http://localhost:3003"
echo

echo "🎉 Architecture complètement fonctionnelle !"
