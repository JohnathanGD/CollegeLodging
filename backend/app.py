from flask import Flask, request, redirect, render_template, g, url_for
from flask import current_app as app

import mysql.connector
from mysql.connector import Error

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder= "../frontend/static"
)

app.config.from_pyfile('config.py')

def get_db_connection():
    '''Establishes a connection to the database'''
    if 'db_conn' not in g:
        try:
            g.db_conn = mysql.connector.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME'],
                port=app.config['DB_PORT']
            )
        except Error as e:
            app.logger.error(f"Error connecting to MySQL: {e}")
            return None
    return g.db_conn

@app.teardown_appcontext
def close_db_connection(exception=None):
    '''Closes the database connection'''
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Registers a new user'''
    if request.method == 'POST':
        # Retrieve form data from the HTML form
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')

        #TODO: Address security issues with storing passwords in plain text
        password = request.form.get('password')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user data into the database
        query = 'INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)'
        cursor.execute(query, (first_name, last_name, email, password))

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the home page after successful sign up
        return render_template('index.html')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Logs in an existing user'''
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db_conn = get_db_connection()
        if db_conn is None:
            return "Database connection error", 500
        
        cursor = db_conn.cursor(dictionary=True)
    
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        cursor.close()

        if user:
            return redirect(url_for('index')) 
        else:
            return render_template('login.html', error="Invalid email or password")
        
    return render_template('login.html')

@app.route('/apartment-search')
def apartment_search():
    return render_template('ApartmentSearch.html')

if __name__ == '__main__':
    app.run(debug=True)