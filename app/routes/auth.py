from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity,\
                        set_refresh_cookies, create_access_token, create_refresh_token
from app.models import db, User
from datetime import timedelta

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        # Vérifier mot de passe
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
            refresh_token = create_refresh_token(identity=email)

            response = make_response(jsonify({"access_token": access_token}), 200)
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=False,      # ⚠️ en local mets False sinon ton cookie sera bloqué
                samesite="Lax"
            )
            return response
        else:
            return jsonify({"error": "Mot de passe incorrect"}), 401
    else:
        # Créer un nouvel utilisateur
        hashed_pwd = generate_password_hash(password)
        new_user = User(email=email, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=email)

        response = make_response(jsonify({"access_token": access_token, "message": "Utilisateur créé"}), 201)
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=False,    # ⚠️ en local mets False sinon ton cookie sera bloqué
            samesite="Lax"
        )
        return response

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify(access_token=new_access_token), 200