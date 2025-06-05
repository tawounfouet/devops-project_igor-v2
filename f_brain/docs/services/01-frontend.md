# Frontend (Client)

## Aperçu

Le frontend est la partie visible de l'application F_BRAIN. Il s'agit d'une application web moderne construite avec React.js et utilisant Vite comme bundler et serveur de développement. Ce service est responsable de l'interface utilisateur avec laquelle les utilisateurs interagissent.

## Caractéristiques techniques

- **Langage de programmation** : JavaScript/JSX
- **Framework** : React
- **Bundler/Server** : Vite
- **Image Docker** : Node Alpine
- **Port exposé** : 4173 (via le proxy Nginx)
- **Volumes** : 
  - `./client:/app` - Montage du code source pour le développement
  - `/app/node_modules` - Volume anonyme pour les dépendances Node.js

## Fichiers importants

### Dockerfile

```dockerfile
FROM node:alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install
# Le COPY est remplacé par un volume dans docker-compose.yml
CMD ["yarn", "dev", "--host"]
```

Ce Dockerfile crée un environnement de développement pour le frontend. Il utilise Node.js Alpine comme image de base, installe les dépendances avec Yarn, et lance le serveur de développement Vite avec l'option `--host` qui permet l'accès depuis l'extérieur du conteneur.

### Structure du projet

```
client/
├── Dockerfile
├── eslint.config.js    # Configuration ESLint
├── index.html          # Point d'entrée HTML
├── package.json        # Dépendances et scripts NPM
├── README.md           # Documentation spécifique au frontend
├── vite.config.js      # Configuration de Vite
├── public/             # Fichiers statiques servis tels quels
│   └── vite.svg
└── src/                # Code source de l'application
    ├── App.css         # Styles pour le composant App
    ├── App.jsx         # Composant principal de l'application
    ├── index.css       # Styles globaux
    ├── main.jsx        # Point d'entrée JavaScript
    ├── assets/         # Images, polices et autres ressources
    ├── components/     # Composants React réutilisables
    └── services/       # Services pour l'interaction avec l'API
```

## Configuration dans docker-compose.yml

```yaml
frontend:
  build:
    context: ./client
    dockerfile: Dockerfile
  ports:
    - "4173:4173"
  volumes:
    - ./client:/app
    - /app/node_modules
  networks: [backend]
  environment:
    - NODE_ENV=development
```

Cette configuration dans le docker-compose.yml définit le service frontend. Elle utilise le Dockerfile situé dans le répertoire `./client`, expose le port 4173, monte le code source en tant que volume pour permettre le développement en temps réel, et configure l'environnement de développement.

## Intégration avec le backend

Le frontend communique avec le backend via des appels API REST. Ces requêtes sont acheminées via le proxy Nginx, qui s'occupe de rediriger les requêtes appropriées vers le service backend.

Les communications typiques incluent :
- Requêtes GET pour récupérer des données
- Requêtes POST pour soumettre des formulaires ou créer des ressources
- Requêtes PUT/PATCH pour mettre à jour des ressources
- Requêtes DELETE pour supprimer des ressources

## Mode de développement

En mode développement, le frontend bénéficie de fonctionnalités comme :
- Le Hot Module Replacement (HMR) pour une mise à jour instantanée de l'interface lors des modifications de code
- Des messages d'erreur détaillés dans la console
- Des outils de développement React accessibles via le navigateur

## Bonnes pratiques

1. **Organisation du code** : Suivre une structure de fichiers claire et cohérente
2. **Composants réutilisables** : Créer des composants modulaires et réutilisables
3. **Séparation des préoccupations** : Séparer la logique métier, l'UI et les appels API
4. **Gestion d'état** : Utiliser des solutions appropriées de gestion d'état (Context API, Redux, etc.)
5. **Tests** : Mettre en place des tests unitaires et d'intégration

## Dépannage courant

### Le frontend ne se charge pas
- Vérifier que le conteneur est en cours d'exécution : `docker-compose ps`
- Vérifier les logs : `docker-compose logs frontend`
- S'assurer que le proxy Nginx est correctement configuré

### Les modifications ne sont pas prises en compte
- Vérifier que le volume est correctement monté
- Parfois, redémarrer le conteneur peut être nécessaire : `docker-compose restart frontend`

### Erreurs de connexion avec le backend
- Vérifier la configuration du proxy dans `proxy/default.conf`
- S'assurer que le backend est en cours d'exécution et accessible

## Ressources additionnelles

- [Documentation React](https://reactjs.org/docs)
- [Documentation Vite](https://vitejs.dev/guide/)
- [Guide du développement avec Docker](https://docs.docker.com/develop/)
