import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from config import config
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)

    app.config.from_object(config_class)

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    # creates table for models defined in db_models.py if they do not already exist
    with app.app_context():
        db.create_all()

    return app
