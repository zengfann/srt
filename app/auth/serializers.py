from marshmallow import Schema, fields, post_load, validate

from .models import User


class UserSerializer(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^[a-zA-Z_0-9]{3,}$",
            error="用户名只能包括字母,数字和下划线,最小长度为3个字符",
        ),
    )
    password = fields.Str(required=True, load_only=True)
    email = fields.Email(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSerializer()
users_schema = UserSerializer(many=True)
