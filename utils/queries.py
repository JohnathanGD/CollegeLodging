from backend.db import get_db_connection
from flask import g, current_app as app

# Database Queries
CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {};"
USE_DATABASE = "USE {};"

CREATE_TABLE_WITH_COLUMNS = "CREATE TABLE IF NOT EXISTS %s (%s);"

CREATE_USERS_TABLE = '''CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    user_type VARCHAR(255) DEFAULT 'user',
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

CREATE_LISTINGS_TABLE = '''CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    bedroom_count INT NOT NULL,
    bathroom_count DECIMAL(10, 1) NOT NULL,
    furnished BOOLEAN DEFAULT FALSE,
    pets_allowed BOOLEAN DEFAULT FALSE,
    utilities_included BOOLEAN DEFAULT FALSE,
    type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

CREATE_APARTMENT_IMAGES_TABLE = '''CREATE TABLE IF NOT EXISTS apartment_images (
    id SERIAL PRIMARY KEY,
    apartment_id FOREIGN KEY (id) REFERENCES listings (id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (apartment_id) REFERENCES apartments (id)
);'''

ADD_COLUMN_INTO_TABLE = "ALTER TABLE %s ADD COLUMN %s %s;"
GET_COLUMNS = "SHOW COLUMNS FROM %s;"
UPDATE_COLUMN_IN_TABLE = "ALTER TABLE %s MODIFY COLUMN %s %s;"
DROP_COLUMN_FROM_TABLE = "ALTER TABLE %s DROP COLUMN %s;"

ADD_KEY_INTO_TABLE = "ALTER TABLE %s ADD %s %s;"
DROP_KEY_FROM_TABLE = "ALTER TABLE %s DROP %s %s;"
GET_KEYS = "SHOW KEYS FROM %s;"
DROP_KEY_FROM_TABLE = "ALTER TABLE %s DROP %s %s;"

GET_TABLES = "SHOW TABLES;"
UPDATE_TABLE = "ALTER TABLE %s RENAME TO %s;"
DELETE_TABLE = "DROP TABLE %s;"

# User Queries
GET_USER_BY_ID = "SELECT * FROM users WHERE id = %s;"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s;"
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s;"

INSERT_NEW_USER = '''INSERT INTO users (email, password, firstname, lastname) 
VALUES (%s, %s, %s, %s);'''

INSERT_NEW_USER_WITH_USER_TYPE = '''INSERT INTO users (email, password, firstname, lastname, user_type)
VALUES (%s, %s, %s, %s, %s);'''

INSERT_NEW_USER_WITH_IS_ADMIN = '''INSERT INTO users (email, password, firstname, lastname, is_admin)
VALUES (%s, %s, %s, %s, %s);'''

INSERT_NEW_USER_WITH_USER_TYPE_AND_IS_ADMIN = '''INSERT INTO users (email, password, firstname, lastname, user_type, is_admin)
VALUES (%s, %s, %s, %s, %s, %s);'''

UPDATE_USER_PASSWORD = "UPDATE users SET password = %s WHERE id = %s;"
UPDATE_USER_EMAIL = "UPDATE users SET email = %s WHERE id = %s;"
UPDATE_USER_FIRSTNAME = "UPDATE users SET firstname = %s WHERE id = %s;"
UPDATE_USER_LASTNAME = "UPDATE users SET lastname = %s WHERE id = %s;"
UPDATE_USER_USER_TYPE = "UPDATE users SET user_type = %s WHERE id = %s;"
UPDATE_USER_IS_ADMIN = "UPDATE users SET is_admin = %s WHERE id = %s;"

DELETE_USER = "DELETE FROM users WHERE id = %s;"

# Listing Queries
GET_LISTING_BY_ID = "SELECT * FROM listings WHERE id = %s;"
GET_LISTINGS = "SELECT * FROM listings;"
GET_LISTINGS_BY_KEY = "SELECT * FROM listings WHERE %s = %s;"

INSERT_NEW_LISTING = '''INSERT INTO listings (title, description, street_address, city, state, postal_code, country, price, bedroom_count, bathroom_count, furnished, pets_allowed, utilities_included, type);'''

UPDATE_LISTING = "UPDATE listings SET %s = %s WHERE id = %s;"
DELETE_LISTING = "DELETE FROM listings WHERE id = %s;"

# Apartment Image Queries
GET_APARTMENT_IMAGE_BY_ID = "SELECT * FROM apartment_images WHERE id = %s;"
GET_APARTMENT_IMAGES = "SELECT * FROM apartment_images;"
GET_APARTMENT_IMAGES_BY_KEY = "SELECT * FROM apartment_images WHERE %s = %s;"
GET_APARTMENT_IMAGES_BY_APARTMENT_ID = "SELECT * FROM apartment_images WHERE apartment_id = %s;"
INSERT_NEW_APARTMENT_IMAGE = '''INSERT INTO apartment_images (apartment_id, image_url);'''
UPDATE_APARTMENT_IMAGE = "UPDATE apartment_images SET %s = %s WHERE id = %s;"
DELETE_APARTMENT_IMAGE = "DELETE FROM apartment_images WHERE id = %s;"
DELETE_APARTMENT_IMAGES_BY_APARTMENT_ID = "DELETE FROM apartment_images WHERE apartment_id = %s;"

# Query Operations
def execute_query(query, params=None, dictionary=False):
    conn = get_db_connection()
    if conn is None or not conn.is_connected():
        print('Database connection failed. Please try again later.')
        return None
    
    cursor = None
    try:
        cursor = conn.cursor()
        if cursor is None:
            print('Database cursor creation failed. Please try again later.')
            return None
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f'An error occurred during query execution: {e}')
        return None
    finally:    
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return True

def execute_query_with_results(query, params=None, dictionary=False, fetch_one=False):
    conn = get_db_connection()
    if conn is None or not conn.is_connected():
        print('Database connection failed. Please try again later.')
        return None
    
    cursor = None
    results = None
    try:
        cursor = conn.cursor(dictionary=dictionary)
        if cursor is None:
            print('Database cursor creation failed. Please try again later.')
            return None
        cursor.execute(query, params)

        results = cursor.fetchone() if fetch_one else cursor.fetchall()
    except Exception as e:
        print(f'An error occurred during query execution: {e}')
        return None
    finally:    
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return results