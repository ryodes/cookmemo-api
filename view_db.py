# view_db.py
from app.extensions import db
from app.models import User, Recipe
from flask import Flask

# Crée une instance Flask pour pouvoir utiliser SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # ajuste si nécessaire
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Utilisation du contexte de l'application
with app.app_context():
    users = User.query.all()
    print("Users dans la base :")
    if users:
        for u in users:
            print(f"id: {u.id}, email: {u.email}, password: {u.password}")
    else:
        print("Aucun user trouvé.")
    # recipe view
    print("weh")
    recipes = Recipe.query.all()
    print("les recettes dans la base :")
    if recipes:
        for u in recipes:
            print(f"id: {u.id}, created by: {u.author_email}, titre: {u.title}")
    else:
        print("Aucun user trouvé.")
