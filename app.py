from flask import Flask, render_template
from dotenv import load_dotenv
import os
import logging

from routes.generate import generate_bp
from routes.posts import posts_bp
from models import db

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(generate_bp)
    app.register_blueprint(posts_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {"status": "running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)