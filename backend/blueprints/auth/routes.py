from flask import Blueprint, render_template, request, redirect, current_app as app, g, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
import mysql.connector
from mysql.connector import Error
from backend.models.users import User
from werkzeug.security import generate_password_hash
from backend.db import get_db_connection
from utils.decorators import unauthenticated_user
import utils.queries as queries

auth_bp = Blueprint('auth', __name__)

def close_db_connection(exception=None):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()

@auth_bp.route('/signup', methods=['GET', 'POST'])
@unauthenticated_user
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('first-name')
        lastname = request.form.get('last-name')

        if User.get_by_email(email):
            flash('User with this email already exists.', 'error')
            return redirect(url_for('auth.signup'))

        params = (email, generate_password_hash(password), firstname, lastname)

        if (queries.execute_query(queries.INSERT_NEW_USER, params)):
            user_id = queries.execute_query_with_results(queries.GET_USER_ID_BY_EMAIL, (email,), fetch_one=True)[0]
            
            if user_id is None:
                flash('An error occurred during signup. Please try again later.', 'error')
                return redirect(url_for('auth.signup'))

            if (queries.execute_query(queries.ADD_USER_ROLE_BY_NAME, (user_id, 'user'))):
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('An error occurred during signup. Please try again later.', 'error')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@unauthenticated_user
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.apartment_search'))

        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))