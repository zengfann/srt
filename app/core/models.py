from typing import List
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    IntField,
    UUIDField,
    DictField,
    document,
)
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import BooleanField
from app.auth.models import User


class Image(Document):
    """
    图片模型
    """

    image_type = StringField(required=True)  # 图片是哪种植物
    train_type = StringField(required=True)  # 选择训练集是识别类的还是病斑类的
    mask_type = StringField(required=True)  # 病斑训练图是标注图还是原图
    tag = IntField(required=True)  # 病害的种类
    user = ReferenceField(User, required=True)
    operate = IntField(required=True)  # test集选择哪种强化处理
    image_uuid = UUIDField(required=True)  # 上传到目录的文件名


class Dataset(Document):

    """
    数据集模型
    """

    type = StringField(Required=True)  # 是识别还是病斑数据集
    name = StringField(Required=True)  # 植物的种类
    creater = ReferenceField(User, Required=True)  # 数据集的创始人
    labels = DictField(Required=True)  # 种类的数据集字典
    managers = List(ObjectIdField)  # 管理人员


class Images(document):
    """
    图片模型
    """

    Dataset = StringField(Required=True)
    labels = DictField(Required=True)
    checked = BooleanField(Required=True)
