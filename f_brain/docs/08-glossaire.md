# Glossaire

Ce glossaire présente les termes techniques utilisés dans la documentation du projet F_BRAIN. Il est conçu pour aider les lecteurs, qu'ils soient débutants ou expérimentés en DevOps, à comprendre les concepts et technologies mentionnés.

## A

**API (Application Programming Interface)**  
Interface permettant à des applications de communiquer entre elles. Dans F_BRAIN, les API RESTful permettent au frontend de communiquer avec le backend.

**Alpine**  
Distribution Linux légère utilisée comme base pour plusieurs images Docker dans le projet F_BRAIN. Sa taille réduite permet de créer des conteneurs plus petits et plus sécurisés.

**AMQP (Advanced Message Queuing Protocol)**  
Protocole de messagerie standardisé utilisé par RabbitMQ pour la communication entre les services.

**Asynchrone**  
Mode de traitement où une opération est lancée sans attendre sa fin d'exécution, permettant de continuer d'autres tâches en parallèle. Dans F_BRAIN, Celery permet l'exécution asynchrone des tâches.

## B

**Backend**  
Partie serveur de l'application, implémentée avec Django dans F_BRAIN. Gère la logique métier, l'accès aux données et expose des API.

**Base de données**  
Système organisé pour stocker, gérer et récupérer des informations structurées. F_BRAIN utilise PostgreSQL comme système de gestion de base de données relationnelle.

**Bridge Network**  
Type de réseau Docker qui permet à des conteneurs isolés de communiquer entre eux tout en restant isolés des autres réseaux.

**Broker**  
Intermédiaire qui reçoit et achemine les messages. Dans F_BRAIN, RabbitMQ agit comme broker pour les tâches Celery.

## C

**Celery**  
Framework Python pour l'exécution de tâches asynchrones et planifiées. Utilisé dans F_BRAIN pour traiter des opérations en arrière-plan.

**Conteneur**  
Instance légère et exécutable d'une application et de ses dépendances, basée sur une image Docker. Les conteneurs sont isolés mais partagent le même système d'exploitation hôte.

**CI/CD (Continuous Integration/Continuous Deployment)**  
Pratiques DevOps qui automatisent l'intégration du code, les tests et le déploiement. F_BRAIN peut être intégré dans un pipeline CI/CD pour automatiser ces étapes.

**CORS (Cross-Origin Resource Sharing)**  
Mécanisme de sécurité qui permet aux ressources web d'être demandées depuis un domaine différent. Configuré dans le backend Django pour permettre les requêtes du frontend.

## D

**DevOps**  
Culture et pratiques visant à unifier le développement logiciel (Dev) et l'administration des systèmes (Ops). F_BRAIN est conçu selon les principes DevOps.

**Django**  
Framework web Python utilisé pour le backend de F_BRAIN. Il fournit une structure robuste pour le développement d'applications web.

**Docker**  
Plateforme de conteneurisation utilisée pour empaqueter les services F_BRAIN avec leurs dépendances dans des conteneurs isolés.

**Docker Compose**  
Outil pour définir et exécuter des applications multi-conteneurs. Le fichier docker-compose.yml définit l'architecture des services F_BRAIN.

**Dockerfile**  
Script contenant les instructions pour construire une image Docker. Chaque service de F_BRAIN a son propre Dockerfile.

## E

**Endpoint**  
Point de terminaison d'une API, représentant une ressource spécifique accessible via une URL. Le backend Django expose plusieurs endpoints.

**Environment Variables**  
Variables définies dans l'environnement d'exécution et utilisées pour configurer les services. Dans F_BRAIN, elles sont définies dans le fichier .env.

## F

**Frontend**  
Interface utilisateur de l'application, implémentée avec React et Vite dans F_BRAIN. Communique avec le backend via des API.

## G

**Grafana**  
Plateforme de visualisation de données utilisée dans F_BRAIN pour créer des tableaux de bord de monitoring.

## H

**Healthcheck**  
Mécanisme vérifiant périodiquement la santé d'un service. Dans F_BRAIN, les healthchecks sont configurés pour PostgreSQL et RabbitMQ.

**HMR (Hot Module Replacement)**  
Fonctionnalité de développement qui permet de mettre à jour les modules d'une application sans recharger la page. Utilisé dans le frontend avec Vite.

## I

**Image Docker**  
Modèle en lecture seule utilisé pour créer des conteneurs. Contient le système d'exploitation, le code, les dépendances et la configuration.

**Infrastructure as Code (IaC)**  
Pratique consistant à gérer l'infrastructure via du code versionné plutôt que par configuration manuelle. Dans F_BRAIN, Docker Compose est un exemple d'IaC.

## J

**JSON (JavaScript Object Notation)**  
Format léger d'échange de données, principalement utilisé pour la communication entre le frontend et le backend via API.

**JWT (JSON Web Token)**  
Standard ouvert pour créer des jetons d'accès sécurisés. Peut être utilisé pour l'authentification dans le système F_BRAIN.

## K

**Kubernetes**  
Système d'orchestration de conteneurs pour automatiser le déploiement, la mise à l'échelle et la gestion d'applications conteneurisées. Non utilisé par défaut dans F_BRAIN, mais possible évolution future.

## L

**Load Balancing**  
Distribution équilibrée des charges de travail entre plusieurs serveurs. Nginx peut être configuré pour faire du load balancing dans F_BRAIN.

**Logs**  
Enregistrements des événements qui se produisent pendant l'exécution d'un système. Chaque service F_BRAIN génère ses propres logs.

## M

**Microservices**  
Architecture où une application est composée de petits services indépendants communiquant via API. F_BRAIN adopte certains principes de cette architecture.

**Migration (Base de données)**  
Mécanisme pour faire évoluer le schéma de base de données de manière contrôlée. Dans Django, les migrations sont automatiquement générées et appliquées.

**Monitoring**  
Surveillance continue des performances et de la santé des systèmes. F_BRAIN utilise Prometheus et Grafana pour le monitoring.

## N

**Nginx**  
Serveur web performant utilisé comme proxy inverse dans F_BRAIN pour router les requêtes entre le client et les services backend.

**Node.js**  
Environnement d'exécution JavaScript côté serveur, utilisé pour le développement et la construction du frontend F_BRAIN.

## O

**Orchestration**  
Automatisation de la configuration, coordination et gestion des systèmes informatiques complexes. Docker Compose est un outil d'orchestration simple.

## P

**PostgreSQL**  
Système de gestion de base de données relationnelle robuste utilisé par F_BRAIN pour le stockage persistant des données.

**Prometheus**  
Système de monitoring open-source qui collecte et stocke des métriques dans une base de données temporelle, utilisé dans F_BRAIN.

**Proxy**  
Serveur intermédiaire qui transmet les requêtes entre clients et serveurs. Nginx agit comme proxy dans l'architecture F_BRAIN.

**Poetry**  
Outil de gestion des dépendances Python utilisé dans le backend Django pour gérer les packages et leurs versions.

## Q

**Queue (File d'attente)**  
Structure de données qui permet de stocker et traiter des éléments dans un ordre spécifique. RabbitMQ gère des files d'attente de messages pour Celery.

## R

**RabbitMQ**  
Broker de messages implémentant AMQP, utilisé dans F_BRAIN pour la communication entre Django et Celery.

**React**  
Bibliothèque JavaScript pour construire des interfaces utilisateur, utilisée pour le frontend de F_BRAIN.

**REST (Representational State Transfer)**  
Style d'architecture pour systèmes distribués. L'API backend de F_BRAIN suit les principes REST.

**Rollback**  
Processus de retour à un état précédent après un déploiement problématique.

## S

**SSL/TLS**  
Protocoles cryptographiques fournissant des communications sécurisées sur un réseau. Peut être configuré dans Nginx pour sécuriser les communications.

**Static Files**  
Fichiers qui ne changent pas (images, CSS, JavaScript). Dans F_BRAIN, ils sont gérés par Django et servis par Nginx.

## T

**Tâche (Task)**  
Unité de travail à exécuter. Dans F_BRAIN, les tâches asynchrones sont définies et exécutées via Celery.

**Test unitaire**  
Test vérifiant le bon fonctionnement d'une unité de code isolée. Django et React permettent tous deux d'écrire des tests unitaires.

## U

**URL (Uniform Resource Locator)**  
Adresse d'une ressource sur le web. Dans F_BRAIN, les URLs sont configurées dans Django et Nginx.

## V

**Variables d'environnement**  
Variables définies dans l'environnement d'exécution d'un programme. Utilisées dans F_BRAIN pour la configuration des services.

**Vite**  
Outil de build frontend ultrarapide utilisé dans F_BRAIN pour le développement et la construction du client React.

**Volume Docker**  
Mécanisme pour persister des données générées par et utilisées par des conteneurs Docker. F_BRAIN utilise des volumes pour les données PostgreSQL, Prometheus et Grafana.

## W

**Worker**  
Processus qui exécute des tâches. Dans F_BRAIN, les workers Celery traitent les tâches asynchrones.

**WebSocket**  
Protocole de communication bidirectionnelle en temps réel. La configuration Nginx dans F_BRAIN prend en charge les WebSockets pour le HMR du frontend.

## X

**XML (eXtensible Markup Language)**  
Format de données flexible qui peut être utilisé comme alternative à JSON pour l'échange de données.

## Y

**YAML (YAML Ain't Markup Language)**  
Format de sérialisation de données lisible par l'humain. Le fichier docker-compose.yml de F_BRAIN est écrit en YAML.

## Z

**Zero Downtime Deployment**  
Stratégie de déploiement visant à mettre à jour une application sans interruption de service. Peut être implémentée avec des techniques comme le déploiement blue/green.
