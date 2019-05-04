import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    VK_API_VERSION = 5.95
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    OAUTH_CREDENTIALS = {
        'vk':{
            'key':os.environ.get('VK_KEY'),
            'secret':os.environ.get('VK_KEY')
        }
    }
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    OAUTH_CREDENTIALS = {
        'vk': {
            'key': os.environ.get('VK_KEY'),
            'secret': os.environ.get('VK_KEY')
        }
    }
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}