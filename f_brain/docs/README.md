# Documentation Projet DevOps F_BRAIN

## Introduction

Bienvenue dans la documentation complète du projet DevOps F_BRAIN. Ce projet est une application moderne construite selon les principes DevOps, intégrant plusieurs services pour former une solution complète et robuste.

Cette documentation est conçue pour être accessible aux étudiants débutants en DevOps tout en étant suffisamment détaillée pour les professionnels qui souhaiteraient maintenir ou améliorer le projet.

## Table des matières

1. [Présentation générale du projet](./01-presentation-generale.md)
2. [Architecture globale](./02-architecture-globale.md)
3. [Services et composants](./03-services-composants.md)
   - [Frontend (client)](./services/01-frontend.md)
   - [Backend (serveur Django)](./services/02-backend.md)
   - [Proxy (Nginx)](./services/03-proxy-nginx.md)
   - [Base de données (PostgreSQL)](./services/04-base-donnees.md)
   - [File de messages (RabbitMQ)](./services/05-rabbitmq.md)
   - [Tâches asynchrones (Celery)](./services/06-celery.md)
   - [Surveillance et monitoring](./services/07-monitoring.md)
     - [Prometheus](./services/07a-prometheus.md)
     - [Grafana](./services/07b-grafana.md)
4. [Déploiement et configuration](./04-deploiement-configuration.md)
5. [Flux de travail DevOps](./05-flux-travail-devops.md)
6. [Guide de maintenance](./06-guide-maintenance.md)
7. [Bonnes pratiques](./07-bonnes-pratiques.md)
8. [Glossaire](./08-glossaire.md)

## Comment naviguer dans cette documentation

- Commencez par la **Présentation générale** pour comprendre le but et la portée du projet.
- Consultez l'**Architecture globale** pour avoir une vision d'ensemble de l'application.
- Explorez chaque **Service** individuellement pour comprendre ses spécificités.
- Référez-vous au **Guide de maintenance** pour les opérations quotidiennes.
- Utilisez le **Glossaire** pour clarifier les termes techniques utilisés.

## Contribuer à la documentation

Si vous souhaitez contribuer à l'amélioration de cette documentation, veuillez consulter nos consignes de contribution dans le fichier [CONTRIBUTING.md](./CONTRIBUTING.md).
