🚀 Flask Backend Template
Ce dépôt fournit une structure de base robuste et modulaire pour démarrer rapidement vos projets backend avec Flask. Il suit les meilleures pratiques, notamment l'utilisation du design pattern "Application Factory" et la séparation des responsabilités.

📁 Structure du Projet
Plaintext

backend/
├── app/
│   ├── routes/          # Blueprints pour les points de terminaison API
│   ├── static/          # Fichiers statiques (si nécessaire)
│   ├── utils/           # Fonctions d'aide et décorateurs
│   ├── extensions.py    # Initialisation des extensions (SQLAlchemy, etc.)
│   ├── models.py        # Définition des modèles de base de données
│   └── __init__.py      # Coeur de l'application (Factory)
├── config.py            # Configuration des environnements
├── requirements.txt     # Dépendances du projet
├── .env                 # Variables d'environnement (non suivi par git)
└── run.py               # Point d'entrée pour lancer le serveur
🛠️ Guide de démarrage rapide
Suivez ces étapes pour configurer et lancer votre environnement de développement.

1. Cloner le projet
Bash

git clone https://github.com/Ibrah2278/flask_backend_template.git
cd votre-repo/backend
2. Créer l'environnement virtuel
Il est fortement recommandé d'utiliser un environnement virtuel pour isoler vos dépendances.

Sur Windows :

Bash

python -m venv venv
.\venv\Scripts\activate
Sur macOS/Linux :

Bash

python3 -m venv venv
source venv/bin/activate
3. Installer les dépendances
Bash

pip install -r requirements.txt
4. Configurer les variables d'environnement
Créez un fichier .env à la racine du dossier backend et ajoutez-y :

Plaintext

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_ici
DATABASE_URL=sqlite:///app.db
💡 Exemple : Implémenter une logique de Login
Pour tester votre structure, voici comment ajouter un modèle utilisateur et une route de connexion.

Étape A : Définir le modèle (app/models.py)
Python

from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
Étape B : Créer la route de login (app/routes/auth.py)
Créez un fichier dans le dossier routes :

Python

from flask import Blueprint, request, jsonify
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Logique simplifiée pour l'exemple
    if data.get('username') == "admin" and data.get('password') == "password":
        return jsonify({"message": "Connexion réussie", "token": "votre-jwt-ici"}), 200
    return jsonify({"error": "Identifiants invalides"}), 401
Étape C : Enregistrer le Blueprint (app/__init__.py)
N'oubliez pas d'enregistrer votre nouveau module dans la factory :

Python

from .routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
🚀 Lancement et Test
1. Lancer le serveur
Bash

flask run
Le serveur sera disponible sur http://127.0.0.1:5000.

2. Tester le point de terminaison
Vous pouvez utiliser Postman, Insomnia ou curl pour tester le login :

Bash

curl -X POST http://127.0.0.1:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
✨ Prochaines étapes
[ ] Configurer les migrations avec Flask-Migrate.

[ ] Ajouter la gestion des JWT avec Flask-JWT-Extended.

[ ] Créer des tests unitaires dans un dossier /tests.