from models.models import User
from werkzeug.security import check_password_hash


def signup(name, hashed_password, signup_date):
    user = User(name=name, password=hashed_password, signup_date=signup_date).save()
    print(hashed_password)
    print(user.password)
    id = user.id
    return id


def login(name, password):
    user = User.objects(name=name).first()
    if user and check_password_hash(user.password, password):
        return user.id
    return False
