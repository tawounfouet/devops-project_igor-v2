#!/bin/bash

# Script de synchronisation des tâches périodiques Celery
# Ce script synchronise les tâches définies dans CELERY_BEAT_SCHEDULE avec la base de données

echo "🔄 Synchronisation des tâches périodiques Celery avec la base de données..."
echo "==========================================================================="

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis le répertoire racine du projet"
    exit 1
fi

# Fonction pour exécuter des commandes Django
run_django_command() {
    local command="$1"
    echo "📋 Exécution: $command"
    
    if docker-compose exec web python manage.py $command; then
        echo "✅ Commande exécutée avec succès"
    else
        echo "❌ Erreur lors de l'exécution de la commande"
        return 1
    fi
}

# Vérifier l'état des services Docker
echo "🐳 Vérification de l'état des services Docker..."
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Les services Docker ne sont pas en cours d'exécution"
    echo "💡 Démarrez les services avec: docker-compose up -d"
    exit 1
fi

echo "✅ Services Docker opérationnels"

# Prévisualisation des tâches qui seront créées
echo "🔍 Prévisualisation des tâches à synchroniser..."
run_django_command "sync_periodic_tasks --dry-run"

echo ""
echo "❓ Voulez-vous continuer et synchroniser ces tâches avec la base de données? (y/N)"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Synchronisation annulée"
    exit 0
fi

# Synchronisation des tâches périodiques
echo "🔄 Synchronisation des tâches périodiques..."
run_django_command "sync_periodic_tasks"

# Vérification des tâches créées
echo "📊 Vérification des tâches créées..."
run_django_command "shell" << 'EOF'
from django_celery_beat.models import PeriodicTask, CrontabSchedule
print(f"📈 Nombre de tâches périodiques: {PeriodicTask.objects.count()}")
print(f"📅 Nombre de planifications crontab: {CrontabSchedule.objects.count()}")
print("\n📋 Tâches périodiques configurées:")
for task in PeriodicTask.objects.all():
    status = "✅ Activée" if task.enabled else "❌ Désactivée"
    print(f"  • {task.name}: {task.task} - {status}")
    if task.crontab:
        print(f"    ⏰ Planification: {task.crontab}")
    if task.args:
        print(f"    📝 Arguments: {task.args}")
EOF

echo ""
echo "🎉 Synchronisation terminée avec succès!"
echo ""
echo "🔗 Liens utiles:"
echo "   • Django Admin: http://localhost:8000/admin/"
echo "   • Section Periodic Tasks: http://localhost:8000/admin/django_celery_beat/periodictask/"
echo "   • Section Crontab Schedules: http://localhost:8000/admin/django_celery_beat/crontabschedule/"
echo ""
echo "💡 Pour démarrer Celery Beat (planificateur de tâches):"
echo "   docker-compose exec web celery -A server_config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"
echo ""
echo "🔧 Commandes utiles:"
echo "   • Voir les tâches: docker-compose exec web python manage.py sync_periodic_tasks --dry-run"
echo "   • Réinitialiser: docker-compose exec web python manage.py sync_periodic_tasks --clear"
echo "   • Logs Celery Worker: docker-compose logs -f celery"
