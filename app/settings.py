# coding=utf-8

import os
import sys

from dotenv import load_dotenv


BASEDIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)

dotenv_path = os.path.join(BASEDIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

# SQLite URI compatible
WIN = sys.platform.startswith("win")
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


def os_getenv2bool(key, default='true'):
    if not isinstance(default, str):
        default = str(default)
    return os.getenv(key, default).lower() in ('1', 'yes', 'true')


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or \
        'hard to guess string and longer than 32 byte!'

    @classmethod
    def init_app(cls, app):
        pass


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        prefix + os.path.join(BASEDIR, 'data-dev.db')
    )


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        prefix + os.path.join(BASEDIR, 'data.db')
    )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
