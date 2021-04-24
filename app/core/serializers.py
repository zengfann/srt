from app.core.models import Image
from marshmallow import Schema, fields
from marshmallow.decorators import post_load


class ImageSerializer(Schema):
    image_type = fields.Str(required=True)
    operate = fields.Int(required=True)
    tag = fields.Str(required=True)
    image_uuid = fields.UUID(required=True)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)


image_schema = ImageSerializer()
images_schema = ImageSerializer(many=True)
