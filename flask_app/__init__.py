from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['API_KEY'] = os.getenv('API_KEY')
    app.config['UPLOAD_PATH'] = os.getenv('UPLOAD_PATH')
    app.config['SESSION_PERMANENT'] = False


    from . import users
    from . import chat

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    migrate.init_app(app, db)

    from flask_app.models import Users
    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)

    app.register_blueprint(users.bp)
    app.register_blueprint(chat.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# export FLASK_APP=run.py
# flask --app run.py db upgrade
# flask run --debug
