from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity,\
                        set_refresh_cookies, create_access_token, create_refresh_token
from app.models import db, User
from datetime import timedelta
import os

IS_PROD = os.getenv("FLASK_ENV") == "production"

def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=os.getenv("SECURE_ENV", "False").lower() == "true",
        samesite=os.getenv("SAMESITE_ENV", "Lax"),
    )

bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- LOGIN ---
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Identifiants incorrects"}), 401

    access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(identity=email)

    response = make_response(jsonify({"access_token": access_token}), 200)
    set_refresh_cookie(response, refresh_token)
    return response

# --- REGISTER ---
@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Cet utilisateur existe déjà."}), 409

    hashed_pwd = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(identity=email)

    response = make_response(jsonify({"access_token": access_token, "message": "Utilisateur créé"}), 201)
    set_refresh_cookie(response, refresh_token)
    return response

# --- REFRESH TOKEN ---
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify(access_token=new_access_token), 200