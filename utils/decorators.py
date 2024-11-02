from flask import g, current_app as app, redirect, url_for
from functools import wraps
from flask_login import current_user

def unauthenticated_user(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        return view(*args, **kwargs)
    return decorated_function

def login_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return view(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return decorated_function

