from flask import g, jsonify

from app import db
from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

api = Redprint('user')


# 被auth装饰器保护的视图函数, 需要auth.verify_password装饰器验证通过后才会回调该函数
@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.get_or_404(uid)
    return jsonify(user)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.get_or_404(uid)
        user.delete()
    return DeleteSuccess()


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    with db.auto_commit():
        user = User.query.get_or_404(uid)
        user.delete()
    return DeleteSuccess()
