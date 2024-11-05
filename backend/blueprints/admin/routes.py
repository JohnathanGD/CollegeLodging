from flask import Blueprint, render_template, request, redirect, current_app as app, g
from flask_login import LoginManager
import utils.decorators

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('admin/admin_signup.html')