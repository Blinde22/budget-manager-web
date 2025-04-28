from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app import db
from app.models.budget_item import BudgetItem
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    filter_type = request.args.get('type')
    filter_month = request.args.get('month')
    filter_category = request.args.get('category')

    query = BudgetItem.query.filter_by(user_id=current_user.id)

    if filter_type == 'income':
        query = query.filter_by(is_income=True)
    elif filter_type == 'expense':
        query = query.filter_by(is_income=False)

    if filter_month:
        try:
            month = int(filter_month)
            query = query.filter(db.extract('month', BudgetItem.date_added) == month)
        except:
            pass

    if filter_category:
        query = query.filter_by(category=filter_category)

    items = query.all()
    balance = calculate_balance(items)

    return render_template('index.html', items=items, balance=balance)

def calculate_balance(items):
    balance = 0
    for item in items:
        if item.is_income:
            balance += item.amount
        else:
            balance -= item.amount
    return balance
