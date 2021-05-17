from copy import deepcopy

from mongoengine import (
    CASCADE,
    DateTimeField,
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
    description = StringField(required=True)
    date = DateTimeField(required=True)
    creator = ReferenceField(User, required=True)
    labels = ListField(DictField(), required=True)
    managers = ListField(LazyReferenceField(User), default=[])

    def can_check(self, user):
        return user.id == self.creator.id or user in self.managers

    def get_label(self, label_id):
        for label in self.labels:
            if label["label_id"] == label_id:
                return deepcopy(label)
        return None

    def get_label_ids(self):
        return set(map(lambda x: x["label_id"], self.labels))


class Sample(Document):
    """
    样本模型
    """

    dataset = LazyReferenceField(Dataset, required=True, reverse_delete_rule=CASCADE)
    labels = DictField(required=True)
    checked = BooleanField(required=True)
    file = StringField(required=True, unique=True)
