# config.py

import os
from pathlib import Path
from datetime import timedelta

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent

# Ensure instance dir exists for SQLite
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

# Default: SQLite in instance folder so it's not committed
# Override with DATABASE_URL for PostgreSQL etc.
class Config:
    """Base configuration"""
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-in-production'

    # Database URI (SQLite in instance folder)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(INSTANCE_DIR / 'transitionos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=7)    # "Remember me" for 7 days
    SESSION_COOKIE_SECURE = False    # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True    # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'    # Prevent CSRF attacks
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)    # "Remember me" for 24 hours

    # Security headers
    SESSION_COOKIE_NAME = 'transitionos_session'

    # Receipt uploads (Expense.receipt_path)
    UPLOAD_FOLDER = str(INSTANCE_DIR / 'uploads')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True # Require HTTPS

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'    # In-memory SQLite for testing
    WTF_CSRF_ENABLED = False    # Disable CSRF protection for testing

# Config dictionary for easy selection
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
