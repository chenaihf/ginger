"""
    配置文件
"""

DEBUG = True

# 数据库配置文件,使用init_app注册数据库对象时,init__app函数会在app.config配置文件中查找
# 参数(str): 数据库类型+数据库驱动://账户名:密码@端口/DB
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:haoge123@localhost:3306/ginger'

# hash yushu
# 加密密码: Flask（以及相关的扩展extension）需要进行加密
SECRET_KEY = 'efe683cc9465cc4632b3ee4251c6fc86'
