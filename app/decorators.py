from flask import request
from .auth.exceptions import UnauthorizedUser
from os import getenv
from jwt.exceptions import InvalidSignatureError, DecodeError
from re import split
from app.auth.models import User

import jwt

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

            return f(user, *args, **kwargs)

        return wrapper

    return decorator
