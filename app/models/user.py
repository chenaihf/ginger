from datetime import datetime

from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24))
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    def keys(self):
        # 返回要被序列化的变量的键
        return ['nickname', 'email', 'id', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @classmethod
    def register_by_email(cls, nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @classmethod
    def verify(cls, email, password):
        user = User.query.filter_by(email=email).first_or_404()
        # 这里调用实例方法得用实例调用,不能用类调用
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
