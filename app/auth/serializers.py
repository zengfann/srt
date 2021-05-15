from marshmallow import Schema, fields, post_load

from .models import User


class UserSerializer(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    user_type = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSerializer()
users_schema = UserSerializer(many=True)
