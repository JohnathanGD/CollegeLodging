from flask import Blueprint, render_template, request, redirect, current_app as app, g, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
import mysql.connector
from mysql.connector import Error
from backend.models.users import User
from werkzeug.security import generate_password_hash
from backend.db import get_db_connection
from utils.decorators import unauthenticated_user

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

        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed. Please try again later.', 'error')
            return redirect(url_for('auth.signup'))

        try:
            cursor = conn.cursor()
            if cursor is None:
                flash('Database cursor creation failed. Please try again later.', 'error')
                return redirect(url_for('auth.signup'))

            password_hash = generate_password_hash(password)
            query = '''
            INSERT INTO users (email, password, firstname, lastname)
            VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(query, (email, password_hash, firstname, lastname))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('An error occurred during signup. Please try again later.', 'error')
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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