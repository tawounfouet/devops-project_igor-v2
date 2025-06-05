# Proxy (Nginx)

## Aperçu

Le proxy Nginx agit comme point d'entrée principal de l'application F_BRAIN. Il est responsable du routage des requêtes HTTP entre le frontend et le backend, de la gestion des requêtes WebSocket, et potentiellement de la terminaison SSL. Ce service fournit une abstraction aux clients, permettant à l'architecture sous-jacente de changer sans impact sur les URL publiques.

## Caractéristiques techniques

- **Technologie** : Nginx
- **Image Docker** : Nginx Alpine (légère)
- **Ports exposés** : 80, 443
- **Volumes** : `./proxy/default.conf:/etc/nginx/conf.d/default.conf` - Configuration Nginx

## Fichiers importants

### Dockerfile

```dockerfile
FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
```

Ce Dockerfile simple utilise l'image officielle Nginx Alpine et y ajoute le fichier de configuration personnalisé.

### Configuration Nginx (default.conf)

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://frontend:4173;   # frontend service on port 4173
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for HMR
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /api/ {
        proxy_pass http://web:8000;        # backend API service
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Cette configuration Nginx définit deux règles principales :
1. Les requêtes vers la racine (`/`) sont transmises au service frontend.
2. Les requêtes vers `/api/` sont transmises au service backend.

Des en-têtes supplémentaires sont définis pour préserver les informations du client d'origine lors du proxying, et le support WebSocket est activé pour permettre le Hot Module Replacement (HMR) en développement.

## Configuration dans docker-compose.yml

```yaml
nginx:
  build:
    context: ./proxy
    dockerfile: Dockerfile
  restart: unless-stopped
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./proxy/default.conf:/etc/nginx/conf.d/default.conf
  networks: [backend]
  depends_on:
    - frontend
    - web
```

Cette configuration dans docker-compose.yml définit le service proxy. Elle utilise le Dockerfile du répertoire `./proxy`, expose les ports HTTP (80) et HTTPS (443), monte le fichier de configuration en tant que volume pour permettre des mises à jour sans reconstruire l'image, et spécifie les dépendances sur les services frontend et backend.

## Rôle dans l'architecture

Le proxy Nginx joue plusieurs rôles clés dans l'architecture de F_BRAIN :

1. **Point d'entrée unique** - Il fournit un point d'accès unifié à l'application.
2. **Routage des requêtes** - Il route les requêtes vers les services appropriés selon leur URL.
3. **Terminaison SSL** - Il peut gérer les certificats SSL et le chiffrement HTTPS (non configuré par défaut).
4. **Protection de base** - Il fournit une couche d'isolation entre Internet et les services internes.
5. **Support WebSocket** - Il gère les connexions WebSocket pour le HMR et d'autres fonctionnalités en temps réel.
6. **Caching** - Il peut mettre en cache certaines réponses pour améliorer les performances (non configuré par défaut).

## Configurations avancées (optionnelles)

### Mise en place de HTTPS

Pour activer HTTPS, il faudrait :
1. Obtenir des certificats SSL (Let's Encrypt ou autre)
2. Modifier la configuration pour écouter sur le port 443
3. Configurer la redirection HTTP vers HTTPS

Exemple de configuration HTTPS :

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # Reste de la configuration...
}
```

### Mise en cache

Pour améliorer les performances, on peut configurer le cache Nginx :

```nginx
proxy_cache_path /tmp/cache levels=1:2 keys_zone=cache:10m max_size=500m inactive=60m;

server {
    # ...
    
    location /static/ {
        proxy_pass http://frontend:4173;
        proxy_cache cache;
        proxy_cache_valid 200 1d;
        add_header X-Proxy-Cache $upstream_cache_status;
    }
}
```

## Bonnes pratiques

1. **Sécurité** - Limiter les informations exposées dans les en-têtes de réponse
2. **Configuration modulaire** - Diviser la configuration en fichiers séparés pour une meilleure lisibilité
3. **Tests** - Valider la configuration avant le déploiement avec `nginx -t`
4. **Logging** - Configurer des logs appropriés pour le débogage
5. **Rate limiting** - Protéger contre les abus avec des limites de taux de requêtes

## Dépannage courant

### Erreur 502 Bad Gateway
- Vérifier que les services backend et frontend sont en cours d'exécution
- Vérifier les noms d'hôte et ports dans la configuration

### Problèmes WebSocket
- S'assurer que les en-têtes Upgrade et Connection sont correctement configurés
- Vérifier les logs Nginx pour des erreurs spécifiques

### Problèmes de performance
- Surveiller l'utilisation des ressources du conteneur Nginx
- Considérer l'activation du cache pour le contenu statique
- Optimiser les worker_processes et worker_connections

## Ressources additionnelles

- [Documentation officielle Nginx](https://nginx.org/en/docs/)
- [Guide Nginx pour Docker](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-docker/)
- [Modèles de configuration Nginx](https://www.nginx.com/resources/wiki/start/topics/examples/full/)
