from app.exceptions import APIEception
from werkzeug.exceptions import Unauthorized


class UserAlreadyExists(APIEception):
    description = "该用户已经存在"


class UserNotExists(APIEception):
    description = "该用户不存在"


class PasswordIncorrect(APIEception):
    description = "密码错误"


class UnauthorizedUser(Unauthorized):
    description = "没有合法的用户权限"
