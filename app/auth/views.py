from flask import Blueprint
from flask import request
from .models import User
from .serializers import user_schema
from .exceptions import UserAlreadyExists, UserNotExists, PasswordIncorrect
from mongoengine.errors import NotUniqueError, DoesNotExist

blueprint = Blueprint("auth", __name__)


@blueprint.route("/signup", methods=("POST",))
def signup():
    """
    用户注册
    """
    user = user_schema.load(request.get_json())
    try:
        user.save()
    except NotUniqueError:
        raise UserAlreadyExists
    return user_schema.dump(user)


@blueprint.route("/signin", methods=("POST",))
def signin():
    """
    用户登录
    """
    login_user = user_schema.load(request.get_json())
    try:
        user = User.objects.get(username=login_user.username)
    except DoesNotExist:
        raise UserNotExists
    if user.password == login_user.password:
        return {"message": "登录成功"}
    else:
        raise PasswordIncorrect
