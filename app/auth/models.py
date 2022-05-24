from mongoengine import Document, StringField, EmailField


class User(Document):
    username = StringField(required=True, max_length=256, unique=True)
    password = StringField(required=True, max_length=256)
    email = EmailField(required=True, unique=True)
