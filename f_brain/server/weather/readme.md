

# Conversion de l'API WeatherSearch de DRF à Django pur

Les principales modifications apportées :

1. **Suppression des imports DRF** : Plus besoin de rest_framework, api_view, Response, etc.

2. **Utilisation de JsonResponse** : Remplace Response de DRF pour retourner des réponses JSON.

3. **Décorateurs Django natifs** :
    - `@require_http_methods(["GET"])` remplace `@api_view(["GET"])`

4. Accès aux paramètres :
    - `request.GET.get()` remplace `request.query_params.get()`

5. **Sérialisation manuelle** :
    - Transformation manuelle des objets WeatherSearch en dictionnaires Python au lieu d'utiliser les serializers DRF

6. **Gestion des erreurs** :
    - Utilisation des codes de `statut HTTP` directement avec JsonResponse

7. **Safe parameter** :
    - Ajout de `safe=False` pour retourner des listes dans JsonResponse, car par défaut, JsonResponse n'autorise pas les listes comme réponse.

Cette implémentation conserve exactement la même fonctionnalité que la version DRF mais utilise uniquement Django pur.