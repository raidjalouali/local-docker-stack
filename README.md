# Stack 3-Tiers Conteneurisée (Docker Compose, Nginx, Flask, MySQL)

Petit projet de lab pour déployer, isoler et sécuriser une architecture applicative 3-tiers sous Linux.

## Architecture & Isolation Réseau

La stack se compose de 3 services répartis sur 2 réseaux Docker bridge distincts :

- web (Nginx) : Reverse proxy HTTP exposé sur le port 8080, configuré avec des en-têtes de sécurité (X-Frame, XSS).
- api (Python / Flask) : API REST exécutée sous un utilisateur non-root (appuser).
- db (MySQL 8.0) : Base de données avec stockage persistant (db_data), totalement isolée du web.

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

## Roadmap V2 : Target Architecture Cloud (AWS, Terraform & Kubernetes)

Évolution projetée de la stack pour passer du lab local à un environnement Cloud managé de niveau production :

### 1. Infrastructure as Code (Terraform)
- **VPC Multi-AZ :** Provisionnement d'un VPC avec sous-réseaux publics (ALB) et sous-réseaux privés (EKS Workers, RDS).
- **Services Managés :** Instanciation d'un cluster **AWS EKS** (Elastic Kubernetes Service) et d'une BDD gérée **Amazon RDS MySQL** (avec réplication Multi-AZ).

### 2. Orchestration & Déploiement Kubernetes
- **Conteneurisation Cloud :** Publication des images de l'API Flask sur **AWS ECR** (Elastic Container Registry) après passage réussi de la pipeline CI/CD.
- **Manifests K8s :** Conversion des services Docker Compose en objets Kubernetes (`Deployment` pour Flask, `ClusterIP` pour le service interne).
- **Gestion des Secrets :** Intégration d'**External Secrets Operator (ESO)** synchronisé avec **AWS Secrets Manager** pour proscrire tout secret en clair dans le cluster.

### 3. SecOps, Ingress & Observabilité
- **Routage Externe :** Déploiement d'**AWS ALB Ingress Controller** avec terminaison TLS/SSL automatique via **AWS ACM** (Certificate Manager).
- **Moindre Privilège :** Configuration d'**IRSA** (*IAM Roles for Service Accounts*) pour attribuer des droits AWS granulaires directement aux Pods.
- **Supervision :** Métriques d'infrastructure centralisées sous **CloudWatch** et stack **Prometheus / Grafana** interne au cluster.
