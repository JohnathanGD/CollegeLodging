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
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

CREATE_ROLES_TABLE = '''CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

CREATE_USER_ROLES_TABLE  = '''CREATE TABLE IF NOT EXISTS user_roles (
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
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
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
);'''

CREATE_LISTING_IMAGES_TABLE = '''CREATE TABLE IF NOT EXISTS listing_images (
    id SERIAL PRIMARY KEY,
    listing_id BIGINT UNSIGNED NOT NULL,
    image_data LONGBLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings (id) ON DELETE CASCADE
);'''

RENAME_COLUMN_IN_TABLE = "ALTER TABLE %s RENAME COLUMN %s TO %s;"
ADD_COLUMN_INTO_TABLE = "ALTER TABLE %s ADD COLUMN %s %s;"
GET_COLUMNS = "SHOW COLUMNS FROM %s;"
UPDATE_COLUMN_IN_TABLE = "ALTER TABLE %s MODIFY COLUMN %s %s;"
UPDATE_COLUMN_IN_TABLE_WITH_DEFAULT = "ALTER TABLE %s MODIFY COLUMN %s %s DEFAULT %s;"
DROP_COLUMN_FROM_TABLE = "ALTER TABLE %s DROP COLUMN %s;"

ADD_KEY_INTO_TABLE = "ALTER TABLE %s ADD %s %s;"
DROP_KEY_FROM_TABLE = "ALTER TABLE %s DROP %s %s;"
GET_KEYS = "SHOW KEYS FROM %s;"
DROP_KEY_FROM_TABLE = "ALTER TABLE %s DROP %s %s;"

GET_TABLES = "SHOW TABLES;"
UPDATE_TABLE = "ALTER TABLE %s RENAME TO %s;"
DELETE_TABLE = "DROP TABLE %s;"

# User Queries
GET_USERS = "SELECT * FROM users;"
GET_USER_BY_ID = "SELECT * FROM users WHERE id = %s;"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s;"
GET_ATTRIBUTE_BY_USER_ID = "SELECT %s FROM users WHERE id = %s;"
GET_USER_ID_BY_EMAIL = "SELECT id FROM users WHERE email = %s;"
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s;"
GET_USERS_WITH_ROLES = '''
SELECT users.id, users.firstname, users.lastname, users.email, GROUP_CONCAT(roles.role_name) as roles, users.is_admin, users.created_at
FROM users
LEFT JOIN user_roles ON users.id = user_roles.user_id
LEFT JOIN roles ON user_roles.role_id = roles.id
GROUP BY users.id;
'''
GET_TOTAL_USERS = "SELECT COUNT(*) FROM users;"

GET_USERS_WITH_PAGINATION = '''
SELECT users.id, users.firstname, users.lastname, users.email, GROUP_CONCAT(roles.role_name) as roles, users.created_at
FROM users
LEFT JOIN user_roles ON users.id = user_roles.user_id
LEFT JOIN roles ON user_roles.role_id = roles.id
GROUP BY users.id
LIMIT %s OFFSET %s;
'''

INSERT_NEW_USER = '''INSERT INTO users (email, password, firstname, lastname) 
VALUES (%s, %s, %s, %s);'''

INSERT_NEW_USER_WITH_IS_ADMIN = '''INSERT INTO users (email, password, firstname, lastname, is_admin)
VALUES (%s, %s, %s, %s, %s);'''

UPDATE_USER_PASSWORD = "UPDATE users SET password = %s WHERE id = %s;"
UPDATE_USER_EMAIL = "UPDATE users SET email = %s WHERE id = %s;"
UPDATE_USER_FIRSTNAME = "UPDATE users SET firstname = %s WHERE id = %s;"
UPDATE_USER_LASTNAME = "UPDATE users SET lastname = %s WHERE id = %s;"
UPDATE_USER_IS_ADMIN_STATUS = "UPDATE users SET is_admin = %s WHERE id = %s;"
UPDATE_USER_NAME_AND_EMAIL = "UPDATE users SET email = %s, firstname = %s, lastname = %s WHERE id = %s;"
DELETE_USER_BY_ID = "DELETE FROM users WHERE id = %s;"

# Role Queries
GET_ROLES = "SELECT * FROM roles;"
GET_ROLE_BY_ID = "SELECT * FROM roles WHERE id = %s;"
GET_ROLE_BY_NAME = "SELECT * FROM roles WHERE role_name = %s;"
GET_ROLE_BY_USER_ID = "SELECT * FROM roles WHERE id = (SELECT role_id FROM user_roles WHERE user_id = %s);"

INSERT_NEW_ROLE = "INSERT INTO roles (role_name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM roles WHERE role_name = %s);"
UPDATE_ROLE = "UPDATE roles SET %s = %s WHERE id = %s;"
UPDATE_ROLE_NAME = "UPDATE roles SET role_name = %s WHERE id = %s;"
DELETE_ROLE = "DELETE FROM roles WHERE id = %s;"
DELETE_ROLE_BY_NAME = "DELETE FROM roles WHERE role_name = %s;"
DELETE_ROLE_BY_USER_ID = "DELETE FROM roles WHERE id = (SELECT role_id FROM user_roles WHERE user_id = %s);"

# User Role Queries
ADD_USER_ROLE = "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s);"
ADD_USER_ROLE_BY_NAME = "INSERT INTO user_roles (user_id, role_id) VALUES (%s, (SELECT id FROM roles WHERE role_name = %s));"
REMOVE_USER_ROLE = "DELETE FROM user_roles WHERE user_id = %s AND role_id = %s;"
REMOVE_USER_ROLE_BY_NAME = "DELETE FROM user_roles WHERE user_id = %s AND role_id = (SELECT id FROM roles WHERE role_name = %s);"
GET_USER_ROLES = "SELECT * FROM user_roles WHERE user_id = %s;"

GET_USER_ROLES_NAMES = '''
SELECT roles.role_name, roles.id
FROM roles
JOIN user_roles ON roles.id = user_roles.role_id
WHERE user_roles.user_id = %s;
'''

GET_USER_ROLE = "SELECT * FROM user_roles WHERE user_id = %s AND role_id = %s;"
GET_USER_ROLE_BY_NAME = "SELECT * FROM user_roles WHERE user_id = %s AND role_id = (SELECT id FROM roles WHERE role_name = %s);"

DELETE_USER = "DELETE FROM users WHERE id = %s;"

# Listing Queries
GET_LISTING_ID_BY_TITLE = "SELECT id FROM listings WHERE title = %s;"
GET_LISTING_BY_ID = "SELECT * FROM listings WHERE id = %s;"
GET_LISTINGS = "SELECT * FROM listings;"
GET_LISTINGS_BY_KEY = "SELECT * FROM listings WHERE %s = %s;"

INSERT_NEW_LISTING = '''INSERT INTO listings (title, description, street_address, city, state, postal_code, country, price, bedroom_count, bathroom_count, furnished, pets_allowed, utilities_included, type)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

UPDATE_LISTING_BY_ID = """
UPDATE listings
SET title = %s, description = %s, street_address = %s, city = %s, state = %s, postal_code = %s,
    country = %s, price = %s, bedroom_count = %s, bathroom_count = %s, furnished = %s, 
    pets_allowed = %s, utilities_included = %s, type = %s
WHERE id = %s;
"""
DELETE_LISTING_BY_ID = "DELETE FROM listings WHERE id = %s;"

# Listing Image Queries
GET_LISTING_IMAGE_BY_ID = "SELECT * FROM listing_images WHERE id = %s;"
GET_LISTING_IMAGES = "SELECT * FROM listing_images;"
GET_LISTING_IMAGES_BY_KEY = "SELECT * FROM listing_images WHERE %s = %s;"
GET_LISTING_IMAGES_BY_LISTING_ID = "SELECT * FROM listing_images WHERE listing_id = %s;"

INSERT_NEW_LISTING_IMAGE = '''INSERT INTO listing_images (listing_id, image_data)
VALUES(%s, %s);'''

UPDATE_LISTING_IMAGE = "UPDATE listing_images SET %s = %s WHERE id = %s;"
DELETE_LISTING_IMAGE = "DELETE FROM listing_images WHERE id = %s;"
DELETE_LISTING_IMAGES_BY_LISTING_ID = "DELETE FROM listing_images WHERE listing_id = %s;"

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