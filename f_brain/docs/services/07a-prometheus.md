# Prometheus

## Aperçu

Prometheus est un système de monitoring et d'alerte open-source développé à l'origine par SoundCloud. Dans l'application F_BRAIN, Prometheus est utilisé comme système central de collecte et de stockage de métriques. Il collecte des données de surveillance en temps réel à partir de cibles configurées via HTTP, stocke ces données localement et les expose pour interrogation via son langage de requête PromQL.

## Caractéristiques techniques

- **Technologie** : Prometheus
- **Image Docker** : prom/prometheus:latest
- **Port exposé** : 9090
- **Volumes** : 
  - `./prometheus.yml:/etc/prometheus/prometheus.yml:ro` - Configuration de Prometheus
  - `prometheus_data:/prometheus` - Stockage persistant des données
- **Healthcheck** : Vérification périodique de la disponibilité avec un ping à l'endpoint de santé

## Configuration dans docker-compose.yml

```yaml
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus_data:/prometheus
  networks: [backend]
  healthcheck:
    test: ["CMD-SHELL", "wget --spider http://localhost:9090/-/ready"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## Fichier de configuration (prometheus.yml)

Le fichier `prometheus.yml` définit la configuration de Prometheus, notamment les cibles à surveiller et les règles de scraping. Dans le projet F_BRAIN, ce fichier est actuellement vide et doit être configuré selon les besoins spécifiques.

Voici un exemple de configuration de base qui pourrait être utilisée :

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'django'
    static_configs:
      - targets: ['web:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['rabbitmq:15692']
    metrics_path: '/metrics'

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']
```

Cette configuration définit :
1. La fréquence de collecte globale (toutes les 15 secondes)
2. L'auto-surveillance de Prometheus
3. La collecte des métriques du serveur Django (nécessite un exporteur de métriques Django)
4. La collecte des métriques PostgreSQL (nécessite postgres-exporter)
5. La collecte des métriques RabbitMQ (nécessite l'activation du plugin Prometheus dans RabbitMQ)
6. La collecte des métriques Nginx (nécessite nginx-exporter)

## Principaux concepts de Prometheus

### Métriques et types de données

Prometheus collecte des métriques qui sont simplement des mesures numériques horodatées. Les principaux types de métriques sont :

1. **Counter** - Valeur numérique qui ne peut qu'augmenter (ex: nombre total de requêtes)
2. **Gauge** - Valeur numérique qui peut augmenter et diminuer (ex: utilisation mémoire)
3. **Histogram** - Échantillonnage des observations et comptage par buckets configurables (ex: temps de réponse)
4. **Summary** - Similaire à l'histogramme, mais calcule des quantiles côté client

### Labels et dimensions

Les métriques Prometheus peuvent être associées à des labels qui ajoutent des dimensions aux données :

```
http_requests_total{method="POST", endpoint="/api/users"}
```

### PromQL

PromQL est le langage de requête de Prometheus qui permet d'interroger et d'agréger les données de métriques. Exemples :

```
# Taux de requêtes HTTP par seconde sur 5 minutes
rate(http_requests_total[5m])

# 95ème percentile du temps de réponse
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

## Interface web Prometheus

L'interface web de Prometheus est accessible à l'adresse http://localhost:9090 et offre plusieurs fonctionnalités :

1. **Explorateur de métriques** - Pour parcourir les métriques disponibles
2. **Éditeur de requêtes** - Pour écrire et exécuter des requêtes PromQL
3. **Graphiques** - Pour visualiser les résultats sous forme de graphiques
4. **Status** - Pour vérifier l'état de Prometheus et ses cibles configurées
5. **Alertes** - Pour visualiser les alertes actives (si configurées)

## Exporteurs de métriques

Pour collecter des métriques à partir des différents services, des exporteurs peuvent être nécessaires :

1. **Django** - Utiliser [django-prometheus](https://github.com/korfuri/django-prometheus) ou similaire
2. **PostgreSQL** - Utiliser [postgres_exporter](https://github.com/prometheus-community/postgres_exporter)
3. **RabbitMQ** - Activer le plugin Prometheus dans RabbitMQ
4. **Nginx** - Utiliser [nginx-prometheus-exporter](https://github.com/nginxinc/nginx-prometheus-exporter)

## Alertes (configuration avancée)

Prometheus peut être configuré pour générer des alertes basées sur des conditions définies. Ces alertes sont ensuite envoyées à Alertmanager qui gère leur routage, regroupement et envoi aux destinataires finaux (email, Slack, etc.).

Exemple de configuration d'alertes :

```yaml
# Dans prometheus.yml
rule_files:
  - 'alert.rules'

alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093
```

Et dans `alert.rules` :

```yaml
groups:
- name: example
  rules:
  - alert: HighLatency
    expr: avg_over_time(api_request_duration_seconds[5m]) > 1
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High request latency"
      description: "API latency is above 1 second for more than 10 minutes."
```

## Bonnes pratiques

1. **Nommage cohérent** - Adopter une convention de nommage claire pour les métriques
2. **Labels utiles** - Utiliser des labels pertinents sans en abuser (cardinality explosion)
3. **Rétention adaptée** - Configurer la rétention des données selon les besoins réels
4. **Alertes actionables** - Ne configurer des alertes que pour des conditions qui nécessitent une intervention
5. **Documentation** - Documenter les métriques personnalisées et leur signification

## Dépannage courant

### Prometheus ne collecte pas certaines métriques
- Vérifier que les cibles sont configurées correctement dans prometheus.yml
- S'assurer que les exporteurs sont en cours d'exécution
- Vérifier les erreurs de scraping dans l'interface web (Status > Targets)

### Problèmes de performances
- Optimiser la fréquence de scraping pour les cibles volumineuses
- Limiter le nombre de séries temporelles collectées
- Augmenter les ressources allouées au conteneur Prometheus

### Problèmes de stockage
- Surveiller l'utilisation du volume prometheus_data
- Ajuster la durée de rétention des données si nécessaire

## Ressources additionnelles

- [Documentation Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Guide PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Alerting avec Prometheus](https://prometheus.io/docs/alerting/latest/overview/)
- [Exporteurs officiels](https://prometheus.io/docs/instrumenting/exporters/)
