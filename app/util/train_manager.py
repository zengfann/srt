from app.core.models import Image
from os import getenv, path
from shutil import copyfile
from threading import Thread
from time import sleep


UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
TRAIN_FOLDER = getenv("TRAIN_FOLDER")


class TrainManager:
    """
    训练管理器,一个时间只能有一个训练任务进行
    """

    def __init__(self):
        # 当前是否正在训练
        self.training = False
        self.train_thread = None
        self.current_user = None
        self.logs = []

    def copy_samples(self, user):
        for tag in range(0, 10):
            images = Image.objects(user=user, image_type="train", tag=tag)
            for image in images:
                image_path = path.join(UPLOAD_FOLDER, str(image.image_uuid))
                print(image_path)
                copyfile(
                    image_path,
                    path.join(
                        TRAIN_FOLDER,
                        "identify",
                        str(tag),
                        str(image.image_uuid) + ".jpg",
                    ),
                )

    def train(self, user):
        """
        开始训练
        """
        if not self.training:
            self.training = True
            self.current_user = user
            # 拷贝该用户的训练集
            # self.copy_samples(user)
            self.train_thread = Thread(target=self.do_train)
            self.train_thread.start()
        else:
            print("已经有训练任务")

    def stop_train(self):
        """
        停止训练
        """
        self.training = False
        self.logs = []
        self.train_thread = None
        self.current_user = None
        print("训练结束")

    def log(self, s):
        self.logs.append(s)

    def get_logs(self):
        return self.logs

    def get_current_user(self):
        return self.current_user

    def do_train(self):
        # fake train
        for i in range(15):
            self.log("训练中...现在是第%d秒" % (i + 1))
            sleep(1)
        self.stop_train()


manager = TrainManager()
