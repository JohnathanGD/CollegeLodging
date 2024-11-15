from flask import Blueprint, render_template, request, redirect, current_app as app, g, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from backend.models.users import User
from backend.models.listings import Listing
from werkzeug.security import generate_password_hash
from backend.db import get_db_connection
import utils.queries as queries
from utils.decorators import unauthenticated_user, login_required, admin_only
from backend import cache
from datetime import datetime

admin_bp = Blueprint('admin', __name__)
PAGINATION_LIMIT = 10

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

@admin_bp.route('/users')
@login_required
@admin_only
def users():
    def get_users(pagination=True, per_page=PAGINATION_LIMIT, page=1):
        if pagination:
            offset = (page - 1) * per_page
            params = (per_page, offset)
            return queries.execute_query_with_results(queries.GET_USERS_WITH_PAGINATION, params=params, dictionary=True)

        return queries.execute_query_with_results(queries.GET_USERS_WITH_ROLES, dictionary=True)

    def get_user_count():
        count = int(queries.execute_query_with_results(queries.GET_TOTAL_USERS, fetch_one=True, dictionary=True)['COUNT(*)'])
        print(count, type(count))

        return count

    page = request.args.get('page', 1, type=int)

    total_users = get_user_count()
    total_pages = (total_users + PAGINATION_LIMIT - 1) // PAGINATION_LIMIT

    cache_key = f'users_page_{page}'
    users = cache.get(cache_key)
    if users is None:
        users = get_users(page=page)
        cache.set(cache_key, users, timeout=60)

    for user in users:
        user['created_at'] = user['created_at'].strftime('%B %d, %Y %I:%M %p')

    return render_template('admin/users.html', users=users, total_pages=total_pages, current_page=page)

@admin_bp.route('/properties')
@login_required
@admin_only
def properties():
    listings = get_listings()  # Use existing function for listings
    
    for listing in listings:
        listing['created_at'] = listing['created_at'].strftime('%B %d, %Y %I:%M %p')

    return render_template('admin/properties.html', listings=listings)

@cache.cached(timeout=60)
def get_listings():
    # Execute the GET_LISTINGS query
    properties = queries.execute_query_with_results(queries.GET_LISTINGS, dictionary=True)
    
    return properties

@admin_bp.route('/add-property', methods=['GET', 'POST'])
@login_required
@admin_only
def add_property():
    if request.method == 'POST':
        # Collect form data
        title = request.form.get('title')
        description = request.form.get('description')
        street_address = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        country = request.form.get('country')
        price = float(request.form.get('price'))  # Ensure price is treated as a number
        bedroom_count = int(request.form.get('bedroom_count'))  # Ensure bedroom count is an integer
        bathroom_count = int(request.form.get('bathroom_count'))  # Ensure bathroom count is an integer
        furnished = request.form.get('furnished') == 'on'
        pets_allowed = request.form.get('pets_allowed') == 'on'
        utilities_included = request.form.get('utilities_included') == 'on'
        
        # Add the missing 'type' and date_listed parameters
        type = request.form.get('type')
        
        # Create a new Listing object
        new_property = Listing(
            id=None,  # Assuming id is auto-generated in the database
            title=title,
            description=description,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            price=price,
            bedroom_count=bedroom_count,
            bathroom_count=bathroom_count,
            furnished=furnished,
            pets_allowed=pets_allowed,
            utilities_included=utilities_included,
            type=type,  # Use 'type_' here as well
        )
        
        # Save the new listing using the insert query
        params = (
            new_property.title, new_property.description, new_property.street_address, new_property.city, new_property.state, 
            new_property.postal_code, new_property.country, new_property.price, new_property.bedroom_count, new_property.bathroom_count, 
            new_property.furnished, new_property.pets_allowed, new_property.utilities_included, new_property.type,
        )
        
        # Execute the insert query
        queries.execute_query(queries.INSERT_NEW_LISTING, params)

        flash("Property added successfully!", "success")
        return redirect(url_for('admin.properties'))  # Redirect to properties page

    return render_template('admin/add_property.html')  # Render the form if GET request
