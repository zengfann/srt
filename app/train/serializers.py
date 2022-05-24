from marshmallow import Schema, fields
from marshmallow.decorators import post_load
from marshmallow.validate import Length
from marshmallow_oneofschema import OneOfSchema

from app.auth.serializers import UserSerializer
from app.core.models import Dataset, Model, Modelset, Sample


class TrainSerializer(Schema):
    date = fields.DateTime()
    stdout = fields.String()
    stdin = fields.String()
