# Directives de contribution

## Introduction

Merci de votre intérêt à contribuer au projet F_BRAIN ! Ce document vise à guider les personnes souhaitant contribuer à l'amélioration de la documentation, du code ou de l'architecture du projet.

## Comment contribuer à la documentation

### Corrections et améliorations

Si vous trouvez des erreurs ou des opportunités d'amélioration dans la documentation existante, vous pouvez :

1. Ouvrir une issue décrivant le problème ou l'amélioration suggérée
2. Soumettre directement une pull request avec les corrections

### Ajouts à la documentation

Pour proposer de nouveaux contenus documentaires :

1. Vérifiez d'abord que le sujet n'est pas déjà couvert
2. Suivez la structure existante et le style rédactionnel
3. Placez les nouveaux fichiers dans les répertoires appropriés
4. Mettez à jour le fichier README.md principal si nécessaire

### Style et format

- Utilisez le français standard sans abréviations
- Suivez le format Markdown avec une syntaxe cohérente
- Utilisez des titres hiérarchiques (# pour les titres principaux, ## pour les sous-titres, etc.)
- Incluez des exemples de code dans des blocs de code avec la syntaxe appropriée
- Pour les diagrammes, utilisez la syntaxe Mermaid

## Comment contribuer au code

### Configuration de l'environnement de développement

1. Clonez le dépôt
2. Installez Docker et Docker Compose
3. Suivez les instructions du document de déploiement pour configurer votre environnement local
4. Vérifiez que tous les tests passent avant de commencer à développer

### Processus de contribution

1. **Fork du projet** - Créez votre propre copie du projet
2. **Créez une branche** - `git checkout -b feature/ma-nouvelle-fonctionnalite`
3. **Développez** - Implémentez votre fonctionnalité ou correction
4. **Testez** - Assurez-vous que tous les tests passent et ajoutez des tests pour votre code
5. **Soumettez une Pull Request** - Décrivez clairement vos changements

### Normes de codage

- **Python (Backend)**
  - Suivez PEP 8
  - Utilisez des docstrings pour documenter les fonctions et classes
  - Maintenez une couverture de tests élevée

- **JavaScript/React (Frontend)**
  - Suivez les normes ESLint configurées
  - Préférez les composants fonctionnels et les hooks
  - Documentez les composants et fonctions complexes

- **Docker**
  - Suivez les meilleures pratiques pour l'optimisation des images
  - Documentez les variables d'environnement

## Processus de revue

Toutes les contributions passeront par un processus de revue :

1. Vérification automatisée par les CI/CD pipelines
2. Revue par un ou plusieurs mainteneurs
3. Feedback et itérations si nécessaire
4. Merge une fois approuvé

## Gestion des issues

### Création d'une issue

- Utilisez un titre clair et descriptif
- Fournissez autant de détails que possible
- Ajoutez des labels appropriés (bug, enhancement, documentation, etc.)
- Incluez des étapes pour reproduire si c'est un bug

### Types d'issues

- **Bug** - Problème dans le code existant
- **Feature** - Nouvelle fonctionnalité
- **Enhancement** - Amélioration d'une fonctionnalité existante
- **Documentation** - Améliorations ou corrections de la documentation

## Communication

- Restez courtois et professionnel dans toutes les communications
- Soyez ouvert aux feedbacks et suggestions
- Posez des questions si quelque chose n'est pas clair

## Licence

En contribuant à ce projet, vous acceptez que vos contributions soient sous la même licence que le projet. Assurez-vous de comprendre les implications avant de contribuer.

## Remerciements

Un grand merci à tous les contributeurs qui aident à améliorer ce projet ! Votre temps et vos efforts sont précieux pour la communauté.
