from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from sqlalchemy.util import namedtuple

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope
from app.models.user import User

auth = HTTPBasicAuth()
User_np = namedtuple('User', ['uid', 'ac_type', 'scope'])


# 校验token, 校验成功后会回调被auth装饰器保护的视图函数
# HTTP Basic Auth是http的一种基本认证协议, 传参需要把数据使用base64加密后再使用request请求头传参
@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    # 查询一下注册token的账号是否被删除
    User.query.filter_by(id=user_info.uid).first_or_404(error_obj=AuthFailed)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


# 校验并提取token中的数据
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg="token is invalid", error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg="token is expired", error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    in_scope = is_in_scope(scope, request.endpoint)
    if not in_scope:
        raise Forbidden()
    return User_np(uid, ac_type, scope)


