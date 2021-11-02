from repository import auth_repository
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash



def signup(username, password):
    hashed_password=generate_password_hash(password)
    return auth_repository.signup(username, hashed_password)


def login(username, password):
    user_id = auth_repository.login(username, password)
    if user_id:
        return create_access_token(user_id)
    return False