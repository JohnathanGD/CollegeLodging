from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import get_db_connection
import utils.queries as queries

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, password_hash, is_admin=False, roles=[]):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = password_hash  
        self.is_admin = is_admin
        self.roles = []
    
    @staticmethod
    def get_by_id(user_id): # Get user by ID
        params = (user_id,)
        user_data = queries.execute_query_with_results(queries.GET_USER_BY_ID, params, dictionary=True, fetch_one=True)
        if user_data:
            user = User(
                id=user_data['id'],
                email=user_data['email'],
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                password_hash=user_data['password'],
                is_admin=user_data['is_admin'],
            )

            user.roles = user.get_roles()

            return user
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
                password_hash=user_data['password'],
                is_admin=user_data['is_admin'],
            )
            
        return None

    def get_roles(self): # Get user roles
        params = (self.id,)
        roles = queries.execute_query_with_results(queries.GET_USER_ROLES, params, dictionary=True)
        if roles:
            self.roles = roles
        return self.roles
    
    def add_role(self, role_id): # Add user role
        params = (self.id, role_id)
        queries.execute_query(queries.ADD_USER_ROLE, params)
        self.get_roles()
    
    def remove_role(self, role_id): # Remove user role
        params = (self.id, role_id)
        queries.execute_query(queries.REMOVE_USER_ROLE, params)
        self.get_roles()
    
    def is_admin(self): # Check if user is admin
        return self.is_admin
    

    def set_password(self, password): # Set password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # Check password
        return check_password_hash(self.password_hash, password)