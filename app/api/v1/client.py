from flask import request
from app.libs.enums import ClientTypeEnum
from app.libs.error import APIException
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')


@api.route('/test', methods=['GET'])
def test():
    1/0
    return Success


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm(data=request.json)
    form.validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm(data=request.json)
    form.validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)





