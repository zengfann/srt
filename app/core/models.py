from copy import deepcopy

from mongoengine import (
    DictField,
    Document,
    LazyReferenceField,
    ListField,
    ReferenceField,
    StringField,
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

    def can_check(self, user_id):
        return user_id == self.creator.id

    def get_label(self, label_id):
        for label in self.labels:
            if label["label_id"] == label_id:
                return deepcopy(label)
        return None


class Sample(Document):
    """
    样本模型
    """

    dataset = LazyReferenceField(Dataset, required=True)
    labels = DictField(required=True)
    checked = BooleanField(required=True)
    file = StringField(required=True, unique=True)
