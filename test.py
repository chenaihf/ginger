

class User:
    name = 'gg'
    age = 12

    def keys(self):
        return ['name', 'age']

    def __getitem__(self, item):
        return getattr(self, item)


gg = User()
d = dict(gg)
print(d)

print('' == None)

