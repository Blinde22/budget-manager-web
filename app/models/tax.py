from app import db

class Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    due_day = db.Column(db.Integer, nullable=False)
    last_paid = db.Column(db.Date, nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
    is_recurring = db.Column(db.Boolean, default=False)

