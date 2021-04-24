from flask import Blueprint, request, send_from_directory
from app.decorators import with_user
from os import path, getenv
from uuid import uuid4
from .serializers import image_schema, images_schema
from .models import Image
from .exceptions import NotOwnerException

blueprint = Blueprint("core", __name__)

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")


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


@blueprint.route("/images/train/upload", methods=("POST",))
@with_user(detail=True)
def upload_train_image(user):
    image = image_schema.load(request.get_json())
    image.user = user
    image.save()

    return image_schema.dump(image)


@blueprint.route("/images/train/<tag>", methods=("GET",))
@with_user(detail=True)
def display_train_image(user, tag):
    images = Image.objects(user=user, image_type="train", tag=tag)

    return {"result": images_schema.dump(images)}


@blueprint.route("/images/test/<int:tag>", methods=("GET",))
@with_user(detail=True)
def display_test_image(user, tag):
    images = Image.objects(user=user, image_type="test", tag=tag)

    return {"result": images_schema.dump(images)}


@blueprint.route("/images/delete/<id>", methods=("DELETE",))
@with_user(detail=True)
def delete_images(user, id):
    delete_image = Image.objects.get(id=id)
    if delete_image.user != user:
        raise NotOwnerException
    delete_image.delete()
    return {"result": "删除成功"}
