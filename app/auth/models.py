from mongoengine import Document, StringField, ReferenceField


class User(Document):
    username = StringField(required=True, max_length=256, unique=True)
    password = StringField(required=True, max_length=256)
