import logging

from celery import Celery
from celery.schedules import crontab
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from config import config
from config import Config

db = SQLAlchemy()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_class=Config):
    app = Flask(__name__)
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'add-every-30-seconds': {
            'task': 'app.test',
            'schedule': 10.0
        },
    }

    app.logger.setLevel(logging.INFO)

    app.config.from_object(config_class)

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    # creates table for models defined in db_models.py if they do not already exist
    with app.app_context():
        db.create_all()

    return app


@celery.task
def test():
    print("Hello!")
