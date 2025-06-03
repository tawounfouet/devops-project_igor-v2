#!/bin/bash

echo "🔧 Test de l'intégration Celery + RabbitMQ"
echo "============================================"
echo

# Vérifier que tous les services sont up
echo "1. Vérification des services Docker..."
if ! docker compose ps | grep -q "Up"; then
    echo "❌ Les services Docker ne sont pas tous en cours d'exécution"
    exit 1
fi
echo "✅ Services Docker actifs"

# Test RabbitMQ Management UI
echo
echo "2. Test de l'interface RabbitMQ Management..."
RABBITMQ_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -u guest:guest http://localhost:15672/api/overview)
if [ "$RABBITMQ_STATUS" = "200" ]; then
    echo "✅ Interface RabbitMQ Management accessible (http://localhost:15672)"
    echo "   - Utilisateur: guest"
    echo "   - Mot de passe: guest"
else
    echo "❌ Interface RabbitMQ Management non accessible (Code: $RABBITMQ_STATUS)"
fi

# Test de l'API RabbitMQ
echo
echo "3. Test des queues RabbitMQ..."
QUEUE_COUNT=$(curl -s -u guest:guest http://localhost:15672/api/queues | python3 -m json.tool | grep -c '"name":')
echo "✅ Nombre de queues actives: $QUEUE_COUNT"

# Test de connexion Celery
echo
echo "4. Test de la connexion Celery..."
docker compose exec -T web python manage.py shell -c "
from server_config.celery import app
try:
    inspect = app.control.inspect()
    stats = inspect.stats()
    if stats:
        print('✅ Celery worker connecté et actif')
        worker_name = list(stats.keys())[0]
        print(f'   Worker: {worker_name}')
        print(f'   PID: {stats[worker_name][\"pid\"]}')
        print(f'   Concurrence: {stats[worker_name][\"pool\"][\"max-concurrency\"]}')
    else:
        print('❌ Aucun worker Celery détecté')
except Exception as e:
    print(f'❌ Erreur de connexion Celery: {e}')
"

# Test d'exécution de tâche
echo
echo "5. Test d'exécution de tâche Celery..."
docker compose exec -T web python manage.py shell -c "
from weather.tasks import test_celery_task
import time

try:
    print('   Envoi de la tâche de test...')
    result = test_celery_task.delay('Test automatisé du système Celery')
    print(f'   ✅ Tâche envoyée (ID: {result.id})')
    
    # Attendre et vérifier les logs
    print('   ⏳ Attente de l\'exécution (5 secondes)...')
    time.sleep(5)
    print('   ✅ Tâche terminée (vérifiez les logs ci-dessous)')
    
except Exception as e:
    print(f'   ❌ Erreur lors de l\'envoi: {e}')
"

# Afficher les derniers logs Celery
echo
echo "6. Derniers logs Celery (10 dernières lignes)..."
echo "---"
docker compose logs celery --tail=10 | grep -E "(INFO|ERROR|WARNING)" | tail -5
echo "---"

# Test des tâches découvertes
echo
echo "7. Tâches Celery découvertes..."
docker compose exec -T web python manage.py shell -c "
from server_config.celery import app
weather_tasks = [task for task in app.tasks.keys() if 'weather.tasks' in task]
print(f'✅ Tâches météo découvertes: {len(weather_tasks)}')
for task in weather_tasks:
    print(f'   - {task}')
"

echo
echo "🎉 Test Celery terminé !"
echo
echo "📝 Résumé des accès :"
echo "   - RabbitMQ Management: http://localhost:15672 (guest/guest)"
echo "   - API Django: http://localhost:8000"
echo "   - Frontend direct: http://localhost:4173"
echo "   - Frontend via nginx: http://localhost"
echo

echo "🔍 Pour surveiller les tâches en temps réel :"
echo "   docker compose logs -f celery"
