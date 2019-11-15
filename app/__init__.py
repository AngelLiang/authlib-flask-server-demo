# coding=utf-8

import os
from flask import Flask

from app.settings import config
from app.extensions import register_extensions
from app.views import register_views
from app.commands import register_commands
from app.oauth2 import config_oauth

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    config_obj = config[config_name]
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    register_extensions(app)
    register_views(app)
    register_commands(app)
    config_oauth(app)

    return app
