from flask import Blueprint, render_template, request, redirect, current_app as app, g
import mysql.connector
from mysql.connector import Error
from backend.db import get_db_connection

main_bp = Blueprint('main', __name__)

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