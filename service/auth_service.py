import datetime

from repository import auth_repository
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


def signup(username, password):
    hashed_password = generate_password_hash(password)
    signup_date = datetime.datetime.now()
    return auth_repository.signup(username, hashed_password, signup_date)


def login(name, password):
    user_id = auth_repository.login(name, password)
    if user_id:
        return create_access_token(str(user_id))
    return False
