# Local 3-Tier Stack (Docker Compose, Nginx, Flask & MySQL)

Projet de lab local pour le déploiement et l'isolation d'une architecture applicative 3-tiers sous Linux.

## Architecture et isolation réseau

L'infrastructure comprend 3 services répartis sur deux réseaux bridge distincts :

- web (Nginx) : Reverse proxy HTTP (port 8080) réexpédiant le trafic vers l'API.
- api (Python / Flask) : Service applicatif exécuté sous un utilisateur non-root (appuser).
- db (MySQL 8.0) : Base de données avec stockage persistant via un volume Docker (db_data).

Diagramme des flux :

  [ Client ] ---> [ Nginx (8080) ] ---> [ API Flask (5000) ] ---> [ MySQL (3306) ]
                   |_______________________|                   |____________________|
                       frontend_network                           backend_network

Note de sécurité : Le conteneur db est uniquement rattaché au réseau backend_network. Aucun port MySQL n'est publié sur la machine hôte.

## Démarrage rapide

1. Définir les variables d'environnement dans un fichier .env à la racine :

MYSQL_ROOT_PASSWORD=rootsecret
MYSQL_DATABASE=appdb
MYSQL_USER=appuser
MYSQL_PASSWORD=secretpass

2. Lancer la stack :

docker compose up -d --build

3. Tester les endpoints :

curl -i http://localhost:8080/
curl -i http://localhost:8080/db-check

4. Stopper l'environnement :

docker compose down

## Implémentation technique

- Ordonnancement : Utilisation des healthchecks natifs (mysqladmin ping et endpoint HTTP) couplés à `condition: service_healthy` pour s'assurer que l'API n'essaie pas de se connecter à la BDD avant son initialisation complète.
- Sécurité applicative : Exécution de l'API Flask sous un utilisateur dédié sans privilèges (appuser) défini dans le Dockerfile.
- Limites de ressources : Définition de plafonds CPU et mémoire dans docker-compose.yml pour simuler un cadre de contraintes réelles.