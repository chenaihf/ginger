"""
    改写封装Form,实现校验失败抛出异常
"""
from wtforms import Form
from app.libs.error_code import ParameterError


class BaseForm(Form):
    def __init__(self, data):
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        valid = self.validate()
        if not valid:
            raise ParameterError(msg=self.errors)

