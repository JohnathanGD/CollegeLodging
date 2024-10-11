from flask import Flask, request, redirect, render_template, g
from flask import current_app as app

import mysql.connector
from mysql.connector import Error

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder= "../frontend/static"
)

app.config.from_pyfile('config.py')

# Database connection
def get_db_connection():
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

# Close database connection
@app.teardown_appcontext
def close_db_connection(exception=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

# Sign up route to handle form submissions
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data from the HTML form
        print(request.form.get('first-name'))
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')

        print(first_name,last_name,email,password)
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

    # If it's a GET request, render the sign-up page
    return render_template('signup.html')

# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/apartment-search')
def apartment_search():
    return render_template('ApartmentSearch.html')

if __name__ == '__main__':
    app.run(debug=True)