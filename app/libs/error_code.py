from werkzeug.exceptions import HTTPException

from app.libs.error import APIException


# 借助APIException实现调用成功返回json格式数据


class Success(APIException):
    code = 201
    error_code = 1
    msg = "ok"


class DeleteSuccess(APIException):
    code = 202
    error_code = -1
    msg = "ok"


class ServerError(APIException):
    code = 500
    msg = "内部错误 — 因为意外情况，服务器不能完成请求"
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    error_code = 1006
    msg = "ClientType parma invalid"


class ParameterError(APIException):
    code = 400
    error_code = 1000
    msg = "Invalid parameter"


class NotFound(APIException):
    code = 404
    error_code = 1001
    msg = 'Resource not found'


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'Authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1009
    msg = "insufficient privilege"

