# app/expenses/routes.py

from flask import render_template
from flask_login import login_required

from app.expenses import expenses_bp

@expenses_bp.route("/")
@login_required
def list():
    """
    Expenses list - placeholder for now.
    Only accessible to authenticated users.
    """
    return "<h1>Expenses List (Coming Soon)</h1>"

@expenses_bp.route("/simulator")
@login_required
def simulator():
    """
    Hanoi simulator - placeholder for now.
    Only accessible to authenticated users.
    """
    return "<h1>Hanoi Simulator (Coming Soon)</h1>"