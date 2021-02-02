from werkzeug.exceptions import HTTPException

from app import create_app
from app.app import JSONEncoder
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()
# 把Flask对象的json_encoder改成自己改写的JSONEncoder,实现重写功能
app.json_encoder = JSONEncoder


# 抛出的错误都会被app.errorhandler(Exception)捕获到这个函数中处理
# 错误统一出口
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return APIException(
            code=e.code,
            error_code=1007,
            msg=e.description
        )
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            return e


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
