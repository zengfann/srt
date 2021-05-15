from mongoengine import Document, StringField


class User(Document):
    username = StringField(required=True, max_length=256, unique=True)
    password = StringField(required=True, max_length=256)
    user_type = StringField(required=True, max_length=256)
