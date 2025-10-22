#!/bin/bash

echo "🚀 Initialisation du projet Flask..."

# 1. Créer un environnement virtuel
python3 -m venv venv
source venv/Scripts/activate

# 2. Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Initialiser la base de données avec Flask-Migrate
echo "🗄️ Initialisation de la base de données..."
export FLASK_APP=wsgi.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 4. Lancer l'application
echo "✅ Installation terminée. Lancement de Flask..."
flask run --host=localhost --port=5000
