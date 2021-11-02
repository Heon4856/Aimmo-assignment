from db import db


class Post(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    create_date = db.DateTimeField(required=True)
    modify_date = db.DateTimeField()
    hits = db.IntField(required=True)
    user = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=30))

    meta = {
        'indexes': [
            {'fields' : ['$title']
             }
        ]
    }

class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    signup_date = db.DateTimeField(required=True)
