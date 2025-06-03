# 🌤️ Weather App - Configuration Double Accès

## ✅ Problème résolu : Accès dual frontend

L'application Weather App peut maintenant être accédée de **deux façons différentes** :

### 1. 🎯 Accès direct frontend (Développement)
- **URL** : `http://localhost:4173`
- **Usage** : Accès direct au serveur de développement Vite
- **API** : Utilise `http://localhost:8000/api/v1` (URL absolue)
- **Idéal pour** : Développement frontend, debugging, tests rapides

### 2. 🌐 Accès via proxy nginx (Production-like)
- **URL** : `http://localhost`
- **Usage** : Accès via le reverse proxy nginx
- **API** : Utilise `/api/v1` (URL relative, routée par nginx)
- **Idéal pour** : Tests de production, déploiement, intégration complète

## 🔧 Configuration technique

### Frontend Intelligence (weatherService.js)
```javascript
const getBackendUrl = () => {
  // Si on accède directement au frontend (port 4173), utiliser l'URL absolue
  if (window.location.port === "4173") {
    return "http://localhost:8000/api/v1";
  }
  // Sinon, utiliser l'URL relative pour nginx
  return "/api/v1";
};
```

### Configuration nginx (proxy/default.conf)
```nginx
location /api/ {
    proxy_pass http://web:8000;        # Route vers le backend Django
}

location / {
    proxy_pass http://frontend:4173;   # Route vers le frontend Vite
}
```

### Configuration CORS Django
```python
CORS_ALLOW_ALL_ORIGINS = True  # Permet les requêtes depuis localhost:4173 et localhost
```

## 🚀 Usage

### Développement Frontend
```bash
# Accès direct au frontend avec HMR complet
open http://localhost:4173
```

### Test Production
```bash
# Accès via nginx (simulation production)
open http://localhost
```

### Tests automatiques
```bash
# Test des deux modes d'accès
./test-dual-access.sh

# Test général de l'application
./test-app.sh
```

## 📊 Avantages de cette configuration

### ✅ Flexibilité de développement
- **Port 4173** : Développement frontend rapide avec HMR
- **Port 80** : Test de l'intégration complète avec nginx

### ✅ Consistance API
- Les deux modes accèdent à la même base de données
- L'historique des recherches est partagé
- Les fonctionnalités sont identiques

### ✅ Debugging facilité
- Possibilité de tester les deux configurations
- Isolation des problèmes frontend vs proxy
- CORS configuré pour les deux scénarios

## 🔍 Troubleshooting

### Si port 4173 ne fonctionne pas :
1. Vérifier que le conteneur frontend est démarré
2. Vérifier que le backend répond sur port 8000
3. Vérifier la configuration CORS

### Si port 80 ne fonctionne pas :
1. Vérifier que nginx est démarré
2. Vérifier la configuration proxy nginx
3. Vérifier que frontend et backend sont accessibles par nginx

### Test rapide des services :
```bash
# Frontend direct
curl -s http://localhost:4173 > /dev/null && echo "✅ Frontend OK"

# Backend direct  
curl -s http://localhost:8000/api/v1/history/ | jq length

# Nginx proxy
curl -s http://localhost/api/v1/history/ | jq length
```

## 🎉 Résultat

L'application fonctionne maintenant parfaitement sur **les deux URLs** :
- **http://localhost:4173** - Accès direct développement
- **http://localhost** - Accès via nginx proxy

Les deux modes offrent une expérience utilisateur identique avec accès complet à l'API météo et à l'historique des recherches ! ☀️
