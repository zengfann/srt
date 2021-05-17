from marshmallow import Schema, fields
from marshmallow.decorators import post_load
from marshmallow_oneofschema import OneOfSchema

from app.auth.serializers import UserSerializer
from app.core.models import Dataset, Sample


class LazyReferenceSerializer(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value.id)


class EnumLabelSerializer(Schema):
    label_id = fields.String(
        dump_only=True,
    )
    label_name = fields.String(required=True)
    description = fields.String(required=True)
    values = fields.List(fields.String(), required=True)

    @post_load
    def make_label(self, data, **kwargs):
        data["type"] = "enum"
        return data


class NumberLabelSerializer(Schema):
    label_id = fields.String(dump_only=True)
    label_name = fields.String(required=True)
    description = fields.String(required=True)
    min_num = fields.Number()
    max_num = fields.Number()

    @post_load
    def make_label(self, data, **kwargs):
        data["type"] = "number"
        return data


class LabelSerializer(OneOfSchema):
    type_field = "type"
    type_schemas = {"enum": EnumLabelSerializer, "number": NumberLabelSerializer}

    def get_obj_type(self, obj):
        return obj["type"]


class DatasetSerializer(Schema):
    """
    数据集序列化器
    """

    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    date = fields.DateTime()
    creator = fields.Nested(UserSerializer, required=True, dump_only=True)
    labels = fields.List(fields.Nested(LabelSerializer), required=True)
    # 创建时不需要指定管理员
    managers = fields.List(LazyReferenceSerializer(), required=True, dump_only=True)

    @post_load
    def make_dataset(self, data, **kwargs):
        return Dataset(**data)


class SampleSerializer(Schema):
    """
    样本模型序列化器
    """

    id = fields.String(dump_only=True)
    dataset = LazyReferenceSerializer(dump_only=True)
    labels = fields.Mapping(fields.String(), None, required=True)
    # 创建时不需要指定是否过审
    checked = fields.Boolean(dump_only=True)
    file = fields.String(required=True)

    @post_load
    def make_sample(self, data, **kwargs):
        return Sample(**data)


class AddManagerDtoSerializer(Schema):
    username = fields.String(required=True)


dataset_schema = DatasetSerializer()
datasets_schema = DatasetSerializer(many=True)

sample_schema = SampleSerializer()
samples_schema = SampleSerializer(many=True)

add_manager_dto_schema = AddManagerDtoSerializer()
