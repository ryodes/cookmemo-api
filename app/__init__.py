from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .extensions import db, migrate
from .config import Config
from .routes import auth, user, recipe

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000", "https://cookmemo.vercel.app"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # Initialiser extensions
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # Enregistrer routes (Blueprints)
    app.register_blueprint(auth.bp)
    app.register_blueprint(recipe.bp)
    app.register_blueprint(user.bp)

    return app
