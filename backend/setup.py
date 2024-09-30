import mysql.connector

# Database connection parameters
host = "localhost"
user = "root"
password = "CollegeLodging"

# Establish connection using mysqlclient (or mysql.connector)
db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password
)
cursor = db.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS Lodging;")
print("Database 'Lodging' created successfully.")

# Select the newly created database
cursor.execute("USE Lodging;")

# Create a new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        password VARCHAR(100),
        type VARCHAR(100)
    ); 
""")
print("Table 'login' created successfully.")
