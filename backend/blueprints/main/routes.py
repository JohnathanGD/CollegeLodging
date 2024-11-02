from flask import Blueprint, render_template, request, redirect, current_app as app, g
import mysql.connector
from mysql.connector import Error

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/apartment-search')
def apartment_search():
    return render_template('ApartmentSearch.html')