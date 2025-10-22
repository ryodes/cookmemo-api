import argparse
from flask import Flask
from app.extensions import db
from app import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def clear_model_data(model_name: str):
    """Vide uniquement la table du modèle donné."""
    with app.app_context():
        # Vérifie si le modèle existe dans app.models
        model_class = getattr(models, model_name, None)
        if model_class is None:
            print(f"❌ Modèle '{model_name}' introuvable dans app.models.")
            return

        # Vide la table correspondante
        table = model_class.__table__
        print(f"🧹 Vidage de la table '{table.name}' associée au modèle '{model_name}'...")
        db.session.execute(table.delete())
        db.session.commit()
        print(f"✅ Table '{table.name}' vidée avec succès !")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vider une table spécifique du modèle Flask.")
    parser.add_argument("-m", "--model", required=True, help="Nom du modèle à vider (ex: Recipe)")
    args = parser.parse_args()

    clear_model_data(args.model)
