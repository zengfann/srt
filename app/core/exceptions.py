from app.exceptions import APIEception, HTTPException


class NotOwnerException(APIEception):
    code = 401
    description = "没有该照片的权限"


class DatasetDoesntExist(APIEception):
    code = 404

    def __init__(self, id):
        HTTPException.__init__(self, "数据集(%s)不存在" % id)


class LabelException(APIEception):
    code = 400

    def __init__(self, help_text):
        HTTPException.__init__(self, help_text)


class FileDoesntExistException(APIEception):
    code = 404

    def __init__(self, filename):
        HTTPException.__init__(self, "文件(%s)不存在" % filename)


class SampleAlreadyExist(APIEception):
    code = 400

    def __init__(self, filename):
        HTTPException.__init__(self, "样本(%s)已存在" % filename)
