from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models.tax import Tax

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = 'ultrasecretkey1312'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from app.routes import main
    from app.auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
