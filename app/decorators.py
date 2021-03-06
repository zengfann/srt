from functools import wraps
from os import getenv
from re import split

import jwt
from flask import request
from jwt.exceptions import DecodeError, InvalidSignatureError

from app.auth.models import User

from .auth.exceptions import UnauthorizedUser

JWT_SECRET = getenv("JWT_SECRET")


def with_user(detail=False):
    """
    注入当前用户

    参数 detail: 如果设置为True会返回用户详细信息（数据库查询），
    正常只会返回用户的用户名比如：
    {
        "username": "jack"
    }
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token is None:
                raise UnauthorizedUser

            parsed = split(r"\s", token.strip())

            if parsed[0] != "Bearer":
                raise UnauthorizedUser

            try:
                user = jwt.decode(parsed[1], JWT_SECRET, "HS256")
            except (InvalidSignatureError, DecodeError):
                # token 错误
                raise UnauthorizedUser

            if detail:
                user = User.objects.get(username=user["username"])

            return f(*args, **kwargs, **{"user": user})

        return wrapper

    return decorator
