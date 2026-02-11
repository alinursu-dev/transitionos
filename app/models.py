# app/models.py

from datetime import datetime, timezone
from sqlalchemy.orm import dynamic
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

# ===========================
# User Model - Authentication and Identity
# ===========================

class User(UserMixin, db.Model):
    """
    User account for authentication.
    Flask-Login requires: get_id(), is_authenticated, is_active, is_anonymous
    UserMixin provides these automatically.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash password before storing in database"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# ===========================
# Expense Model - Financial Tracking
# ===========================

class Expense(db.Model):
    """
    Individual expense transaction.
    Core feature for tracking spending toward €6000 savings goal.
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Transaction details
    date = db.Column(db.Date, nullable=False, index=True)   # Index for date-range queries
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='RON')   # Currency code
    category = db.Column(db.String(100), nullable=False, index=True)   # Index for category filtering
    vendor = db.Column(db.String(100), nullable=True, index=True)   # Index for vendor filtering
    notes = db.Column(db.Text, nullable=True)   # Optional notes field

    # Receipt tracking (Week 7-8 OCR feature)
    receipt_path = db.Column(db.String(255), nullable=True)   # Path to stored receipt image

    # Metadata
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)   # Creation timestamp for sorting
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, onupdate=lambda: datetime.now(timezone.utc))   # Update timestamp for tracking changes

    def __repr__(self):
        return f'<Expense {self.date} {self.amount} {self.currency} - {self.category}>'

    @property
    def amount_ron(self):
        """Convert amount to RON for consistent calculations using current exchange rate"""
        if self.currency == 'RON':
            return self.amount
        elif self.currency == 'EUR':
            return self.amount * 5.1 # Placeholder exchange rate, replace with live rate from API later
        elif self.currency == 'USD':
            return self.amount * 4.28 # Placeholder exchange rate, replace with live rate from API later
        elif self.currency == 'VND':
            return self.amount * 0.00016 # Placeholder exchange rate, replace with live rate from API later 
        else:
            return self.amount # Default to original amount if currency is not recognized
    
# ===========================
# Goal Model - Savings Tracking
# ===========================
class Goal(db.Model):
    """
    Goal tracking for Financial, Career, Relocation categories.
    Example: Financial -> Save €6000 by Oct 31, 2026
    """
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Goal details
    category = db.Column(db.String(50), nullable=False)   # 'Financial', 'Career', 'Relocation'
    title = db.Column(db.String(200), nullable=False)   # 'Save €6000 by Oct 31, 2026'
    description = db.Column(db.Text)   # Optional description field

    # Progress tracking
    target_value = db.Column(db.Float, nullable=False)   # Amount to save in target currency e.g. €6000 for savings
    current_value = db.Column(db.Float, nullable=False, default=0.0)   # Current progress towards target e.g. €3000 saved
    unit = db.Column(db.String(20), nullable=False, default='RON')   # Currency unit e.g. '€', 'RON', 'USD', 'VND', clients, words (Vietnamese)

    # Timeline
    target_date = db.Column(db.Date, nullable=False)   # Date by which goal should be achieved
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)   # Creation timestamp for sorting
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, onupdate=lambda: datetime.now(timezone.utc))   # Update timestamp for tracking changes

    # Status
    is_completed = db.Column(db.Boolean, nullable=False, default=False)   # Whether goal has been achieved
    completed_at = db.Column(db.DateTime, nullable=True)   # Date and time when goal was completed
    completion_notes = db.Column(db.Text, nullable=True)   # Optional notes about completion

    def __repr__(self):
        return f'<Goal {self.category}: {self.title} ({self.progress_percent}%)>'

    @property
    def progress_percent(self):
        """Calculate remaining value to reach target in percentage"""
        if self.target_value == 0:
            return 0
        return min(100, (self.current_value / self.target_value) * 100)

    @property
    def remaining_value(self):
        """Calculate remaining value to reach target"""
        return max(0, self.target_value - self.current_value)

    @property
    def days_remaining(self):
        """Calculate days remaining to reach target"""
        if self.target_date:
            delta = self.target_date - datetime.now(timezone.utc).date()
            return max(0, delta.days)
        return None

    def is_on_track(self):
        """
        Simple on-track calculation.
        If today's progress >= expected progress by now, return True.
        """
        if not self.target_date:
            return None

        total_days = (self.target_date - self.created_at.date()).days
        elapsed_days = (datetime.now(timezone.utc).date() - self.created_at.date()).days

        if total_days <= 0:
            return self.is_completed

        expected_progress = (elapsed_days / total_days) * 100
        return self.progress_percent >= expected_progress