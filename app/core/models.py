from mongoengine import Document, StringField, ReferenceField, FileField
from app.auth.models import User


class Image(Document):
    """
    图片的分类：
    训练集 测试集 病害种类
    """
    type = StringField(required=True)
    tag = StringField(required=True)
    user = ReferenceField(User, required=True)
