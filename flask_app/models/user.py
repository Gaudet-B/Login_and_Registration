from werkzeug.utils import redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        first_name = user['first_name_input']
        last_name = user['last_name_input']
        user_email = user['email_input']
        confirm = user['confirm_input']
        query = "SELECT email FROM users;"
        emails = connectToMySQL('login_and_registration_schema').query_db(query)
        print("PRINT:", emails)
        if not EMAIL_REGEX.match(user['email_input']):
            flash("invalid email address.")
            is_valid = False
        if len(user['first_name_input']) < 2:
            flash("first name must be at least two characters long.")
            is_valid = False
        if not first_name.isalpha():
            flash("first name must only contain alphabetical characters.")
            is_valid = False
        if len(user['last_name_input']) < 2:
            flash("first name must be at least two characters long.")
        if not last_name.isalpha():
            flash("last name must only contain alphabetical characters.")
            is_valid = False
        for email in emails:
            print(email)
            print(user_email)
            if user_email == email['email']:
                flash("a user with this email address already exists.")
                is_valid = False
        if len(user['password_input']) < 8:
            flash("password must be at least 8 characters long")
            is_valid = False
        if confirm != user['password_input']:
            flash("passwords do not match.")
            is_valid = False
        return is_valid

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('login_and_registration_schema').query_db(query, data)

    @classmethod
    def get_email(cls, data):
        query = "SELECT email FROM users;"
        return connectToMySQL('login_and_registration_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL('login_and_registration_schema').query_db(query)