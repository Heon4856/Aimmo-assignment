from db import db


class Post(db.Document):
    id = db.IntegerField()
    subject = db.Stringfield()
    content = db.Stringfield()


class User(db.Document):
    id = db.IntegerField()
    name = db.StringField()
    email = db.StringField()
