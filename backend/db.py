from mysql.connector import Error
from flask import g, current_app as app
import mysql.connector
from .config import Config

def get_db_connection():
    if 'db_connection' not in g or not g.db_connection.is_connected():
        try:
            g.db_connection = mysql.connector.connect(
                host=app.config.get('DB_HOST'),
                user=app.config.get('DB_USER'),
                password=app.config.get('DB_PASSWORD'),
                database=app.config.get('DB_NAME'),
                port=app.config.get('DB_PORT')
            )
        except Error as e:
            print(f"Error connecting to the database: {e}")
            app.logger.error(f"Error connecting to the database: {e}")
            return None
    return g.db_connection

# @app.teardown_appcontext
def close_db_connection(exception=None):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()