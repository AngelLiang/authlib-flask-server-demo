# coding=utf-8

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.compat import iteritems
from wtforms.validators import DataRequired


class OAuth2ClientForm(FlaskForm):
    """for authlib.flask.oauth2.sqla.OAuth2ClientMixin"""
    client_name = StringField(
        label='client_name',  default='remote')
    client_uri = StringField(
        label='client_uri', default='http://127.0.0.1:8000/')
    allowed_scope = StringField(
        label='allowed_scope', default='profile')
    redirect_uris = TextAreaField(
        label='redirect_uris', default='http://127.0.0.1:8000/auth')
    allowed_grant_types = TextAreaField(
        'allowed_grant_types', default='authorization_code')
    allowed_response_types = TextAreaField(
        label='grant_types', default='code')
    token_endpoint_auth_method = SelectField(
        label='token_endpoint_auth_method',
        choices=[
            ('client_secret_basic',
             'client_secret_basic'),
            ('client_secret_post',
             'client_secret_post'),
            ('none', 'none')
        ],
        default='client_secret_basic')


class OAuth2ClientForm2(FlaskForm):
    """for authlib.integrations.sqla_oauth2.OAuth2ClientMixin"""
    client_name = StringField(
        label='client_name',  default='remote')
    client_uri = StringField(
        label='client_uri', default='http://127.0.0.1:8000/')
    scope = StringField(
        label='scope', default='profile')
    redirect_uris = TextAreaField(
        label='redirect_uris', default='http://127.0.0.1:8000/auth')
    grant_types = TextAreaField(
        'grant_types', default='authorization_code')
    response_types = TextAreaField(
        label='response_types', default='code')
    token_endpoint_auth_method = SelectField(
        label='token_endpoint_auth_method',
        choices=[
            ('client_secret_basic',
             'client_secret_basic'),
            ('client_secret_post',
             'client_secret_post'),
            ('none', 'none')
        ],
        default='client_secret_basic')

    def populate_obj(self, obj):
        data = self.data
        if 'csrf_token' in data:
            del data['csrf_token']
        obj.set_client_metadata(data)
