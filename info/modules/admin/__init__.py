from flask import Blueprint, session, redirect, request, url_for

# 创建蓝图对象
admin_blu = Blueprint('admin', __name__)

from . import views


@admin_blu.before_request
def chech_admin():
    # 如果不是管理员，那么直接跳转到主页
    is_admin = session.get("is_admin", False)
    # 不是管理员，当前访问的url也不是管理登录页
    if not is_admin and not request.url.endswith(url_for('admin.login')):
        return redirect('/')