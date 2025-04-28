from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from app import db
from app.models.budget_item import BudgetItem
from datetime import datetime
from app.models.tax import Tax
from datetime import date
from app.models.category import Category


main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    handle_recurring_items()
    
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

@main.route('/summary')
@login_required
def summary():
    items = BudgetItem.query.filter_by(user_id=current_user.id).all()

    total_income = sum(item.amount for item in items if item.is_income)
    total_expense = sum(item.amount for item in items if not item.is_income)
    balance = total_income - total_expense

    if total_income > 0:
        savings_rate = (balance / total_income) * 100
    else:
        savings_rate = 0

    return render_template(
        'summary.html',
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        savings_rate=savings_rate
    )


@main.route('/taxes', methods=['GET', 'POST'])
@login_required
def taxes():
    if request.method == 'POST':
        name = request.form.get('name')
        due_day = int(request.form.get('due_day'))
        new_tax = Tax(user_id=current_user.id, name=name, due_day=due_day)
        db.session.add(new_tax)
        db.session.commit()
        return redirect(url_for('main.taxes'))

    taxes = Tax.query.filter_by(user_id=current_user.id).all()
    today = date.today()

    return render_template('taxes.html', taxes=taxes, today=today)

@main.route('/pay_tax/<int:tax_id>')
@login_required
def pay_tax(tax_id):
    tax = Tax.query.get(tax_id)
    if tax and tax.user_id == current_user.id:
        tax.is_paid = True
        tax.last_paid = date.today()
        db.session.commit()
    return redirect(url_for('main.taxes'))

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    categories = Category.query.all()

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
            date_added=datetime.today()
        )
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add_item.html', categories=categories)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

