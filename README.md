# TransitionOS

A personal life operating system and portfolio web app for tracking career transition, relocation, and financial goals—built with Flask.

## What is TransitionOS

TransitionOS is a Flask application that serves three purposes: (1) a **personal command center** for financial, career, and relocation goals (e.g. savings target, freelance income, days to move); (2) a **portfolio showcase** demonstrating full-stack Flask, SQLAlchemy, and modern UI; and (3) a **reusable template** others can fork for their own transitions. The app consolidates dashboard metrics, expense tracking, and goal progress in one place.

## What's done (current state)

- **Environment:** Virtual environment, `requirements.txt`, `.gitignore`.
- **Project structure:** Blueprint layout (`auth`, `dashboard`, `expenses`), app factory in `app/__init__.py`, `config.py` with dev SQLite, `UPLOAD_FOLDER` for receipts.
- **Database:** SQLAlchemy models (`User`, `Expense`, `Goal`), Flask-Migrate, migrations, SQLite stored in `instance/`.
- **Authentication:** Flask-Login, `/auth/login` and `/auth/logout`, password hashing (Werkzeug), session handling, `@login_required` on protected routes, root `/` redirect to login or dashboard.
- **Dashboard:** Routes `/` and `/dashboard` with hero metrics (savings progress, freelance income, days to move, runway months), recent expenses table.
- **Expenses:** List view at `/expenses` showing the current user's expenses.
- **UI:** `base.html` with navbar, flash messages, Bootstrap 5 (CDN), DM Sans font; login page, dashboard index, expenses list; responsive layout.

## Tech stack

- **Backend:** Flask 3, Flask-Login, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, SQLAlchemy 2, Werkzeug
- **Templates:** Jinja2, Bootstrap 5 (CDN)
- **Database:** SQLite (default); configurable via `DATABASE_URL` (e.g. PostgreSQL)
- **Future use:** pandas, Plotly (in `requirements.txt`)

## Project structure

```
transitionos/
├── app/
│   ├── __init__.py      # App factory, root route, blueprint registration
│   ├── extensions.py    # db, login_manager, migrate
│   ├── models.py        # User, Expense, Goal
│   ├── auth/            # Login, logout
│   ├── dashboard/       # Dashboard index, metrics, recent expenses
│   ├── expenses/        # Expense list
│   └── templates/       # base, auth/login, dashboard/index, expenses/list
├── config.py            # Config, SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER
├── migrations/          # Flask-Migrate / Alembic
├── instance/            # SQLite DB and uploads (not committed)
├── requirements.txt
└── README.md
```

## Getting started

**Prerequisites:** Python 3.10+

1. Clone the repo and go to the project directory.

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set the Flask app and run migrations:
   ```bash
   export FLASK_APP=app
   flask db upgrade
   ```

5. (Optional) Create an admin user and sample goals in the Flask shell:
   ```python
   from app.extensions import db
   from app.models import User, Goal
   from datetime import date

   admin = User(username='admin', email='your@email.com')
   admin.set_password('YourSecurePassword')
   db.session.add(admin)
   db.session.commit()

   goals = [
       Goal(user_id=admin.id, category='Financial', title='Save €5,500 for Hanoi',
            target_value=5500, current_value=3200, unit='EUR', target_date=date(2026, 10, 31)),
       Goal(user_id=admin.id, category='Career', title='Reach €1,500/mo freelance income',
            target_value=1500, current_value=800, unit='EUR', target_date=date(2026, 12, 31)),
   ]
   db.session.add_all(goals)
   db.session.commit()
   ```

6. Run the development server:
   ```bash
   flask run
   ```
   Open http://127.0.0.1:5000 . The root URL redirects to login (or dashboard if already logged in).

**Production:** Set `SECRET_KEY` and optionally `DATABASE_URL` (e.g. PostgreSQL) via environment variables or a `.env` file; do not rely on the default dev secret.

## License

MIT.
