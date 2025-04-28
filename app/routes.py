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


def handle_recurring_items():
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    existing_dates = db.session.query(BudgetItem.date_added).filter(
        BudgetItem.user_id == current_user.id,
        BudgetItem.is_recurring == True
    ).all()

    existing_dates = {d[0].month for d in existing_dates if d[0].year == current_year}

    if current_month not in existing_dates:
        recurring_items = BudgetItem.query.filter_by(user_id=current_user.id, is_recurring=True).all()
        for item in recurring_items:
            new_item = BudgetItem(
                user_id=item.user_id,
                name=item.name,
                amount=item.amount,
                category=item.category,
                is_income=item.is_income,
                is_recurring=True,
                emoji=item.emoji,
                date_added=today
            )
            db.session.add(new_item)
        db.session.commit()
