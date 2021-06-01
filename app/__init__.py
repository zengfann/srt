from os import environ
from pathlib import Path

from flask import Flask, json
from marshmallow.exceptions import ValidationError
from mongoengine import connect
from stackprinter import set_excepthook, show
from werkzeug.exceptions import HTTPException

from app import auth, core
from app.util.converters import ObjectIDConverter

# 设置更好的报错
set_excepthook(style="darkbg2")

# 连接数据库
connect(host=environ["MONGODB_HOST"])


def handle_exception(e):
    show(style="darkbg2")
    response = json.jsonify(
        {
            "code": 500,
            "name": "INTERNAL SERVER ERROR",
        }
    )
    response.status_code = 500
    return response


def create_app():
    app = Flask(__name__, root_path=Path(__file__).parent.parent)
    app.url_map.converters["objectid"] = ObjectIDConverter

    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(core.views.blueprint)
    app.handle_exception = handle_exception

    @app.route("/")
    def hello_world():
        return {"message": "Hello, World!"}

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_exception(e):
        return {"code": 400, "errors": e.messages}, 400

    return app
