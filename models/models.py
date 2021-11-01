from db import db


class Post(db.Document):
    title = db.StringField()
    content = db.StringField()


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
