from app import create_app, db
from app.models import User  # ou n'importe quelle table

app = create_app()

with app.app_context():
    if not db.inspect(db.engine).has_table("user"):
        db.create_all()

if __name__ == "__main__":
    app.run()
