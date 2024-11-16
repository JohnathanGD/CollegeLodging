# College Lodging

## Overview

CollegeLodging is a Flask-based web application designed to help college students find and share housing information. This project enables users to register, log in, and manage their housing details through a user-friendly interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

## Features

- User signup and login functionality
- Database integration with MySQL
- Create, read, update, and delete housing listings
- Search for housing listings
- User profile management

## Technologies Used

- **Frontend**: HTML/CSS, JavaScript, Bootstrap
- **Backend Framework**: Flask
- **Database**: MySQL
- **User Authentication**: Flask-Login
- **Environment Management**: Python-dotenv
- **Password Hashing**: Werkzeug

## Project Structure

```
CollegeLodging/
│
├── backend/
│   ├── __init__.py            # Application factory and initialization
│   ├── config.py              # Configuration class
│   ├── db.py                  # Database connection logic
│   ├── models/
│   │   └── users.py           # User model for authentication
│   ├── blueprints/
│   │   ├── main/
│   │   │   └── routes.py      # Main application routes
│   │   └── auth/
│   │       └── routes.py      # Authentication routes
│   └── templates/             # HTML templates for rendering views
│   └── static/                # Static files (CSS, JS, images)
│   └── setup.py               # Setup script
├── frontend/
│   ├── screens/               # Screens for specific parts of the app
│   │   └── AddApartment.html
│   └── templates/             # Additional templates
│       ├── index.html
│       ├── login.html
│       ├── signup.html
│       ├── header.html
│       └── ApartmentSearch.html
├── .env                        # Environment variables (ignored in Git)
├── .env.example                # Example of environment variables
├── .gitignore                  # Git ignore file
├── requirements.txt            # Project dependencies
├── run_app.py                  # Script to run the Flask application
└── README.md                   # Project documentation
```

## Installation

### Prerequisites

- **Python 3.7+**
- **MySQL Server**
- **pip** (Python package installer)

### Setup Instructions
1. **Clone the Repository**:

```bash
git clone https://github.com/JohnathanGD/CollegeLodging.git
cd CollegeLodging
```

2. **Create a Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**: Copy the `.env.example` file to `.env` and update the values accordingly.
```bash
cp .env.example .env
```

5. **Configure the Database**:
- Ensure MySQL is running and configured to match the credentials in `.env`
- Create the required database and tables if necessary

## Usage

### Running the Application

1. Run the Flask Application: Use the run_app.py script to start the Flask application
```bash
python run_app.py  # On Windows, use py run_app.py if necessary
```
2. Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Authors

- [Kester Mbah](https://github.com/kestermbah) - km21q@fsu.edu
- [Johnathan Gutierrez-Diaz](https://github.com/JohnathanGD)
- [Alex Bundy](https://github.com/AlexBundy)
- [Rodjina Pierre Louis](https://github.com/rxdjina)
- [Christopher Laughlin](https://github.com/Chris-Laughlin)

