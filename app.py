# app.py
import os
from app import create_app
from app.extensions import db
from app.models import User, Expense, Goal

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Flask shell context
@app.shell_context_processor
def make_shell_context():
    """
    Automatically import db and models for Flask shell.
    Usage: flask shell
    """
    return {
        'db': db,
        'User': User,
        'Expense': Expense,
        'Goal': Goal,
    }

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])