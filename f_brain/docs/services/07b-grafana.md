# Grafana

## Aperçu

Grafana est une plateforme open-source de visualisation et d'analyse de données qui permet de créer des tableaux de bord interactifs et élégants. Dans l'application F_BRAIN, Grafana est utilisé comme interface principale pour visualiser les métriques collectées par Prometheus, offrant ainsi une vision claire et intuitive de la santé et des performances de l'application.

## Caractéristiques techniques

- **Technologie** : Grafana
- **Image Docker** : grafana/grafana:latest
- **Port exposé** : 3003:3000
- **Volumes** : 
  - `./grafana.ini:/etc/grafana/grafana.ini:ro` - Configuration de Grafana
  - `grafana_data:/var/lib/grafana` - Stockage persistant des données
- **Crédentiels par défaut** : admin/admin (configurables via variables d'environnement)

## Configuration dans docker-compose.yml

```yaml
grafana:
  image: grafana/grafana:latest
  env_file: .env
  restart: always
  ports:
    - "3003:3000"
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
```

## Fichier de configuration (grafana.ini)

Le fichier `grafana.ini` définit la configuration de Grafana. Dans le projet F_BRAIN, ce fichier est actuellement vide et doit être configuré selon les besoins spécifiques.

Voici un exemple de configuration de base qui pourrait être utilisée :

```ini
[server]
http_port = 3000
domain = localhost
root_url = %(protocol)s://%(domain)s:%(http_port)s/

[security]
admin_user = admin
admin_password = admin

[auth.anonymous]
enabled = false

[analytics]
reporting_enabled = false
check_for_updates = true

[dashboards]
default_home_dashboard_path = /etc/grafana/provisioning/dashboards/overview.json

[alerting]
enabled = true
```

Cette configuration définit :
1. Les paramètres du serveur web Grafana
2. Les paramètres de sécurité de base
3. La désactivation de l'accès anonyme
4. La désactivation des rapports d'utilisation
5. Le tableau de bord par défaut
6. L'activation des alertes

## Fonctionnalités principales de Grafana

### Sources de données

Grafana peut se connecter à diverses sources de données, dont :
- **Prometheus** - Principale source de données dans F_BRAIN
- **PostgreSQL** - Peut être utilisé pour des requêtes directes sur la base de données
- **Loki** - Pour les logs (non configuré par défaut)
- **Alertmanager** - Pour les alertes Prometheus

### Tableaux de bord

Les tableaux de bord Grafana sont composés de panneaux configurables qui affichent des visualisations de données :
1. **Graphiques** - Pour visualiser des séries temporelles
2. **Jauges** - Pour afficher des valeurs uniques avec des seuils
3. **Tableaux** - Pour présenter des données tabulaires
4. **Statistiques** - Pour afficher des chiffres clés
5. **Cartes thermiques** - Pour visualiser la distribution des valeurs

### Exemples de tableaux de bord

#### Tableau de bord système

Un tableau de bord pour surveiller les métriques système des conteneurs :
- Utilisation CPU par service
- Consommation mémoire par service
- Utilisation disque
- Trafic réseau

#### Tableau de bord application Django

Un tableau de bord pour surveiller les performances de l'application Django :
- Requêtes par seconde
- Temps de réponse moyen, médian, 95e percentile
- Taux d'erreurs HTTP
- Utilisation de la base de données

#### Tableau de bord base de données

Un tableau de bord pour surveiller PostgreSQL :
- Connexions actives
- Taux de transactions
- Temps de requête
- Cache hit ratio
- Croissance des tables

#### Tableau de bord RabbitMQ

Un tableau de bord pour surveiller la messagerie :
- État des files d'attente
- Taux de messages entrants/sortants
- Latence des messages
- Consommateurs actifs

### Alertes

Grafana permet de configurer des alertes basées sur les données visualisées :
1. **Règles d'alerte** - Conditions qui déclenchent les alertes
2. **Canaux de notification** - Destinations des alertes (email, Slack, etc.)
3. **Silences et inhibitions** - Règles pour éviter les alertes redondantes

## Provisionnement automatique

Pour une approche "configuration as code", Grafana permet le provisionnement automatique des tableaux de bord et des sources de données :

```
/etc/grafana/provisioning/
├── dashboards/
│   ├── dashboard.yml
│   └── overview.json
└── datasources/
    └── prometheus.yml
```

Exemple de configuration pour le provisionnement des sources de données :

```yaml
# prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## Bonnes pratiques

1. **Organisation des tableaux de bord** - Structurer les tableaux de bord par domaine fonctionnel
2. **Templating** - Utiliser des variables pour rendre les tableaux de bord dynamiques
3. **Annotations** - Marquer les événements importants (déploiements, incidents)
4. **Seuils visuels** - Utiliser des couleurs et des seuils pour identifier rapidement les anomalies
5. **Configuration as code** - Gérer les tableaux de bord dans le dépôt Git

## Dépannage courant

### Grafana ne démarre pas
- Vérifier les logs : `docker-compose logs grafana`
- S'assurer que le volume grafana_data a les bonnes permissions
- Vérifier la configuration dans grafana.ini

### Problèmes de connexion aux sources de données
- Vérifier que Prometheus est accessible depuis le conteneur Grafana
- Contrôler les URL et identifiants configurés
- Vérifier les logs pour des erreurs de connexion

### Tableaux de bord vides ou incomplets
- S'assurer que les métriques sont correctement collectées par Prometheus
- Vérifier les requêtes PromQL dans les panneaux
- Ajuster la plage temporelle d'affichage

## Ressources additionnelles

- [Documentation Grafana](https://grafana.com/docs/grafana/latest/)
- [Galerie de tableaux de bord](https://grafana.com/grafana/dashboards/)
- [Guide d'utilisation de Prometheus avec Grafana](https://prometheus.io/docs/visualization/grafana/)
- [Grafana Play](https://play.grafana.org/) - Environnement de démonstration en ligne
