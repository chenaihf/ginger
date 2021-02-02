"""
    封装的错误类, 实现自己的错误返回数据(json格式)
"""
from flask import json, request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "内部错误 — 因为意外情况，服务器不能完成请求"
    error_code = 999

    def __init__(self, code=None, msg=None, error_code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json")]

    @staticmethod
    def get_url_no_param():
        full_path = request.full_path
        main_path = full_path.split('?')
        return main_path[0]

