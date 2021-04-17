from app.exceptions import APIEception


class UserAlreadyExists(APIEception):
    description = "该用户已经存在"


class UserNotExists(APIEception):
    description = "该用户不存在"


class PasswordIncorrect(APIEception):
    description = "密码错误"