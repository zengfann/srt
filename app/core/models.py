from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DictField,
    ListField,
)
from mongoengine.fields import BooleanField
from app.auth.models import User


class Dataset(Document):
    """
    数据集模型
    """

    name = StringField(required=True)
    creator = ReferenceField(User, required=True)
    labels = ListField(DictField(), required=True)
    managers = ListField(ReferenceField(User), default=[])


class Sample(Document):
    """
    样本模型
    """

    dataset = ReferenceField(Dataset, required=True)
    labels = DictField(required=True)
    checked = BooleanField(required=True)
