from mongoengine import Document, StringField, ReferenceField, IntField, UUIDField
from app.auth.models import User


class Image(Document):
    """
    训练集图片信息
    病害的种类
    """

    image_type = StringField(required=True)  # 图片是train or test 集
    operate = IntField(required=True)  # test集选择哪种强化处理
    tag = StringField(required=True)  # 病害的种类
    user = ReferenceField(User, required=True)
    image_uuid = UUIDField(required=True)  # 上传到目录的文件名
