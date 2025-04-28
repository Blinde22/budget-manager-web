from app import db
from flask_login import UserMixin

class Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    due_day = db.Column(db.Integer, nullable=False)  # e.g., 20th of the month
    last_paid = db.Column(db.Date, nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
