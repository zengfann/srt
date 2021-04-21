from app.core.models import TrainImage
from marshmallow import Schema, fields
from marshmallow.decorators import post_load
from app.auth.serializers import UserSerializer


class ImageSerializer(Schema):
    type = fields.Str(required=True)
    tag = fields.Str(required=True)
    user = fields.Nested(UserSerializer, dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return TrainImage(**data)


image_schema = ImageSerializer()
images_schema = ImageSerializer(many=True)
