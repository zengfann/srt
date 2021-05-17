from os import environ
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, json
from marshmallow.exceptions import ValidationError
from mongoengine import connect
from werkzeug.exceptions import HTTPException

from app import auth, core

# 加载环境变量
load_dotenv()

# 连接数据库
connect(host=environ["MONGODB_HOST"])


def create_app():
    app = Flask(__name__, root_path=Path(__file__).parent.parent)

    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(core.views.blueprint)

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
