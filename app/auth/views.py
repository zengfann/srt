from os import environ

import jwt
from flask import Blueprint, request
from mongoengine.errors import DoesNotExist, NotUniqueError

from app.decorators import with_user

from .exceptions import PasswordIncorrect, UserAlreadyExists, UserNotExists, NotAdmin
from .models import User
from .serializers import user_schema, users_schema

blueprint = Blueprint("auth", __name__)

JWT_SECRET = environ["JWT_SECRET"]


@blueprint.route("/signup", methods=("POST",))
def signup():
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
    login_user = user_schema.load(
        request.get_json(),
        partial=("user_type", "email"),
    )
    try:
        user = User.objects.get(username=login_user.username)
    except DoesNotExist:
        raise UserNotExists
    if user.password == login_user.password:
        token = jwt.encode({"username": user.username}, JWT_SECRET)
        return {"message": "登录成功", "access_token": token, "user_id": str(user.id)}
    else:
        raise PasswordIncorrect


@blueprint.route("/current_user", methods=("GET",))
@with_user(detail=True)
def get_current_user(user):
    """
    获取当前登录用户
    """
    return user_schema.dump(user)


@blueprint.route("/all_users", methods=("GET",))
def get_all_users():
    """
    获取所有用户
    """
    return {"results": users_schema.dump(User.objects)}


@blueprint.route("/change_user/<username>", methods=("POST",))
def change_user(username):
    """
    更改用户信息
    """
    changedUser = user_schema.load(
        request.get_json(),
        partial=("password",),
    )
    try:
        user = User.objects.get(username=username)
    except DoesNotExist:
        raise UserNotExists
    user.username = changedUser.username
    user.email = changedUser.email
    try:
        user.save()
    except NotUniqueError:
        raise UserAlreadyExists
    return user_schema.dump(user)


@blueprint.route("/users/<username>", methods=("DELETE",))
@with_user(detail=True)
def delete_user(username, user):
    if user.username == "admin":
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return None
        user.delete()
        return None
    else:
        raise NotAdmin
