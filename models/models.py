from mongoengine.fields import EmbeddedDocumentField
from bson.objectid import ObjectId
from db import db


class ChildComment(db.EmbeddedDocument):
    content = db.StringField(required=True)
    create_date = db.DateTimeField(required=True)
    user_id = db.StringField(required=True)
    post_id = db.StringField(required=True)



class Comment(db.EmbeddedDocument):
    content = db.StringField(required=True)
    create_date = db.DateTimeField(required=True)
    user_id = db.StringField(required=True)
    post_id = db.StringField(required=True)
    oid = db.ObjectIdField(default=ObjectId)
    reply = db.ListField(EmbeddedDocumentField(ChildComment))


class Post(db.Document):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    create_date = db.DateTimeField(required=True)
    modify_date = db.DateTimeField()
    hits = db.IntField(required=True)
    user = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=30))
    reply = db.MapField(EmbeddedDocumentField(Comment))


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

