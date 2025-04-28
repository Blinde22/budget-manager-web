from app import db

class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    is_income = db.Column(db.Boolean)
    is_recurring = db.Column(db.Boolean)
    emoji = db.Column(db.String(10))
    date_added = db.Column(db.Date)
