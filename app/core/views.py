from math import ceil
from flask import Blueprint, request, send_from_directory
from app.decorators import with_user
from os import path, getenv
from uuid import uuid4
from .serializers import image_schema, images_schema
from .models import Image
from .exceptions import NotOwnerException, ImageDoesntExist
from os.path import isfile
from app.util.train_manager import manager

blueprint = Blueprint("core", __name__)

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
TRAIN_FOLDER = getenv("TRAIN_FOLDER")


@blueprint.route("/image/upload", methods=("POST",))
@with_user()
def upload_image(user):
    """
    图片上传
    """
    file = request.files["file"]
    id = uuid4()
    file.save(path.join(UPLOAD_FOLDER, str(id)))
    return {"message": "上传成功", "url": "/images/%s" % (id)}


@blueprint.route("/images/<uuid:id>", methods=("GET",))
def images(id):
    """
    显示用户上传的图片
    """
    return send_from_directory(UPLOAD_FOLDER, str(id), mimetype="image/jpg")


@blueprint.route("/images/train_test/upload", methods=("POST",))
@with_user(detail=True)
def upload_train_image(user):
    """
    上传用户样本图片
    """
    image = image_schema.load(
        request.get_json(),
        partial=(
            "operate",
            "train_type",
            "mask_type",
        ),
    )
    id = image.image_uuid
    if not isfile(path.join(UPLOAD_FOLDER, str(id))):
        raise ImageDoesntExist(id)
    image.user = user
    image.operate = -1  # 初始化operate为-1
    image.save()
    return image_schema.dump(image)


"""
图片识别训练集
"""


@blueprint.route("/images/train_identify/<tag>", methods=("GET",))
@with_user(detail=True)
def display_train_identify(user, tag):
    page = request.args.get("page")
    page_size = request.args.get("page_size")
    if page is None:
        page = 1
    if page_size is None:
        page_size = 2
    page = int(page)
    page_size = int(page_size)
    images = Image.objects(
        user=user, image_type="train", train_type="identify", tag=tag
    )
    count = images.count()
    images = images[(page - 1) * page_size : page * page_size]
    return {
        "result": images_schema.dump(images),
        "pages": ceil(count / page_size),
        "current_page": page,
    }


"""
图片病斑训练集
"""


@blueprint.route("/images/train_mask/<mask_type>/<tag>", methods=("GET",))
@with_user(detail=True)
def display_train_mask(user, tag, mask_type):
    page = request.args.get("page")
    page_size = request.args.get("page_size")
    if page is None:
        page = 1
    if page_size is None:
        page_size = 2
    page = int(page)
    page_size = int(page_size)
    images = Image.objects(
        user=user, image_type="train", train_type="mask", mask_type=mask_type, tag=tag
    )
    count = images.count()
    images = images[(page - 1) * page_size : page * page_size]
    return {
        "result": images_schema.dump(images),
        "pages": ceil(count / page_size),
        "current_page": page,
    }


# @blueprint.route("/images/test/<int:tag>", methods=("GET",))
# @with_user(detail=True)
# def display_test_image(user, tag):
#     page = request.args.get("page")
#     page_size = request.args.get("page_size")
#     if page is None:
#         page = 1
#     if page_size is None:
#         page_size = 2
#     page = int(page)
#     page_size = int(page_size)
#     images = Image.objects(user=user, image_type="test", tag=tag)
#     count = images.count()
#     images = images[(page - 1) * page_size : page * page_size]
#     return {
#         "result": images_schema.dump(images),
#         "pages": ceil(count / page_size),
#         "current_page": page,
#     }


# @blueprint.route("file/download",methods=("POST",))
# @with_user(detail=True)
# def download_model(user):


@blueprint.route("/images/delete/<id>", methods=("DELETE",))
@with_user(detail=True)
def delete_images(user, id):
    delete_image = Image.objects.get(id=id)
    if delete_image.user != user:
        raise NotOwnerException
    delete_image.delete()
    return {"result": "删除成功"}


@blueprint.route("/start_train", methods=("POST",))
@with_user(detail=True)
def train_images_copy(user):
    manager.train(user)
    return "复制成功"


@blueprint.route("/train_status", methods=("GET",))
@with_user(detail=True)
def get_current_train_status(user):
    current_user = manager.get_current_user()
    if user == current_user:
        return {"logs": manager.get_logs()}
    else:
        return {"error": "当前没有训练任务"}, 400
