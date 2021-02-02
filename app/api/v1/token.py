from flask import request, current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm(data=request.json)
    form.validate_for_api()  # 自己写的校验函数, 作用:校验失败会抛出异常
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[form.type.data](
        form.account.data,
        form.secret.data
    )
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'], form.type.data,
                                scope=identity['scope'],
                                expiration=expiration)
    return jsonify(
        {'token': token.decode('utf-8')}
    ), 201


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
    生成token(令牌)函数
    :param uid: 用户id
    :param ac_type: 客户端类型
    :param scope: 用户权限
    :param expiration: 令牌有效时间
    :return: Serializer对象
    """
    # 先创建一个Serializer加密对象, 再写入信息到这个对象!!
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
