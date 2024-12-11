from flask import Flask, Blueprint, render_template, request, redirect, current_app as app, g
import mysql.connector
from mysql.connector import Error
from backend.db import get_db_connection
from backend.services.webscraper import get_listing_near_university
import backend.services.university_service as university_service
from backend import cache

main_bp = Blueprint('main', __name__)

listings_cache = {}

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/apartment-search')
def apartment_search():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM listings"
    cursor.execute(query)
    listings = cursor.fetchall()

    cursor.close()
    return render_template('ApartmentSearch.html' , listings= listings)

@main_bp.route('/apartment-search/<string:state>/<string:city>/<string:school>')
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def apartment_search_near_university(state, city, school):
    listings = []
    
    # Normalize input
    state = state.lower()
    city = city.lower()
    school = school.lower().replace(" ", "-")

    cache_key = f"{state}_{city}_{school}"

    if cache_key in listings_cache:
        listings = listings_cache[cache_key]
    else:
        listings = get_listing_near_university(state, city, school)
        listings_cache[cache_key] = listings

    return render_template('ApartmentSearch.html', listings=listings)