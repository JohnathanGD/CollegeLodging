import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

            print(f"Creating database {db_name}...")

            cursor.execute(queries.CREATE_DATABASE.format(db_name))
            cursor.execute(queries.USE_DATABASE.format(db_name))

            cursor.execute(queries.CREATE_USERS_TABLE)
            cursor.execute(queries.CREATE_ROLES_TABLE)
            cursor.execute(queries.CREATE_USER_ROLES_TABLE)
            cursor.execute(queries.CREATE_LIKES_TABLE)

            roles = ['admin', 'user']

            for role in roles:
                cursor.execute(queries.INSERT_NEW_ROLE, (role, role))

            cursor.execute(queries.CREATE_LISTINGS_TABLE)
            cursor.execute(queries.CREATE_LISTING_IMAGES_TABLE)

            db_connection.commit()

            print(f"Database {db_name} created successfully.")
    except Error as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()

if __name__ == '__main__':
    setup_db()
