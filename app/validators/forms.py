from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.error_code import ClientTypeError
from app.validators.base import BaseForm
from app.libs.enums import ClientTypeEnum
from app.models.user import User


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    # 函数名加了validate_后,wtform会自动验证字段,并且value会自动赋值为字段的值
    def validate_type(self, value):
        try:
            type = ClientTypeEnum(value.data)
            self.type.data = type
        except ValueError:
            raise ClientTypeError()


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message="invalidate email")
    ])
    secret = StringField(validators=[
        DataRequired(),
        Regexp("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$")
    ])
    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)
    ])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="该账号已创建")


