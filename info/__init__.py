from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, g
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from redis import StrictRedis
from config import config
import logging

# 初始化数据库
# 在flask中

db = SQLAlchemy()
redis_store = None   # type: StrictRedis


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL) # 调试debug级
    # 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式，日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象 （flask app使用的） 添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """
    通过传入不同的配置名字，初始化其对应配置的应用实例
    :param config_name:  配置名字
    :return: app
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 配置数据库
    db.init_app(app)

    # 配置redis
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_POST, decode_responses=True)

    # 开启当前项目CSRF保护,只做服务器验证功能
    # 帮我们做了：从cookie中抽取出随机值，从表单中取出随机值，然后进行校验，并且响应校验结果
    # 我们需要做：1，在返回响应的时候，往cookie中添加一个csrf_token,。 2，并且在表单中添加一个隐藏的csrf_token
    # 而我们现在登录或者注册不是使用的表单，而是使用ajax请求，所以我们需要在ajax请求的时候带上 csrf_token 这个随机值
    CSRFProtect(app)

    # 设置session 保存指定位置
    Session(app)

    from info.utils.common import do_index_class
    # 添加自定义过滤器
    app.add_template_filter(do_index_class, "index_class")

    from info.utils.common import user_login_data
    @app.errorhandler(404)
    @user_login_data
    def page_not_fount(e):

        user = g.user
        data = {
            "user": user.to_dict() if user else None
        }

        return render_template('news/404.html', data=data)

    @app.after_request
    def after_request(response):
        # 生成随机的csrf_token值
        csrf_token = generate_csrf()
        # 设置一个cookie
        response.set_cookie('csrf_token', csrf_token)
        return response

    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    from info.modules.profile import profile_blu
    app.register_blueprint(profile_blu)

    from info.modules.admin import admin_blu
    app.register_blueprint(admin_blu, url_prefix="/admin")

    return app

