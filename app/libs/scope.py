

class ScopeBase:
    forbidden_api = []

    def __init__(self, obj):
        self.forbidden_api = self.forbidden_api + obj.forbidden_api


class UserScope(ScopeBase):
    forbidden_api = ['v1.user+super_delete_user',
                     'v1.user+super_get_user']

    def __init__(self):
        super(UserScope, self).__init__(AdminScope)


class AdminScope():
    forbidden_api = []


def is_in_scope(scope, endpoint):
    # 传进来的scope是一个字符串, 需要把它变成对象再实例化
    scope = globals()[scope]()
    if endpoint in scope.forbidden_api:
        return False
    else:
        return True
