from flask import Flask, current_app as app
from flask_login import LoginManager
from .config import Config
from .models.users import User
from flask_caching import Cache

# Initialize the Flask application
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def create_app(config_class=Config):
    app = Flask(
        __name__, 
        static_folder='../frontend/static', 
        template_folder='../frontend/templates'
    )
    
    app.config.from_object(Config)

    # Initialize the login manager
    login_manager.init_app(app)

    # Initialize the cache
    cache.init_app(app)

    # Register the blueprints
    from .blueprints.main.routes import main_bp as main
    from .blueprints.auth.routes import auth_bp as auth
    from .blueprints.admin.routes import admin_bp as admin
    from .blueprints.university.routes import university_bp as university

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(university, url_prefix='/university/api/v1')

    # Register the error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return "404: Page not found", 404

    @app.errorhandler(500)
    def server_error(e):
        return "500: Internal server error", 500