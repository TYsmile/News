# 个人中心的相关业务逻辑都放在当前模块中

from flask import Blueprint

# 创建蓝图对象
profile_blu = Blueprint('profile', __name__, url_prefix='/user')

from . import views