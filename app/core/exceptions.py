from app.exceptions import APIEception


class NotOwnerException(APIEception):
    description = "没有该照片的权限"
