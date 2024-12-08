from flask import Blueprint, render_template, request, redirect, current_app as app, g, url_for, flash, jsonify, get_flashed_messages
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from backend.models.users import User
from backend.models.listings import Listing
from werkzeug.security import generate_password_hash
from backend.db import get_db_connection
import utils.queries as queries
from utils.decorators import unauthenticated_user, login_required, admin_only
from backend import cache
from datetime import datetime
import base64

admin_bp = Blueprint('admin', __name__)
PAGINATION_LIMIT = 10
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@admin_bp.route('/get_flash_messages', methods=['GET'])
@login_required
@admin_only
def get_flash_messages():
    messages = get_flashed_messages(with_categories=True)
    return jsonify(messages=messages)

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
        
        params = (email, generate_password_hash(password), firstname, lastname, True)
        roles = ['admin', 'user']

        if (queries.execute_query(queries.INSERT_NEW_USER_WITH_IS_ADMIN, params)):
            user_id = queries.execute_query_with_results(queries.GET_USER_ID_BY_EMAIL, (email,), fetch_one=True)[0]

            for role in roles:
                if not queries.execute_query(queries.ADD_USER_ROLE_BY_NAME, (user_id, role)):
                    flash('An error occurred during signup. Please try again later.', 'error')
                    return redirect(url_for('admin.signup'))

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

@admin_bp.route('/get_user/<int:user_id>', methods=['GET'])
@login_required
@admin_only
def get_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'roles': user.roles,
            'created_at': user.created_at
        })
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_only
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete yourself.', 'error')
        return jsonify({
            'success': False,
            'error': 'You cannot delete yourself.',
        }), 400
    
    if queries.execute_query(queries.DELETE_USER_BY_ID, (user_id,)):
        flash('User deleted successfully.', 'success')
        return jsonify({
            'success': True,
            'message': 'User deleted successfully.'
        }), 200

    flash('An error occurred while deleting the user.', 'error')
    return jsonify({
        'success': False,
        'error': 'An error occurred while deleting the user.'
    }), 500
    
@admin_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@login_required
@admin_only    
def update_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        roles = data.get('roles')

        if user.email != email and User.get_by_email(email):
            flash('User with this email already exists.', 'error')
            return jsonify({'error': 'User with this email already exists.'}), 400

        if user.firstname == firstname and user.lastname == lastname and user.email == email and user.roles == roles:
            flash('No changes detected.', 'info')
            return jsonify({'message': 'No changes detected.'}), 200

        if queries.execute_query(queries.UPDATE_USER_NAME_AND_EMAIL, (email, firstname, lastname, user_id)):
            flash('User updated successfully.', 'success')
            return jsonify({'message': 'User updated successfully.'}), 200

        app.logger.debug(f'Updating user {user_id} with data: {data}')
        flash('An error occurred while updating the user.', 'error')
        return jsonify({'error': 'An error occurred while updating the user.'}), 500

    flash('User not found.', 'error')
    return jsonify({'error': 'User not found.'}), 404

# Listings
@admin_bp.route('/properties')
@login_required
@admin_only
def properties():
    listings = get_listings()  # Use existing function for listings
    
    for listing in listings:
        listing['created_at'] = listing['created_at'].strftime('%B %d, %Y %I:%M %p')

    return render_template('admin/properties.html', listings=listings)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cache.cached(timeout=60)
def get_listings():
    properties = queries.execute_query_with_results(queries.GET_LISTINGS, dictionary=True)
    property_images = queries.execute_query_with_results(queries.GET_LISTING_IMAGES, dictionary=True)

    images_by_listing_id = {}
    for image in property_images:
        listing_id = image['listing_id']
        if listing_id not in images_by_listing_id:
            images_by_listing_id[listing_id] = []
        # Encode image data as Base64
        images_by_listing_id[listing_id].append(base64.b64encode(image['image_data']).decode('utf-8'))

    listings_dict = {}
    for property in properties:
        listing_id = property['id']
        if listing_id not in listings_dict:
            listings_dict[listing_id] = {
                'id': property['id'],
                'title': property['title'],
                'description': property['description'],
                'street_address': property['street_address'],
                'city': property['city'],
                'state': property['state'],
                'postal_code': property['postal_code'],
                'country': property['country'],
                'price': property['price'],
                'bedroom_count': property['bedroom_count'],
                'bathroom_count': property['bathroom_count'],
                'furnished': property['furnished'],
                'pets_allowed': property['pets_allowed'],
                'utilities_included': property['utilities_included'],
                'is_available': property['is_available'],
                'type': property['type'],
                'created_at': property['created_at'],
                'images': images_by_listing_id.get(listing_id, [])
            }

    return list(listings_dict.values())

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
        type = request.form.getlist('type')
        
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
