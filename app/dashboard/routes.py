# app/dashboard/routes.py
from flask import render_template
from flask_login import login_required, current_user
from datetime import date

from app.dashboard import dashboard_bp
from app.models import Goal, Expense


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Simple initial metrics
    financial_goal = Goal.query.filter_by(user_id=current_user.id, category="Financial").first()
    career_goal = Goal.query.filter_by(user_id=current_user.id, category="Career").first()

    savings_current = financial_goal.current_value if financial_goal else 0
    savings_target = financial_goal.target_value if financial_goal else 5500
    savings_percent = round((savings_current / savings_target) * 100, 1) if savings_target else 0

    freelance_current = career_goal.current_value if career_goal else 0
    freelance_target = career_goal.target_value if career_goal else 1500

    move_date = date(2026, 10, 31)
    days_left = (move_date - date.today()).days

    hanoi_burn = 890
    runway_months = round(savings_current / hanoi_burn, 1) if hanoi_burn else 0

    recent_expenses = (
        Expense.query.filter_by(user_id=current_user.id)
        .order_by(Expense.date.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        savings_current=savings_current,
        savings_target=savings_target,
        savings_percent=savings_percent,
        freelance_current=freelance_current,
        freelance_target=freelance_target,
        days_left=days_left,
        runway_months=runway_months,
        recent_expenses=recent_expenses,
    )
