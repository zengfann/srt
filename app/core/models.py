from mongoengine import Document, StringField, ReferenceField
from app.auth.models import User


class Image(Document):
    """
    图片的分类：
    训练集 测试集 病害种类
    """

    type = StringField(required=True)
    tag = StringField(required=True)
    user = ReferenceField(User, required=True)


class TrainImage(Document):
    """
    训练集图片信息
    病害的种类
    """

    type = StringField(required=True)  # 图片是train or test 集
    tag = StringField(required=True)  # 病害的种类
    user = ReferenceField(User, required=True)


class TestImage(Document):
    """
    强化后测试集的图片：
    处理类型、病害种类
    """

    type = StringField(required=True)  # 图片是train or test 集
    operate = StringField(required=True)  # test集选择哪种强化处理
    tag = StringField(required=True)  # 病害的种类
    user = ReferenceField(User, required=True)
