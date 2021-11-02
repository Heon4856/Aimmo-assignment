from models.models import User
from werkzeug.security import check_password_hash


def signup(username, hashed_password):
    user = User(username, hashed_password).save()
    id = user.id
    return id


def login(username, password):
    user = User.objects(username).first()
    if user and check_password_hash(user.password, password) :
        return user.id
    return False