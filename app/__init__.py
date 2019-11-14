# coding=utf-8

import os
from flask import Flask

from app.settings import config
from app.extensions import register_extensions
from app.commands import register_commands


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    config_obj = config[config_name]
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    register_extensions(app)
    register_commands(app)

    return app
