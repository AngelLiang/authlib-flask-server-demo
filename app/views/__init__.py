# coding=utf-8

from app.views.auth import auth_bp
from app.views.oauth import oauth_bp


def register_views(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(oauth_bp)
