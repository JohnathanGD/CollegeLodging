from flask import Flask, request, redirect, render_template
import mysql.connector

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder= "../frontend/static"
)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="CollegeLodging",
        database="Lodging"
    )

# Sign up route to handle form submissions
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data from the HTML form
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        print(first_name,last_name,email,password)
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user data into the database
        query = 'INSERT INTO login (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)'
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