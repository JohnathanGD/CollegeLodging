from flask import Blueprint, render_template, request, redirect, current_app as app, g, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from backend.models.users import User
from werkzeug.security import generate_password_hash
from backend.db import get_db_connection
import utils.queries as queries
from utils.decorators import unauthenticated_user, login_required, admin_only
from backend import cache
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/signup', methods=['GET', 'POST'])
@unauthenticated_user
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        firstname = request.form.get('first-name')
        lastname = request.form.get('last-name')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('admin/admin_signup.html')
                
        if User.get_by_email(email):
            flash('User with this email already exists.', 'error')
            return render_template('admin/admin_signup.html')
        
        params = (email, generate_password_hash(password), firstname, lastname, 'admin', True)

        if (queries.execute_query(queries.INSERT_NEW_USER_WITH_USER_TYPE_AND_IS_ADMIN, params)):
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred during signup. Please try again later.', 'error')
            return redirect(url_for('admin.signup'))
        
    return render_template('admin/admin_signup.html')

@admin_bp.route('/dashboard')
@login_required
@admin_only
def dashboard():
    return render_template('admin/admin_dashboard.html')

@admin_bp.route('/database')
@login_required
@admin_only
def database():
    return render_template('admin/database.html')

@cache.cached(timeout=60)
def get_users():
    users = queries.execute_query_with_results(queries.GET_USERS_WITH_ROLES, dictionary=True)

    return users

@admin_bp.route('/users')
@login_required
@admin_only
def users():
    users = get_users()

    for user in users:
        user['created_at'] = user['created_at'].strftime('%B %d, %Y %I:%M %p')

    return render_template('admin/users.html', users=users)