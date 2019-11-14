# coding=utf-8

# from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView

from app.extensions import db
from app.models import User, OAuth2Client, OAuth2Token, OAuth2AuthorizationCode


class UserModelView(ModelView):
    pass


class OAuth2ClientModelView(ModelView):
    pass


class OAuth2TokenModelView(ModelView):
    pass


class OAuth2AuthorizationCodeModelView(ModelView):
    pass


def init_admin(admin):
    admin.add_view(OAuth2ClientModelView(
        User, db.session, name='User'))
    admin.add_view(OAuth2ClientModelView(
        OAuth2Client, db.session, name='OAuth2Client'))
    admin.add_view(OAuth2TokenModelView(
        OAuth2Token, db.session, name='OAuth2Token'))
    admin.add_view(OAuth2AuthorizationCodeModelView(
        OAuth2AuthorizationCode, db.session, name='OAuth2AuthorizationCode'))
