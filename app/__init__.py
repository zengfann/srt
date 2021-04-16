from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
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

    return app
