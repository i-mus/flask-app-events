# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    venue = db.Column(db.String(150))
    location = db.Column(db.String(200))
    booking_url = db.Column(db.String(500))
    ticket_price = db.Column(db.Float)
    category = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Event {self.name}>"