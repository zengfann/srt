from mongoengine import Document, StringField, ReferenceField, FileField
from app.auth.models import User


class Image(Document):
    type = StringField(required=True)
    tag = StringField(required=True)
    user = ReferenceField(User, required=True)
