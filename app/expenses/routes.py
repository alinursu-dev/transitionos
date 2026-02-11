# app/expenses/routes.py

from flask import render_template
from flask_login import login_required, current_user

from app.expenses import expenses_bp
from app.models import Expense


@expenses_bp.route("/")
@login_required
def list():
    expenses = (
        Expense.query.filter_by(user_id=current_user.id)
        .order_by(Expense.date.desc())
        .all()
    )
    return render_template("expenses/list.html", expenses=expenses)
