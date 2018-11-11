from datetime import datetime

from flask import current_app

from app import db


class TestModel(db.Model):
    __tablename__ = "test_model"
    id = db.Column(db.Integer, primary_key=True)
    some_value = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            current_app.logger.exception("Error adding test row")

