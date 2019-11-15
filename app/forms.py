# coding=utf-8

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class OAuth2ClientForm(FlaskForm):
    client_name = StringField(
        label='client_name',  default='client')
    client_uri = StringField(
        label='client_uri', default='http://127.0.0.1:8000/')
    allowed_scope = StringField(
        label='allowed_scope', default='profile')
    redirect_uris = TextAreaField(
        label='redirect_uris', default='http://127.0.0.1:8000/auth')
    allowed_grant_types = TextAreaField(
        'allowed_grant_types', default='authorization_code')
    allowed_response_types = TextAreaField(
        label='allowed_response_types', default='code')
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
