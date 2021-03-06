from werkzeug.exceptions import Unauthorized

from app.exceptions import APIEception


class UserAlreadyExists(APIEception):
    description = "该用户已经存在"


class UserNotExists(APIEception):
    description = "该用户不存在"


class PasswordIncorrect(APIEception):
    description = "密码错误"


class UnauthorizedUser(Unauthorized):
    description = "没有合法的用户权限"


class NotAdmin(Unauthorized):
    description = "您不是管理员"
