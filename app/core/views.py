from os import getenv, path
from uuid import uuid4

from flask import Blueprint, request, send_from_directory
from mongoengine.errors import NotUniqueError
from shortuuid import uuid as suuid
from werkzeug.utils import secure_filename

from app.decorators import with_user
from app.util.labels import validate_labels
from app.util.utils import file_exist

from .exceptions import (
    DatasetDoesntExist,
    FileDoesntExistException,
    LabelException,
    SampleAlreadyExist,
)
from .models import Dataset, Sample
from .serializers import dataset_schema, datasets_schema, sample_schema

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
    return {"message": "上传成功", "filename": filename}


@blueprint.route("/files/<filename>", methods=("GET",))
def static_files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@blueprint.route("/datasets", methods=("GET",))
def get_datasets():
    datasets = Dataset.objects.all()
    return {"results": datasets_schema.dump(datasets)}


@blueprint.route("/datasets", methods=("POST",))
@with_user(detail=True)
def create_dataset(user):
    """
    创建数据集
    """
    dataset = dataset_schema.load(request.get_json())
    dataset.creator = user
    dataset.managers = []
    for label in dataset.labels:
        label["label_id"] = suuid()
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
    sample.checked = True if dataset.can_check(user.id) else False
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
    dataset = Dataset.objects.filter(id=id).first()
    if dataset is None:
        raise DatasetDoesntExist(id)
    Sample.objects.filter(checked=True)
