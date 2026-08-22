# Stack web locale conteneurisée (Docker Compose, Nginx, Flask & MySQL)

Projet personnel de mise en place d'une architecture 3-tiers conteneurisée sous Linux. L'objectif est de manipuler l'isolation réseau, la persistance de données et l'automatisation du déploiement via une chaîne CI/CD simple.

## Architecture

L'application est découpée en 3 conteneurs distincts :
- web (Nginx) : Reverse proxy recevant le trafic HTTP sur le port 8080 et le transférant à l'API.
- api (Python / Flask) : Traite les requêtes applicatives et s'exécute sous un utilisateur non-root (appuser).
- db (MySQL 8.0) : Stocke les données de manière persistante sur un volume Docker.

### Réseaux virtuels
- frontend_network : Liaison Nginx <-> API Flask.
- backend_network : Liaison API Flask <-> MySQL (Réseau privé isolé, la BDD n'a aucun port exposé sur l'hôte).

## Structure du projet

.
├── .github/workflows/ci.yml  # Pipeline GitHub Actions (build & tests curl)
├── app/                      # Code source Flask et Dockerfile
├── nginx/                    # Configuration du reverse proxy
├── .env                      # Variables d'environnement (exclu de Git)
├── docker-compose.yml        # Orchestration multi-conteneurs
└── README.md

## Démarrage rapide

### Prérequis
Docker Engine et Docker Compose V2 installés.

1. Créer le fichier d'environnement .env à la racine :
MYSQL_ROOT_PASSWORD=rootsecret
MYSQL_DATABASE=appdb
MYSQL_USER=appuser
MYSQL_PASSWORD=secretpass

2. Lancer l'infrastructure :
docker compose up -d --build

3. Vérifier les endpoints :
curl -i http://localhost:8080/
curl -i http://localhost:8080/db-check

4. Stopper l'environnement :
docker compose down
