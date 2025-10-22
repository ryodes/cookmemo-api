from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author_email = db.Column(
        db.String(120),
        db.ForeignKey('user.email'),
        nullable=False
    )

    author = db.relationship(
        'User',
        backref=db.backref('recipes', lazy=True),
        primaryjoin='Recipe.author_email == User.email'
    )

    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.JSON, nullable=True)
    image = db.Column(db.String(), nullable=False)
    nb_part = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
