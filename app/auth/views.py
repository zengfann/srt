from flask import Blueprint
from flask import request

blueprint = Blueprint("auth", __name__)


@blueprint.route("/signup", methods=("POST",))
def signup():
    """
    用户注册
    """
    user = request.get_json()
    return user
