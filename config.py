class Config(object):
    DEBUG = False
    TESTING = False

    APP_SESSION_SK = 'mjePmctHGDjbaBYGbk7'
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = APP_SESSION_SK
    TEMPLATES_AUTO_RELOAD = True

    VERSION = 'v1'
    API_BASE_URI = '/api/%s' % VERSION


class ProductionConfig(Config):
    PSQL_DBNAME = 'rrnvpnc'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = ''
    PSQL_HOST = '127.0.0.1'


class DevelopmentConfig(Config):
    DEBUG = True

    PSQL_DBNAME = 'rrnvpnc'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = 'railroadman'
    PSQL_HOST = '127.0.0.1'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
