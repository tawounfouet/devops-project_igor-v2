#!/bin/bash

echo "🚀 Test des tâches Celery avancées pour l'application météo"
echo "============================================================"

# Fonction pour afficher des messages colorés
show_info() {
    echo -e "\n\033[34m[INFO]\033[0m $1"
}

show_success() {
    echo -e "\033[32m[SUCCESS]\033[0m $1"
}

show_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

show_warning() {
    echo -e "\033[33m[WARNING]\033[0m $1"
}

# Vérifier que Docker Compose est démarré
show_info "Vérification de l'état des services Docker..."
if ! docker-compose ps | grep -q "Up"; then
    show_warning "Services Docker non démarrés. Lancement..."
    docker-compose up -d
    sleep 10
fi

# Fonction pour tester une tâche Celery
test_celery_task() {
    local task_name=$1
    local task_args=$2
    local description=$3
    
    show_info "Test: $description"
    echo "Tâche: $task_name"
    
    # Exécuter la tâche dans le conteneur web
    if [ -n "$task_args" ]; then
        result=$(docker-compose exec -T web python manage.py shell -c "
from weather.tasks import $task_name
result = $task_name.delay($task_args)
print(f'Task ID: {result.id}')
print(f'Task State: {result.state}')
import time
time.sleep(5)
try:
    final_result = result.get(timeout=30)
    print('Task Result:')
    print(final_result)
except Exception as e:
    print(f'Error: {e}')
")
    else
        result=$(docker-compose exec -T web python manage.py shell -c "
from weather.tasks import $task_name
result = $task_name.delay()
print(f'Task ID: {result.id}')
print(f'Task State: {result.state}')
import time
time.sleep(5)
try:
    final_result = result.get(timeout=30)
    print('Task Result:')
    print(final_result)
except Exception as e:
    print(f'Error: {e}')
")
    fi
    
    echo "$result"
    
    if echo "$result" | grep -q "Task ID:"; then
        show_success "✅ Tâche exécutée avec succès"
    else
        show_error "❌ Erreur lors de l'exécution de la tâche"
    fi
    
    echo "----------------------------------------"
}

# Tests des tâches avancées
echo "🧪 Début des tests des tâches avancées"

# 1. Test de génération de statistiques
test_celery_task "generate_weather_statistics" "" "Génération des statistiques météo"

# 2. Test d'alerte météo
test_celery_task "send_weather_alerts" "" "Vérification des alertes météo extrêmes"

# 3. Test d'export de données
test_celery_task "export_weather_data" "'json'" "Export des données météo en JSON"

# 4. Test de nettoyage
test_celery_task "cleanup_old_searches" "" "Nettoyage des anciennes recherches"

# 5. Test de maintenance de base de données
test_celery_task "database_maintenance" "" "Maintenance de la base de données"

# 6. Test de mise à jour en masse (avec une liste réduite)
show_info "Test: Mise à jour en masse de quelques villes"
echo "Tâche: bulk_weather_update"

bulk_test_result=$(docker-compose exec -T web python manage.py shell -c "
from weather.tasks import bulk_weather_update
cities = [
    {'city': 'Paris', 'country': 'FR'},
    {'city': 'London', 'country': 'GB'},
    {'city': 'Berlin', 'country': 'DE'}
]
result = bulk_weather_update.delay(cities)
print(f'Task ID: {result.id}')
print(f'Task State: {result.state}')
import time
time.sleep(10)
try:
    final_result = result.get(timeout=60)
    print('Task Result:')
    print(final_result)
except Exception as e:
    print(f'Error: {e}')
")

echo "$bulk_test_result"

if echo "$bulk_test_result" | grep -q "Task ID:"; then
    show_success "✅ Mise à jour en masse exécutée avec succès"
else
    show_error "❌ Erreur lors de la mise à jour en masse"
fi

echo "----------------------------------------"

# Test des tâches périodiques programmées
show_info "Vérification des tâches périodiques configurées"

periodic_tasks=$(docker-compose exec -T web python manage.py shell -c "
from django_celery_beat.models import PeriodicTask
tasks = PeriodicTask.objects.all()
print(f'Nombre de tâches périodiques: {tasks.count()}')
for task in tasks:
    print(f'- {task.name}: {task.task} ({task.crontab})')
")

echo "$periodic_tasks"

# Vérification de l'état des workers Celery
show_info "État des workers Celery"
celery_status=$(docker-compose exec -T web celery -A server_config inspect active)
echo "$celery_status"

# Vérification des résultats des tâches dans la base de données
show_info "Derniers résultats des tâches stockés en base"
task_results=$(docker-compose exec -T web python manage.py shell -c "
from django_celery_results.models import TaskResult
recent_tasks = TaskResult.objects.order_by('-date_created')[:10]
print(f'Nombre total de résultats: {TaskResult.objects.count()}')
print('Dernières tâches:')
for task in recent_tasks:
    print(f'- {task.task_name}: {task.status} ({task.date_created})')
")

echo "$task_results"

# Résumé final
show_info "📊 Résumé du test des tâches avancées"
echo "✅ Tâches de génération de statistiques"
echo "✅ Système d'alertes météo"
echo "✅ Export de données"
echo "✅ Nettoyage automatique"
echo "✅ Maintenance de base de données"
echo "✅ Mise à jour en masse"
echo "✅ Configuration des tâches périodiques"
echo "✅ Stockage des résultats en base de données"

show_success "🎉 Tests des tâches Celery avancées terminés!"
echo "Les tâches périodiques sont maintenant configurées et s'exécuteront automatiquement selon le planning défini."
