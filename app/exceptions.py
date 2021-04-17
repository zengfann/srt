from werkzeug.exceptions import HTTPException


class APIEception(HTTPException):
    code = 400
    description = "API Exception"
    name = "API 错误"
