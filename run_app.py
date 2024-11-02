import os
import subprocess
import sys
import platform

def run_command(command):
    """Run a shell command in a cross-platform way."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def check_and_install_requirements():
    """Check if all requirements are installed, prompt the user to install if missing."""
    try:
        import flask
        import flask_login
        import mysql.connector
        import dotenv  
        import werkzeug     
    except ImportError as e:
        package_name = str(e).split("'")[1]  # Extract missing package name
        print(f"Package '{package_name}' is not installed.")

        # Ask the user to install the requirements
        install = input("Would you like to install all requirements? (y/n): ").strip().lower()
        if install == 'y':
            python_cmd = 'py' if platform.system() == 'Windows' else 'python3'
            run_command(f"{python_cmd} -m pip install -r requirements.txt")
        else:
            print("Please install the required packages manually and re-run the script.")
            sys.exit(1)

def main():
    # Ensure requirements are installed
    check_and_install_requirements()

    # Set the FLASK_APP environment variable
    os.environ['FLASK_APP'] = 'backend:create_app'
    os.environ['FLASK_ENV'] = 'development'

    # Run the Flask application
    print("Starting the Flask application...")
    python_cmd = 'py' if platform.system() == 'Windows' else 'python3'
    run_command(f"{python_cmd} -m flask run")

if __name__ == "__main__":
    main()