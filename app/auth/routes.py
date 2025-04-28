from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print('Username entered:', username)
        print('Password entered:', password)

        user = User.query.filter_by(username=username).first()

        if user:
            print('User found:', user.username)
            print('Stored password hash:', user.password)
        else:
            print('No user found')

        if user and check_password_hash(user.password, password):
            print('Password correct! Logging in...')
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            print('Password incorrect or user missing')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
