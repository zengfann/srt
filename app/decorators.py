from flask import request
from .auth.exceptions import UnauthorizedUser
from os import getenv
from jwt.exceptions import InvalidSignatureError, DecodeError
from re import split

import jwt

JWT_SECRET = getenv("JWT_SECRET")


def with_user(f):
    """
    注入当前用户
    """

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

        return f(user, *args, **kwargs)

    return wrapper
