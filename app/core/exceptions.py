from app.exceptions import APIEception, HTTPException


class NotOwnerException(APIEception):
    code = 401
    description = "没有该数据集的权限"


class NotManagerException(APIEception):
    code = 401
    description = "你不是该数据集的管理员"


class DatasetDoesntExist(APIEception):
    code = 404

    def __init__(self, id):
        HTTPException.__init__(self, "数据集(%s)不存在" % id)


class ModelsetDoesntExist(APIEception):
    code = 404

    def __init__(self, id):
        HTTPException.__init__(self, "模型集(%s)不存在" % id)


class SampleDoesntExist(APIEception):
    code = 404

    def __init__(self, id):
        HTTPException.__init__(self, "样本(%s)不存在" % id)


class ModelDoesntExist(APIEception):
    code = 404

    def __init__(self, id):
        HTTPException.__init__(self, "模型(%s)不存在" % id)


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


class ModelAlreadyExist(APIEception):
    code = 400

    def __init__(self, filename):
        HTTPException.__init__(self, "样本(%s)已存在" % filename)


class NoLabelException(APIEception):
    code = 404

    def __init__(self, label_id):
        HTTPException.__init__(self, "标签(%s)不存在" % label_id)


class NotEnumLabelException(APIEception):
    code = 400

    def __init__(self, label_id):
        HTTPException.__init__(self, "标签(%s)不是一个枚举类型" % label_id)
