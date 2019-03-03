from datetime import datetime

from flask import current_app

from app import db


class TemperatureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    temp_in_f = db.Column(db.Float())

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            current_app.logger.exception("Error adding temp reading row")

