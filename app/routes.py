from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.budget_item import BudgetItem
from datetime import date

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    items = BudgetItem.query.filter_by(user_id=current_user.id).all()
    balance = calculate_balance(items)
    return render_template('index.html', items=items, balance=balance)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        is_income = request.form.get('is_income') == 'on'
        is_recurring = request.form.get('is_recurring') == 'on'
        emoji = request.form.get('emoji')

        new_item = BudgetItem(
            user_id=current_user.id,
            name=name,
            amount=amount,
            category=category,
            is_income=is_income,
            is_recurring=is_recurring,
            emoji=emoji,
            date_added=date.today()
        )
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add_item.html')

def calculate_balance(items):
    balance = 0
    for item in items:
        if item.is_income:
            balance += item.amount
        else:
            balance -= item.amount
    return balance
