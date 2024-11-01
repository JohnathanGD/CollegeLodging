import mysql.connector
from mysql.connector import Error
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')  # Load configurations from config.py

def setup_database():
    db_conn = None
    try:
        with app.app_context():
            db_conn = mysql.connector.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD']
            )
            cursor = db_conn.cursor()

            db_name = app.config['DB_NAME']

            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Database {db_name} created successfully.")

            cursor.execute(f"USE {db_name};")

            # Create the users table if it doesn't exist
            create_users_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(120) NOT NULL UNIQUE,
                password VARCHAR(120) NOT NULL,
                firstname VARCHAR(50),
                lastname VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''

            cursor.execute(create_users_table_query)
            print("Table 'users' created successfully.")
        
            db_conn.commit()
    except Error as e:
        print(f"Error during database setup: {e}")
    finally:
        if db_conn and db_conn.is_connected():
            cursor.close()
            db_conn.close()

if __name__ == '__main__':
    setup_database()
