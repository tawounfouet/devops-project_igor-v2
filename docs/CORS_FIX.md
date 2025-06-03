# 🌤️ Weather App - Correction CORS

## Problème résolu ✅

Le frontend ne pouvait pas communiquer avec l'API backend à cause d'un problème de **CORS (Cross-Origin Resource Sharing)**.

### Cause du problème
Le service frontend utilisait l'URL `http://localhost:8000/api/v1` pour accéder à l'API, mais dans l'environnement Docker :
- Le frontend s'exécute dans un conteneur sur le port 4173
- `localhost` dans le conteneur frontend fait référence au conteneur lui-même, pas au backend
- Les requêtes n'atteignaient donc jamais le serveur Django

### Solution implémentée

1. **Configuration de l'URL de l'API** : 
   - Changé de `http://localhost:8000/api/v1` vers `/api/v1` (URL relative)
   - Permet à nginx de router correctement les requêtes vers le backend

2. **Configuration nginx** (déjà en place) :
   ```nginx
   location /api/ {
       proxy_pass http://web:8000;
   }
   ```

3. **Variables d'environnement frontend** :
   - Ajout de `VITE_API_BASE_URL=/api/v1` dans `.env`
   - Configuration flexible pour différents environnements

## Architecture finale

```
Browser → nginx:80 → frontend:4173 (pour /)
       → nginx:80 → web:8000 (pour /api/)
```

## Tests effectués ✅

- ✅ Frontend accessible sur http://localhost
- ✅ API accessible via nginx sur http://localhost/api/v1/
- ✅ Recherche météo fonctionnelle
- ✅ Historique des recherches sauvegardé en base
- ✅ Interface utilisateur opérationnelle
- ✅ Tous les services Docker UP

## Ports configurés

| Service | Port interne | Port externe | Statut |
|---------|-------------|-------------|---------|
| Frontend | 4173 | 4173 | ✅ |
| Backend API | 8000 | 8000 | ✅ |
| Nginx Proxy | 80 | 80 | ✅ |
| PostgreSQL | 5432 | 5435 | ✅ |
| Grafana | 3000 | 3003 | ✅ |
| Prometheus | 9090 | 9090 | ✅ |
| RabbitMQ | 15672 | 15672 | ✅ |

## Utilisation

1. **Accès à l'application** : http://localhost
2. **Test automatique** : `./test-app.sh`
3. **Monitoring** : 
   - Grafana : http://localhost:3003
   - Prometheus : http://localhost:9090
   - RabbitMQ : http://localhost:15672

L'application Weather App est maintenant pleinement fonctionnelle ! 🎉
