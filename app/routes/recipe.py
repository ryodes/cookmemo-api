from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Recipe

bp = Blueprint("recipes", __name__, url_prefix="/recipes")

################ GET ################

@bp.route('/', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.filter_by().all()

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

################ POST ################

@bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    data = request.get_json()

    title = data.get('title')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    image = data.get('image')
    nb_part = data.get('nb_part')

    if not title or not ingredients or not steps:
        return jsonify({"error": "Missing required fields"}), 400

    author_email = get_jwt_identity()

    user = User.query.filter_by(email=author_email).first()
    if not user:
        return jsonify({"error": "Author not found"}), 404

    recipe = Recipe(
        author_email=author_email,
        image=image,
        title=title,
        ingredients=ingredients,
        steps=steps,
        nb_part=nb_part
    )
    db.session.add(recipe)
    db.session.commit()

    return jsonify({
        "message": "Recipe created successfully",
        "recipe": {
            "id": recipe.id,
            "author_email": recipe.author_email,
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "nb_part": recipe.nb_part,
            "image": recipe.image,
            "created_at": recipe.created_at
        }
    }), 201

# curl -X POST http://127.0.0.1:5000/recipes   -H "Content-Type: application/json"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTk2MTMwOSwianRpIjoiNDY1NWQ3NjYtNWEwMS00MThlLWI0ODgtNDUyMmZkZWY5N2NmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImsyYWNpbTMxQGdtYWlsLmNvbSIsIm5iZiI6MTc1OTk2MTMwOSwiY3NyZiI6ImRkYTYzMTk0LTQ0ZTAtNGMwNC05OTcxLTY2OTk1NTFlNDgxMiIsImV4cCI6MTc1OTk2MjIwOX0.JrJYmiZeg8-1JvzSlUUn7NgN7A1vBQHIuGA6gD_l3_s"   -d '{"title": "Test", "ingredients": ["Farine"], "steps": ["Mélanger"]}'
# curl -X GET http://127.0.0.1:5000/recipes   -H "Content-Type: application/json"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDAwNDAxNCwianRpIjoiNGIzZjM0ZDYtMTZmZi00YzkxLTk4MzEtMzk0MjFiYmNiNmZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImsyYWNpbTMxQGdtYWlsLmNvbSIsIm5iZiI6MTc2MDAwNDAxNCwiZXhwIjoxNzYwMDA0OTE0fQ.gfp7UAKgFpinNbG9dgqgBapiaIYgcVBE8m9XhQTtUBQ"
# curl -i -X POST http://127.0.0.1:5000/auth/refresh --cookie "refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTk5OTc0OSwianRpIjoiOWZlY2VjY2MtZGVlNS00ZTgzLTg1ZTktZmY2M2ZkMDE4NDQyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJrMmFjaW0zMUBnbWFpbC5jb20iLCJuYmYiOjE3NTk5OTk3NDksImNzcmYiOiJmY2FlMGY2Yi1kMDk4LTQ2NzktYjlkNC0zMmMxY2VmZGJjZDIiLCJleHAiOjE3NjI1OTE3NDl9.puJ8WsnWtrqFVNcSTNbLDamSvM4OXBzZbSXkibkG7J8"

# {"recipes":[{"author_email":"k2acim31@gmail.com","id":1,"ingredients":["aze","aze"],"steps":["aze"],"title":"aze"},{"author_email":"k2acim31@gmail.com","id":2,"ingredients":["inge1","aze52","aze50"],"steps":["aze489","987"],"title":"nouvelle recette"},{"author_email":"k2acim31@gmail.com","id":3,"ingredients":["aze","aze"],"steps":["azeaze"],"title":"aze"},{"author_email":"k2acim31@gmail.com","id":4,"ingredients":["aze","aze"],"steps":["aze"],"title":"azeazeaze"}]}
