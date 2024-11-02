from setuptools import setup, find_packages
import mysql.connector
from mysql.connector import Error
from flask import current_app as app
from backend import create_app

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
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            cursor.execute(f"USE {db_name};")

            create_users_table = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    user_type VARCHAR(100)
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """

            cursor.execute(create_users_table)
            db_connection.commit()
    except Error as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()

if __name__ == '__main__':
    setup_db()