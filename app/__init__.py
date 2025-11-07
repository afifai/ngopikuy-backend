from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from .extensions import db, migrate

def create_app():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    

    from config import get_config
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import members, cash, expenses, purchases, summary, export

    app.register_blueprint(members.bp)
    app.register_blueprint(cash.bp, url_prefix="/cash")
    app.register_blueprint(expenses.bp, url_prefix="/expenses")
    app.register_blueprint(purchases.bp, url_prefix="/purchases")
    app.register_blueprint(summary.bp, url_prefix="/summary")
    app.register_blueprint(export.bp, url_prefix="/export")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

from . import models  # noqa
