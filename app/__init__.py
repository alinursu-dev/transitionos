# app/__init__.py

from flask import Flask
from config import Config
from app.extensions import db, login, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints when they have routes
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


# So "flask" CLI finds the app when FLASK_APP=app
app = create_app()
