# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions (bound to app in create_app)
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()