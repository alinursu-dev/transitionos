# app/auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import auth_bp
from app.auth.forms import LoginForm
from app.models import User
from app.extensions import db

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route.
    GET: Display login form
    POST: Process login form
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    # Process login form
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(username=form.username.data).first()

        # Verify user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        # Login user
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}!', 'success')

        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index') # Redirect to dashboard
        return redirect(next_page) # Redirect to next page

    return render_template('auth/login.html', form=form, title='Login')

@auth_bp.route('/logout')
def logout():
    """
    Logout route.
    Logs out the current user and redirects to login page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))