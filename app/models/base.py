"""
    定义模型(数据库模型)
    业务的本质就是记录一些数据,使用这些数据
    所以需要把这些数据抽象成一个类,方便保存和使用
"""
# 可以给导入的类设置一个别名,这样我们自己写的类就可以使用这个类名了
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager


# 通过继承SQLAlchemy定义自己的类,增加自己写的方法
#
from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield  # 这个yield会让程序跳出去执行with里面的语句,执行完后会跳回来执行下面的语句
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


# 重写SQLAlchemy中的filter_by对象,让其默认查询status数据
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1  # 这里的意思是在传入的参数里增加一个参数,就是增加了status=1的条件
        return super(Query, self).filter_by(**kwargs)

    # 重写get_or_404和first_or_404,使其返回的错误类型为APIException
    def get_or_404(self, ident, description=None, error_obj=None):
        rv = self.get(ident)
        if rv is None:
            raise error_obj() or NotFound()
        return rv

    def first_or_404(self, description=None, error_obj=None):
        rv = self.first()
        if rv is None:
            raise error_obj() or NotFound()
        return rv


# SQLAlchemy预留的接口让你可以改变query类
db = SQLAlchemy(query_class=Query)  # 创建数据库对象实例


# 定义user,wish,gift 的基类
class Base(db.Model):
    __abstract__ = True  # 继承Model类程序会自动创建数据库, 设置此函数不创建数据库实例
    # 基类默认添加create_time和status
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # keys和__getitem__函数用来实现序列化model对象, dict()方法会调用这两个方法
    def keys(self):
        # 返回要被序列化的变量的键
        return ['nickname', 'email']

    def __getitem__(self, item):
        return getattr(self, item)

    # 把dict格式的数据写入到model类的方法
    def set_attrs(self, attrs_dict):
        for key, val in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, val)
            # if key == 'password':
            #     self.password(val)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0


