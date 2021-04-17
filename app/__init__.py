from flask import Flask, json, Response
from dotenv import load_dotenv
from mongoengine import connect
from traceback import format_list
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException, InternalServerError
from os import environ

import sys

from app import auth

# 加载环境变量
load_dotenv()

# 连接数据库
connect(host=environ["MONGODB_HOST"])


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth.views.blueprint)

    @app.route("/")
    def hello_world():
        return {"message": "Hello, World!"}

    @app.errorhandler(Exception)
    def handle_exception(e):
        return {
            "code": 500,
            "message": repr(e),
            "descripton": InternalServerError.description,
        }, 500

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
        return {"code": 400, "data": e.data, "errors": e.messages}, 400

    return app
