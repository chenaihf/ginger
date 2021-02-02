"""
    自定义一个红图类(视图函数级别)
    1.红图可以通过蓝图的add_url_rule函数实现为视图函数添加路由
    2.再按需求实现url_perfix的功能,实现视图函数级别的"蓝图"
    重点: 添加路由实际是使用blueprint下的add_url_rule函数
"""


class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        for f, rule, options in self.mound:
            endpoint = self.name + '+' + options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
