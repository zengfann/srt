from mongoengine import (
    DateTimeField,
    Document,
    ReferenceField,
    StringField,
)

from app.auth.models import User


class Train(Document):
    stdout = StringField()
    stderr = StringField()
    status = StringField()
    date = DateTimeField(required=True)
    creator = ReferenceField(User, required=True)
