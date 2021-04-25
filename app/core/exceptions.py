from app.exceptions import APIEception, HTTPException


class NotOwnerException(APIEception):
    code = 401
    description = "没有该照片的权限"


class ImageDoesntExist(APIEception):
    code = 404
    description = "没这个图片草泥马"

    def __init__(self, id):
        self.description = "图片(%s)不存在,草泥马" % (id)
        HTTPException.__init__(self, self.description)
