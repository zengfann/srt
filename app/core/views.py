from app.core.models import Dataset
from flask import Blueprint, request, send_from_directory
from app.decorators import with_user
from os import path, getenv
from uuid import uuid4
from .serializers import dataset_schema, datasets_schema

blueprint = Blueprint("core", __name__)

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
TRAIN_FOLDER = getenv("TRAIN_FOLDER")


@blueprint.route("/files", methods=("POST",))
@with_user()
def upload_files():
    """
    文件上传
    """
    file = request.files["file"]
    id = uuid4()
    filename = str(id) + "." + file.filename
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
    dataset.save()
    return dataset_schema.dump(dataset)
