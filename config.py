# config.py

import os
from pathlib import Path

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent

# Ensure instance dir exists for SQLite
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

# Default: SQLite in instance folder so it's not committed
# Override with DATABASE_URL for PostgreSQL etc.
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(INSTANCE_DIR / 'transitionos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
