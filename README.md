# papernest-test

API pour vérifier la couverture réseau 2G/3G/4G des opérateurs français sur différentes adresses.

## Architecture

- **Backend**: Django avec Django REST Framework et Swagger
- **Frontend**: Next.js 
- **Base de données**: Données CSV incluse l'app (dossier data/)
- **Déploiement**: Docker Compose

##  Prérequis

- Python 3.13.2
- Node.js 22.8.0
- Docker et Docker Compose (optionnel)
- Git

## Démarrage rapide avec Docker

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd papernest-test
```

### 2. Lancer l'application avec Docker Compose

```bash
docker-compose up -d --build
```

### Rebuild complet

```bash
# Supprimer tout et reconstruire
docker-compose down -v
docker system prune -f
docker-compose up --build
```


### 3. Accéder aux services

- **Frontend Next.js**: http://localhost:3000
- **Backend Django**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/swagger/

### 4. Arrêter les services

```bash
docker-compose down
```

##  Démarrage sans Docker

### Backend (Django)

```bash
# Se placer dans le dossier backend
cd backend/test_papernest

# Créer un environnement virtuel
python -m venv papernest_env

# Activer l'environnement virtuel
# Sur Windows
papernest_env\Scripts\activate
# Sur Linux/Mac
source papernest_env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Effectuer les migrations
python manage.py migrate

# Démarrer le serveur de développement
python manage.py runserver 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
# Ouvrir un nouveau terminal et se placer dans le dossier frontend
cd frontend/coverage-app

# Installer les dépendances
pnpm install

# Démarrer le serveur de développement
pnpm run dev
```

## Utilisation de l'API

### Via l'interface web (Next.js)

1. Ouvrir http://localhost:3000
2. importer un fichier json comportant les adresses
3. Cliquer sur "Vérifier la couverture"
4. Consulter les résultats 

### Via l'API directement

#### Swagger UI
- Accéder à http://localhost:8000/swagger/
- Tester les endpoints directement dans l'interface

## Tests

### Tests backend

```bash
cd backend/test_papernest

# Avec l'environnement virtuel activé
python manage.py test

Note: Les tests sont également exécutés automatiquement lors d'un push via GitHub Actions (voir .github/workflows/).

```

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de données (si utilisée)
DATABASE_URL=sqlite:///db.sqlite3

# API externe
ADRESSE_API_URL=https://api-adresse.data.gouv.fr

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:8000
```


