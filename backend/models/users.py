from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import get_db_connection
import utils.queries as queries

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, password_hash):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = password_hash
    
    @staticmethod
    def get_by_id(user_id): # Get user by ID
        params = (user_id,)
        user_data = queries.execute_query_with_results(queries.GET_USER_BY_ID, params, dictionary=True, fetch_one=True)
        if user_data:
            return User(
                id=user_data['id'],
                email=user_data['email'],
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                password_hash=user_data['password']
            )
        return None

    @staticmethod
    def get_by_email(email): # Get user by email
        params = (email,)
        user_data = queries.execute_query_with_results(queries.GET_USER_BY_EMAIL, params, dictionary=True, fetch_one=True)
        if user_data:
            return User(
                id=user_data['id'],
                email=user_data['email'],
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                password_hash=user_data['password']
            )
        return None

    def set_password(self, password): # Set password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # Check password
        return check_password_hash(self.password_hash, password)