from marshmallow import Schema, fields
from app.auth.serializers import UserSerializer
from .models import Image


class ImageSerializer(Schema):
    type = fields.Str(required=True)
    tag = fields.Str(required=True)
    user = fields.Nested(UserSerializer, dump_only=True)


image_schema = ImageSerializer()
images_schema = ImageSerializer(many=True)
