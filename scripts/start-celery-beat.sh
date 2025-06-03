#!/bin/bash

echo "🕰️ Démarrage du scheduler Celery Beat pour les tâches périodiques"
echo "=================================================================="

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

# Vérifier que les services sont démarrés
show_info "Vérification de l'état des services Docker..."
if ! docker-compose ps | grep -q "Up"; then
    show_error "Services Docker non démarrés. Veuillez d'abord exécuter 'docker-compose up -d'"
    exit 1
fi

# Créer les tâches périodiques dans la base de données
show_info "Création des tâches périodiques dans la base de données..."
docker-compose exec web python manage.py shell -c "
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone

# Créer les horaires cron s'ils n'existent pas
schedules = [
    {'hour': 2, 'minute': 0, 'name': 'daily-2am'},
    {'hour': 6, 'minute': 0, 'name': 'daily-6am'},
    {'hour': 8, 'minute': 0, 'name': 'daily-8am'},
    {'hour': 3, 'minute': 0, 'day_of_week': 0, 'name': 'sunday-3am'},
    {'hour': 7, 'minute': 0, 'day_of_week': 1, 'name': 'monday-7am'},
    {'minute': 0, 'hour': '*/2', 'name': 'every-2-hours'},
    {'minute': '*/15', 'name': 'every-15-minutes'},
]

for schedule_data in schedules:
    name = schedule_data.pop('name')
    schedule, created = CrontabSchedule.objects.get_or_create(**schedule_data)
    if created:
        print(f'Créé horaire: {name}')
    else:
        print(f'Horaire existant: {name}')

print('Horaires configurés avec succès!')
"

# Démarrer Celery Beat en arrière-plan
show_info "Démarrage du scheduler Celery Beat..."

# Arrêter le processus existant s'il y en a un
docker-compose exec web pkill -f "celery.*beat" || true

# Démarrer Celery Beat
docker-compose exec -d web celery -A server_config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

sleep 3

# Vérifier que Beat est démarré
if docker-compose exec web pgrep -f "celery.*beat" > /dev/null; then
    show_success "✅ Celery Beat démarré avec succès!"
    
    # Afficher les tâches périodiques configurées
    show_info "Tâches périodiques configurées:"
    docker-compose exec web python manage.py shell -c "
from django_celery_beat.models import PeriodicTask
tasks = PeriodicTask.objects.all()
for task in tasks:
    print(f'🔄 {task.name}:')
    print(f'   Tâche: {task.task}')
    if task.crontab:
        print(f'   Planning: {task.crontab}')
    print(f'   Activé: {task.enabled}')
    print()
"
    
    show_info "Suivi des logs Celery Beat (Ctrl+C pour arrêter):"
    docker-compose logs -f web | grep -i beat
    
else
    show_error "❌ Échec du démarrage de Celery Beat"
    exit 1
fi
