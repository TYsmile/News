from redis import StrictRedis


class Config(object):
    """项目配置"""
    # DEBUG = True

    SECRET_KEY = 'tCDMlA0Q97pIi0dE9d0azpGI0cYnPn+pWLPaGUei6QnLzIFKkW3VTNVady+/0ZY1'

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:你的仓库名@127.0.0.1:3306/数据库名"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 在请求结束时，如果指定此配置为 True， 那么 SQLAlchemy 会自动执行一次 db.session.commit()操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis 配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379

    # Session保存配置
    SESSION_TYPE = 'redis'
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 指定 Session 保存的 redis
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_POST)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2


class DevelopmentConfig(Config):
    """开发环境下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境下的配置"""
    DEBUG = False
    # 生产环境下的数据库配置
    # SQLALCHEMY_DATABASE_URI = "mysql://root:weixiao@192.168.1.104:3306/information27"


class TestingConfig(Config):
    """单元测试环境下的配置"""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
