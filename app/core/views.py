from datetime import datetime
from io import BytesIO
from os import getenv, path
from uuid import uuid4

from flask import Blueprint, request, send_from_directory
from mongoengine.errors import NotUniqueError
from PIL import Image
from shortuuid import uuid as suuid
from werkzeug.utils import secure_filename

from app.auth.exceptions import UserNotExists
from app.auth.models import User
from app.decorators import with_user
from app.util.labels import validate_labels
from app.util.utils import file_exist
from ml import recognize

from .exceptions import (
    DatasetDoesntExist,
    FileDoesntExistException,
    LabelException,
    ModelAlreadyExist,
    ModelDoesntExist,
    ModelsetDoesntExist,
    NoLabelException,
    NotEnumLabelException,
    NotManagerException,
    NotOwnerException,
    SampleAlreadyExist,
    SampleDoesntExist,
)
from .models import Dataset, Model, Modelset, Sample
from .serializers import (
    DatasetSerializer,
    ModelsetSerializer,
    add_enum_value_dto_schema,
    add_manager_dto_schema,
    dataset_schema,
    model_schema,
    models_schema,
    modelset_schema,
    sample_schema,
    samples_schema,
)

blueprint = Blueprint("core", __name__)

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")


@blueprint.route("/files", methods=("POST",))
@with_user()
def upload_files(user):
    """
    文件上传
    """
    file = request.files["file"]
    id = uuid4()
    filename = str(id) + "." + secure_filename(file.filename)
    file.save(path.join(UPLOAD_FOLDER, filename))
    return {"message": "上传成功", "filename": filename, "mimetype": file.mimetype}


@blueprint.route("/files/<filename>", methods=("GET",))
def static_files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@blueprint.route("/datasets", methods=("GET",))
def get_datasets():
    """
    列出所有数据集
    """
    # 隐藏 labels 信息
    username = request.args.get("user")
    datasets = Dataset.objects.exclude("labels", "managers").all()

    if username is not None:
        user = User.objects.filter(username=username).first()
        if user is not None:
            datasets = datasets.filter(creator=user)
        else:
            datasets = []

    return {
        "results": DatasetSerializer(exclude=["labels", "managers"], many=True).dump(
            datasets
        )
    }


@blueprint.route("/datasets", methods=("POST",))
@with_user(detail=True)
def create_dataset(user):
    """
    创建数据集
    """
    dataset = dataset_schema.load(request.get_json())
    dataset.creator = user
    dataset.managers = []
    dataset.date = datetime.now()
    for label in dataset.labels:
        label["label_id"] = suuid()
    dataset.save()
    return dataset_schema.dump(dataset)


@blueprint.route("/datasets/<objectid:dataset_id>/del_datasets", methods=("DELETE",))
@with_user(detail=True)
def del_dataset(dataset_id, user):
    """
    删除当前数据集
    """
    dataset = Dataset.objects.filter(id=dataset_id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)
    if dataset.can_check(user):
        dataset.delete()
    else:
        raise NotManagerException
    return {"message": "删除成功", "deleted_dataset": dataset_schema.dump(dataset)}, 204


@blueprint.route(
    "/datasets/<objectid:dataset_id>/labels/<label_id>",
    methods=("POST",),
)
@with_user(detail=True)
def add_enum_value(dataset_id, label_id, user):
    """
    添加标签枚举项
    """
    add_enum_value_dto = add_enum_value_dto_schema.load(request.get_json())

    dataset = Dataset.objects.filter(id=dataset_id).first()

    if dataset is None:
        raise DatasetDoesntExist(dataset_id)

    if dataset.creator.id != user.id:
        # 不是自己的数据集不能添加管理员
        raise NotOwnerException

    label = dataset.get_label(label_id)
    if label is None:
        # label 不存在
        raise NoLabelException(label_id)

    if label["type"] != "enum":
        # 不是枚举类型
        raise NotEnumLabelException(label_id)

    for i in range(len(dataset.labels)):
        if dataset.labels[i]["label_id"] == label_id:
            # 使用 set 避免相同的 value 添加到 values
            print(list(dataset.labels[i]["values"]))
            print((add_enum_value_dto["values"]))
            dataset.labels[i]["values"] = list(
                set(dataset.labels[i]["values"] + add_enum_value_dto["values"])
            )

    dataset.save()
    return dataset_schema.dump(dataset)


@blueprint.route("/datasets/<objectid:id>/managers", methods=("PUT",))
@with_user(detail=True)
def add_managers(id, user):
    """
    添加管理员
    """
    add_manager_dto = add_manager_dto_schema.load(request.get_json())
    dataset = Dataset.objects.filter(id=id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)

    if dataset.creator.id != user.id:
        # 不是自己的数据集不能添加管理员
        raise NotOwnerException

    manager = User.objects.filter(username=add_manager_dto["username"]).first()

    if manager is None:
        raise UserNotExists

    else:
        if dataset.creator.id != manager.id and manager not in dataset.managers:
            dataset.managers.append(manager)

    dataset.save()
    return dataset_schema.dump(dataset)


@blueprint.route("/datasets/<objectid:id>", methods=("GET",))
def get_dataset(id):
    dataset = Dataset.objects.filter(id=id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)
    return dataset_schema.dump(dataset)


@blueprint.route("/datasets/<objectid:id>/samples", methods=("POST",))
@with_user(detail=True)
def create_sample(id, user):
    dataset = Dataset.objects.filter(id=id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)
    sample = sample_schema.load(request.get_json())
    sample.dataset = dataset
    sample.checked = True if dataset.can_check(user) else False
    is_valid, help_text = validate_labels(sample, dataset)
    if not is_valid:
        raise LabelException(help_text)
    if not file_exist(sample.file):
        raise FileDoesntExistException(sample.file)

    try:
        sample.save()
    except NotUniqueError:
        raise SampleAlreadyExist(sample.file)
    return sample_schema.dump(sample)


@blueprint.route("/datasets/<objectid:id>/samples", methods=("GET",))
def get_samples(id):
    """
    获取样本
    """
    dataset = Dataset.objects.filter(id=id).first()

    if dataset is None:
        raise DatasetDoesntExist(id)

    samples = Sample.objects.filter(checked=True, dataset=dataset)

    # 筛选出所选样本信息
    for label_id in dataset.get_label_ids():
        label_query = request.args.get(label_id)

        if label_query is None:
            continue

        label = dataset.get_label(label_id)
        if label["type"] == ("enum"):
            samples = samples.filter(
                **{
                    f"labels__{label_id}": label_query,
                }
            )
        elif label["type"] == ("number"):

            arr = []
            arr = label_query.split("-", 2)
            low = int(arr[0])
            high = int(arr[1])
            samples = samples.filter(
                **{f"labels__{label_id}__lte": high, f"labels__{label_id}__gte": low}
            )
    return {"results": samples_schema.dump(samples)}


@blueprint.route("/datasets/<objectid:id>/unchecked_samples", methods=("GET",))
def get_unchecked_samples(id):
    """
    获取未审核样本
    """
    dataset = Dataset.objects.filter(id=id).first()

    if dataset is None:
        raise DatasetDoesntExist(id)

    samples = Sample.objects.filter(checked=False, dataset=dataset)

    return {"results": samples_schema.dump(samples)}


@blueprint.route(
    "/datasets/<objectid:dataset_id>/samples/<objectid:sample_id>", methods=("DELETE",)
)
@with_user(detail=True)
def delete_sample(dataset_id, sample_id, user):
    """
    删除样本
    """

    dataset = Dataset.objects.filter(id=dataset_id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)
    sample = Sample.objects.filter(id=sample_id, dataset=dataset).first()

    if sample is None:
        # 样本不存在
        raise SampleDoesntExist(sample_id)

    if dataset.can_check(user):
        sample.delete()
    else:
        raise NotManagerException

    return {"message": "删除成功", "deleted_sample": sample_schema.dump(sample)}


@blueprint.route(
    "/datasets/<objectid:dataset_id>/samples/<objectid:sample_id>/checked",
    methods=("PUT",),
)
@with_user(detail=True)
def check_sample(dataset_id, sample_id, user):
    """
    审核样本
    """
    dataset = Dataset.objects.filter(id=dataset_id).first()

    if dataset is None:
        raise DatasetDoesntExist(dataset_id)

    sample = Sample.objects.filter(id=sample_id, dataset=dataset).first()

    if sample is None:
        # 样本不存在
        raise SampleDoesntExist(sample_id)

    if dataset.can_check(user):
        sample.checked = True
        sample.save()
    else:
        raise NotManagerException

    return sample_schema.dump(sample)


"""
                        模型管理
"""


@blueprint.route("/modelsets", methods=("POST",))
@with_user(detail=True)
def create_modelset(user):
    """
    创建模型集
    """
    modelset = modelset_schema.load(request.get_json())
    modelset.creator = user
    modelset.date = datetime.now()
    for label in modelset.labels:
        label["label_id"] = suuid()
    modelset.save()
    return modelset_schema.dump(modelset)


@blueprint.route("/modelsets", methods=("GET",))
def get_modelsets():
    """
    列出所有模型集
    """
    # 隐藏 labels 信息
    username = request.args.get("user")
    modelsets = Modelset.objects.exclude(
        "labels",
    ).all()

    if username is not None:
        user = User.objects.filter(username=username).first()
        if user is not None:
            modelsets = modelsets.filter(creator=user)
        else:
            modelsets = []

    return {
        "results": ModelsetSerializer(exclude=["labels"], many=True).dump(modelsets)
    }


@blueprint.route("/modelsets/<objectid:modelset_id>/del_modelsets", methods=("DELETE",))
@with_user(detail=True)
def del_modelset(modelset_id, user):
    """
    删除当前模型集
    """
    modelset = Modelset.objects.filter(id=modelset_id).first()
    if modelset is None:
        raise ModelsetDoesntExist(id)
    if modelset.can_check(user):
        modelset.delete()
    else:
        raise NotManagerException
    return {"message": "删除成功", "deleted_dataset": dataset_schema.dump(modelset)}, 204


@blueprint.route("/modelsets/<objectid:id>/models", methods=("POST",))
@with_user(detail=True)
def create_model(id, user):
    """
    上传模型
    """
    modelset = Modelset.objects.filter(id=id).first()
    print(modelset)
    if modelset is None:
        raise ModelsetDoesntExist(id)
    model = model_schema.load(request.get_json())
    model.modelset = modelset
    try:
        model.save()
    except NotUniqueError:
        raise ModelAlreadyExist(model.file)
    return model_schema.dump(model)


@blueprint.route("/modelsets/<objectid:id>", methods=("GET",))
def get_modelset(id):
    """
    查看单个模型集
    """
    modelset = Modelset.objects.filter(id=id).first()
    if modelset is None:
        raise ModelsetDoesntExist(id)
    return dataset_schema.dump(modelset)


@blueprint.route("/modelsets/<objectid:id>/models", methods=("GET",))
def get_models(id):
    """
    获取模型集模型
    """
    modelset = Modelset.objects.filter(id=id).first()

    if modelset is None:
        raise ModelsetDoesntExist(id)

    models = Model.objects.filter(modelset=modelset)

    # 筛选出所选样本信息
    for label_id in modelset.get_label_ids():
        label_query = request.args.get(label_id)

        if label_query is None:
            continue

        label = modelset.get_label(label_id)
        if label["type"] == ("enum"):
            models = models.filter(
                **{
                    f"labels__{label_id}": label_query,
                }
            )
        elif label["type"] == ("number"):

            arr = []
            arr = label_query.split("-", 2)
            low = int(arr[0])
            high = int(arr[1])
            models = models.filter(
                **{f"labels__{label_id}__lte": high, f"labels__{label_id}__gte": low}
            )
    return {"results": models_schema.dump(models)}


@blueprint.route(
    "/modelsets/<objectid:modelset_id>/models/<objectid:model_id>", methods=("DELETE",)
)
@with_user(detail=True)
def delete_model(modelset_id, model_id, user):
    """
    删除模型
    """

    modelset = Modelset.objects.filter(id=modelset_id).first()
    if modelset is None:
        raise ModelsetDoesntExist(id)
    model = Model.objects.filter(id=model_id, modelset=modelset).first()

    if model is None:
        # 样本不存在
        raise ModelDoesntExist(model_id)

    if modelset.can_check(user):
        model.delete()
    else:
        raise NotManagerException

    return {"message": "删除成功", "deleted_model": model_schema.dump(model)}


@blueprint.route("/upload_test_img", methods=("POST",))
@with_user()
def upload_test_files(user):
    """
    上传测试文件
    """
    file = request.files["file"]
    img_buff = file.read()
    im = Image.open(BytesIO(img_buff))
    r = recognize.recognize(im)
    return {"result": r}
