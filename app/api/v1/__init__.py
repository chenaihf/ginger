from flask import Blueprint
from app.api.v1 import user, book, client, token


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    user.api.register(bp_v1, url_prefix='/user')
    book.api.register(bp_v1, url_prefix='/book')
    client.api.register(bp_v1, url_prefix='/client')
    token.api.register(bp_v1, url_prefix='/token')
    return bp_v1
