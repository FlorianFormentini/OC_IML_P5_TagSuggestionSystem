import os

basedir = os.getcwd()


class Config(object):
    """Base config"""
    DEBUG = False
    TESTING = False

    # API
    API_KEY = os.getenv('API_KEY')
    RESTX_MASK_SWAGGER = True
    ERROR_404_HELP = False  # disable complementary error message when 404

    # Tag suggestion
    VECT_PATH = './static/model.h5'
    MODEL_PATH = './static/model.h5'


class DevelopmentConfig(Config):
    """Uses local database server and display debug"""
    DEBUG = True


class ProductionConfig(Config):
    """Uses production database server"""
    DEBUG = False


class TestingConfig(Config):
    """Unit tests configuration"""
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    API_KEY = os.getenv('API_KEY', 'test_apikey')


config_by_name = {
    'dev': DevelopmentConfig,
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'tests': TestingConfig,
    'prod': ProductionConfig,
    'production': ProductionConfig,
}
