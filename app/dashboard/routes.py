# app/dashboard/routes.py

from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    """
    Master dashboard - protected route.
    Only accessible to authenticated users.
    """
    return render_template('dashboard/index.html', title='Dashboard', user=current_user)