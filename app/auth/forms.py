# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """ Login form with CSRF protection """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        ],
        render_kw={'placeholder': 'Enter your username', 'autofocus': True}
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=4, max=120, message='Password must be between 4 and 120 characters'),
        ],
        render_kw={'placeholder': 'Enter your password'},
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')