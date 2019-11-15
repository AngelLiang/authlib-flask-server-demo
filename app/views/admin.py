# coding=utf-8

# from flask_admin import BaseView
from werkzeug.security import gen_salt
from flask_admin.contrib.sqla import ModelView

from app.extensions import db
from app.models import User, OAuth2Client, OAuth2Token, OAuth2AuthorizationCode
from app.forms import OAuth2ClientForm
from app.views.utils import current_user


class UserModelView(ModelView):
    pass


class OAuth2ClientModelView(ModelView):

    # form_columns =  ('user', 'client_name', 'client_uri', 'redirect_uri','grant_type')

    def get_create_form(self):
        return OAuth2ClientForm

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.client_id = gen_salt(24)
            if model.token_endpoint_auth_method == 'none':
                model.client_secret = ''
            else:
                model.client_secret = gen_salt(48)
            user = current_user()
            if user:
                model.user_id = user.id


class OAuth2TokenModelView(ModelView):
    pass


class OAuth2AuthorizationCodeModelView(ModelView):
    pass


def init_admin(admin, app=None):
    admin.add_view(OAuth2ClientModelView(
        User, db.session, name='User'))
    admin.add_view(OAuth2ClientModelView(
        OAuth2Client, db.session, name='OAuth2Client'))
    admin.add_view(OAuth2TokenModelView(
        OAuth2Token, db.session, name='OAuth2Token'))
    admin.add_view(OAuth2AuthorizationCodeModelView(
        OAuth2AuthorizationCode, db.session, name='OAuth2AuthorizationCode'))
