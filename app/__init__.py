# app/__init__.py
from flask import Flask
from config import config
from app.extensions import db, login_manager
from app.models import User

def create_app(config_name='development'):
    """
    Flask application factory.
    Creates and configures the Flask application with all extensions and blueprints.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = 'auth.login' # Redirect to login page if user is not logged in
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login user loader callback.
        Returns User object for the given user_id in session.
        """
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/')

    from app.expenses import expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


