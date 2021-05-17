from bson.objectid import InvalidId, ObjectId
from werkzeug.routing import BaseConverter, ValidationError


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)

        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return str(value)
