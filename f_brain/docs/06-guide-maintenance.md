# Guide de maintenance

## Introduction

Ce guide de maintenance fournit les informations essentielles pour entretenir, dépanner et faire évoluer l'application F_BRAIN. Il est conçu pour être utilisé par les administrateurs système, les ingénieurs DevOps et les développeurs responsables du maintien de l'application en état de fonctionnement optimal.

## Maintenance quotidienne

### Vérifications de routine

Il est recommandé d'effectuer les vérifications suivantes quotidiennement :

1. **État des services**
   ```bash
   docker-compose ps
   ```
   Vérifiez que tous les services sont "Up" et fonctionnent correctement.

2. **Utilisation des ressources**
   ```bash
   docker stats
   ```
   Surveillez l'utilisation du CPU, de la mémoire et du réseau par les conteneurs.

3. **Logs d'erreurs**
   ```bash
   docker-compose logs --tail=100 | grep -i error
   ```
   Recherchez les erreurs récentes dans les logs.

4. **Vérification de l'espace disque**
   ```bash
   df -h
   ```
   Assurez-vous qu'il reste suffisamment d'espace disque pour les volumes.

### Nettoyage régulier

Pour éviter l'encombrement des ressources, effectuez régulièrement :

1. **Nettoyage des logs Docker**
   ```bash
   docker-compose logs --no-color | grep -v "prometheus" > logs/docker-$(date +%Y%m%d).log
   docker-compose logs --truncate 0
   ```

2. **Suppression des images inutilisées**
   ```bash
   docker image prune -a --filter "until=24h"
   ```

3. **Suppression des volumes inutilisés**
   ```bash
   docker volume prune
   ```

## Mises à jour

### Mise à jour des services

Pour mettre à jour les services avec les dernières versions :

1. **Mise à jour du code source**
   ```bash
   git pull origin main
   ```

2. **Mise à jour des images Docker**
   ```bash
   docker-compose pull
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Mise à jour de la base de données

Pour appliquer les migrations de base de données :

```bash
docker-compose exec web python manage.py migrate
```

### Mise à jour des dépendances

Pour mettre à jour les dépendances Python :

```bash
docker-compose exec web poetry update
docker-compose exec web poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Pour mettre à jour les dépendances Node.js :

```bash
docker-compose exec frontend yarn upgrade
```

## Sauvegarde et récupération

### Plan de sauvegarde

Implémentez un plan de sauvegarde régulier :

1. **Sauvegarde de la base de données**
   ```bash
   # Sauvegarde quotidienne
   docker-compose exec db pg_dump -U devops_user -d devops_db > backups/db-$(date +%Y%m%d).sql
   ```

2. **Sauvegarde des volumes**
   ```bash
   # Sauvegarde hebdomadaire
   docker run --rm -v f_brain_pgdata:/source -v $(pwd)/backups:/dest ubuntu tar czvf /dest/pgdata-$(date +%Y%m%d).tar.gz /source
   ```

3. **Sauvegarde des configurations**
   ```bash
   # Sauvegarde mensuelle
   cp .env backups/.env-$(date +%Y%m%d)
   cp docker-compose.yml backups/docker-compose-$(date +%Y%m%d).yml
   cp grafana.ini backups/grafana-$(date +%Y%m%d).ini
   cp prometheus.yml backups/prometheus-$(date +%Y%m%d).yml
   ```

### Procédures de restauration

En cas de besoin de restauration :

1. **Restauration de la base de données**
   ```bash
   cat backups/db-20250101.sql | docker-compose exec -T db psql -U devops_user -d devops_db
   ```

2. **Restauration d'un volume**
   ```bash
   docker-compose down
   docker volume rm f_brain_pgdata
   docker volume create f_brain_pgdata
   docker run --rm -v $(pwd)/backups:/source -v f_brain_pgdata:/dest ubuntu tar xzvf /source/pgdata-20250101.tar.gz -C /dest --strip-components=1
   docker-compose up -d
   ```

## Surveillance et monitoring

### Alertes Prometheus/Grafana

Configurez des alertes pour être notifié des problèmes :

1. **Espace disque insuffisant**
2. **Utilisation élevée du CPU/mémoire**
3. **Temps de réponse longs des API**
4. **Taux d'erreurs élevé**
5. **Files d'attente RabbitMQ qui s'allongent**

### Vérification des métriques

Examinez régulièrement les tableaux de bord Grafana pour :

1. **Tendances d'utilisation** - Identifier les pics et les modèles
2. **Performance des requêtes** - Détecter les requêtes lentes
3. **Santé des services** - Vérifier les taux d'erreur et les temps de disponibilité

## Résolution des problèmes courants

### Le service ne démarre pas

1. **Vérifier les logs**
   ```bash
   docker-compose logs [service]
   ```

2. **Vérifier les dépendances**
   ```bash
   docker-compose ps
   ```
   Assurez-vous que les services dont dépend votre service sont fonctionnels.

3. **Vérifier les configurations**
   ```bash
   docker-compose config
   ```
   Vérifiez s'il y a des erreurs de configuration.

### Problèmes de base de données

1. **Vérifier la connectivité**
   ```bash
   docker-compose exec web python manage.py dbshell
   ```

2. **Vérifier les migrations**
   ```bash
   docker-compose exec web python manage.py showmigrations
   ```

3. **Réparer les problèmes de migrations**
   ```bash
   docker-compose exec web python manage.py migrate --fake-initial
   ```

### Problèmes d'authentification

1. **Réinitialiser les crédentiels d'admin Django**
   ```bash
   docker-compose exec web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').update(password='pbkdf2_sha256\$600000\$abcdefghijklmnopqrstuvwxyz\$1234567890abcdefghijklmnopqrstuvwxyz=')"
   ```

2. **Vérifier les variables d'environnement d'authentification**
   ```bash
   docker-compose exec web env | grep -i pass
   ```

### Problèmes de performances

1. **Identifier les goulets d'étranglement**
   ```bash
   docker stats
   ```

2. **Examiner les requêtes SQL lentes**
   ```bash
   docker-compose exec db psql -U devops_user -d devops_db -c "SELECT * FROM pg_stat_activity WHERE state='active' ORDER BY query_start;"
   ```

3. **Vérifier les files d'attente RabbitMQ**
   ```bash
   docker-compose exec rabbitmq rabbitmqctl list_queues
   ```

## Maintenance du code

### Tests automatisés

Exécutez régulièrement la suite de tests pour détecter les régressions :

```bash
docker-compose run --rm web python manage.py test
```

### Analyse de la qualité du code

Utilisez des outils d'analyse statique pour maintenir la qualité du code :

```bash
docker-compose run --rm web flake8
docker-compose run --rm web black --check .
```

## Documentation et procédures

### Mise à jour de la documentation

Maintenez cette documentation à jour en y reflétant tous les changements :

1. Modifications de l'architecture
2. Nouveaux services ajoutés
3. Modifications des procédures de maintenance
4. Nouvelles solutions aux problèmes courants

### Procédures d'urgence

Documentez les procédures pour les situations d'urgence :

1. **Indisponibilité de service** - Étapes pour identifier et résoudre
2. **Corruption de données** - Procédures de restauration
3. **Failles de sécurité** - Protocole d'intervention et de correction

## Maintenance de la sécurité

### Mise à jour des vulnérabilités

Restez informé des vulnérabilités de sécurité et appliquez régulièrement les correctifs :

```bash
# Scanner les vulnérabilités des conteneurs
docker-compose build --no-cache
docker scan $(docker images -q)

# Mettre à jour les dépendances Python avec des correctifs de sécurité
docker-compose exec web poetry update
```

### Audit des accès

Effectuez périodiquement un audit des accès et des permissions :

1. Vérifiez les utilisateurs du système
2. Examinez les journaux d'authentification
3. Révoquez les accès non nécessaires

## Évolution et mise à l'échelle

### Augmentation des ressources

Pour faire face à une charge accrue :

```bash
# Modifier docker-compose.yml pour augmenter les limites de ressources
# Par exemple, pour le service web :
web:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 1G
      reservations:
        cpus: '0.5'
        memory: 512M
```

### Ajout de nouveaux services

Documentez le processus d'ajout de nouveaux services :

1. Créer les fichiers de configuration nécessaires
2. Mettre à jour docker-compose.yml
3. Configurer les connexions avec les services existants
4. Mettre à jour la documentation

## Références utiles

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation React](https://reactjs.org/docs/getting-started.html)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Documentation Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Documentation Grafana](https://grafana.com/docs/)
