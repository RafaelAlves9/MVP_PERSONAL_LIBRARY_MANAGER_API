import os
from flask import Flask
from flask_cors import CORS
from app.models.database import db
from app.controllers.livro_controller import BookController
from app.settings.swagger import swagger


def create_app():
    app = Flask(__name__)
    db_path = os.getenv("DATABASE_URL", "sqlite:////app/instance/books.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    swagger.init_app(app)
    BookController.configure_routes(swagger)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
