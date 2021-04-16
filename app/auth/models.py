from mongoengine import Document, StringField


class User(Document):
    username = StringField(required=True, max_length=256)
    password = StringField(required=True, max_length=256)
