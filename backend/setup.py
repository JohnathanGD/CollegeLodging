from setuptools import setup, find_packages
import mysql.connector
from mysql.connector import Error
from flask import current_app as app
from backend import create_app
import utils.queries as queries

app = create_app()

def setup_db():
    db_connection = None

    try:
        with app.app_context():
            db_connection = mysql.connector.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                port=app.config['DB_PORT']
            )

            cursor = db_connection.cursor()
            db_name = app.config['DB_NAME']

            params = (db_name,)

            cursor.execute(queries.CREATE_DB, params)
            cursor.execute(queries.USE_DB, params)
            cursor.execute(queries.CREATE_USERS_TABLE)
            
            db_connection.commit()
    except Error as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()

if __name__ == '__main__':
    setup_db()