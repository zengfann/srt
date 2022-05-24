from flask import Blueprint
from app.decorators import with_user
from app.train.models import Train
from datetime import datetime

blueprint = Blueprint("train", __name__)


@blueprint.route("/train", methods=("POST",))
@with_user(detail=True)
def new_train(user):
    """
    创建一次训练
    """
    train = Train()
    train.date = datetime.now()
    train.creator = user
    train.save()
    return 
