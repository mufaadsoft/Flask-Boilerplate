from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_server():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KDsnvhsVmnuas717'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from app.controllers.home import home
    from app.controllers.auth import auth

    app.register_blueprint(home)
    app.register_blueprint(auth)

    # user model
    from app.models.user import User

    # create database if not exists
    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('instance/'+DB_NAME):
        with app.app_context():
            db.create_all()
