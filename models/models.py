from db import db


class Post(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    create_date = db.DateTimeField(required=True)
    modify_date = db.DateTimeField()
    user = db.StringField(required=True)


class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    signup_date = db.DateTimeField(required=True)
