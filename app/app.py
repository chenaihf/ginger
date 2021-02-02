from app.models.base import Base
from flask.json import JSONEncoder as _JSONEncoder


# 重写Flask的JSONEncoder对象, 实现通过Flask对象序列化自己的类
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, Base):
            return dict(o)
        return super().default(o)


