from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Recipe

bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email} for u in users])

@bp.route("/recipes", methods=["GET"])
@jwt_required()
def get_recipes():
    user_email = get_jwt_identity()

    recipes = Recipe.query.filter_by(author_email=user_email).all()

    recipes_list = [
        {
            "id": r.id,
            "title": r.title,
            "ingredients": r.ingredients,
            "steps": r.steps,
            "image": r.image,
            "author_email": r.author_email,
            "nb_part": r.nb_part,
            "created_at": r.created_at,
        }
        for r in recipes
    ]

    return jsonify({"recipes": recipes_list}), 200