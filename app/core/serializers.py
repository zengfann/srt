from marshmallow import Schema, fields
from marshmallow.decorators import post_load

from app.core.models import Image


class ImageSerializer(Schema):
    id = fields.Str(required=True, dump_only=True)
    image_type = fields.Str(required=True)
    operate = fields.Int(required=True)
    tag = fields.Int(required=True)
    image_uuid = fields.UUID(required=True)
    train_type = fields.Str(required=True)
    mask_type = fields.Str(required=True)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)


image_schema = ImageSerializer()
images_schema = ImageSerializer(many=True)


# class DatasetSerializer(Schema):

#     type = fields.Str(Required=True)  # 是识别还是病斑数据集
#     name = fields.Str(Required=True)  # 植物的种类
#     creater = fields.(User)  # 数据集的创始人
#     labels = fields.Dict(Required=True)  # 种类的数据集字典
#     managers = List(ObjectIdField)  # 管理人员
