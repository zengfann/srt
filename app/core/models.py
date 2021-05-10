from mongoengine import Document, StringField, ReferenceField, IntField, UUIDField
from app.auth.models import User


class Image(Document):
    """
    训练集与测试集图片信息
    病害的种类
    """

    image_type = StringField(required=True)  # 图片是train or test 集
    train_type = StringField(required=True)  # 选择训练集是识别类的还是病斑类的
    mask_type = StringField(required=True)  # 病斑训练图是标注图还是原图
    tag = IntField(required=True)  # 病害的种类
    user = ReferenceField(User, required=True)
    operate = IntField(required=True)  # test集选择哪种强化处理
    image_uuid = UUIDField(required=True)  # 上传到目录的文件名
