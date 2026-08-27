# Stack 3-Tiers Conteneurisée (Docker Compose, Nginx, Flask, MySQL)

Petit projet de lab pour déployer, isoler et sécuriser une architecture applicative 3-tiers sous Linux.

## Architecture & Isolation Réseau

La stack se compose de 3 services répartis sur 2 réseaux Docker bridge distincts :

- web (Nginx) : Reverse proxy HTTP exposé sur le port 8080, configuré avec des en-têtes de sécurité (X-Frame, XSS).
- api (Python / Flask) : API REST exécutée sous un utilisateur non-root (appuser).
- db (MySQL 8.0) : Base de données avec stockage persistant (db_data), totalement isolée du web.

### Schéma des flux

[ Client ] ---> [ Nginx:8080 ] ---> [ API Flask:5000 ] ---> [ MySQL:3306 ]
                 |_______________________|                  |____________________|
                     frontend_network                          backend_network

Note de sécurité : La base de données est uniquement connectée au réseau backend_network. Aucun port MySQL n'est publié sur la machine hôte.

## Pipeline CI/CD & DevSecOps (GitHub Actions)

À chaque push ou pull request sur la branche main, le workflow (.github/workflows/ci.yml) valide automatiquement la stack :

1. Scan de secrets : Détection de fuites de mots de passe ou clés avec Gitleaks.
2. Linting : Vérification de la qualité du code Python avec Flake8 et du Dockerfile avec Hadolint.
3. Scan de vulnérabilités : Analyse de l'image Docker de l'API avec Trivy (détection des CVE critiques/hautes).
4. Tests d'intégration : Démarrage temporaire de la stack et validation des endpoints HTTP (/ et /db-check) via curl.

## Démarrage Rapide

### 1. Variables d'environnement
Crée un fichier .env à la racine :

MYSQL_ROOT_PASSWORD=rootsecret
MYSQL_DATABASE=appdb
MYSQL_USER=appuser
MYSQL_PASSWORD=secretpass

### 2. Lancer la stack
Tu peux utiliser Docker Compose directement :

docker compose up -d --build

Ou passer par le Makefile :

make up     # Build et lance les conteneurs
make test   # Teste les endpoints via curl
make clean  # Stoppe tout et nettoie les volumes

### 3. Endpoints disponibles
- http://localhost:8080/ : Statut de l'API.
- http://localhost:8080/health : Healthcheck HTTP de l'API.
- http://localhost:8080/db-check : Test de connexion Flask -> MySQL.

## Bonnes pratiques intégrées

- Non-root user : L'API Flask tourne sous un utilisateur système dédié (appuser) créé dans le Dockerfile.
- Gestion des dépendances : L'API attend l'initialisation complète de MySQL via des healthchecks natifs (mysqladmin ping et condition: service_healthy).
- Limites de ressources : Caps CPU et mémoire définis dans le docker-compose.yml pour chaque service.
