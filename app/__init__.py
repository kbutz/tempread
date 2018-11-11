import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from config import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)

    # TODO: add database config
    db_uri = "mysql+pymysql" + "://" + "root" + ":" + "password" + "@" + "192.168.1.3" + ":" + "3307" + "/" + "tempread"

    app.logger.info("DB URI: " + db_uri)

    # Sets default database uri
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_ECHO'] = True  # Logs useful debugging data, defaults to False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Notifies the app of db changes, recommended to leave False

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    # creates table for models defined in db_models.py if they do not already exist
    with app.app_context():
        db.create_all()

    return app
