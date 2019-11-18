# coding=utf-8

import time
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin, OAuth2AuthorizationCodeMixin, OAuth2TokenMixin
)

from app.extensions import db


__all__ = ('User', 'OAuth2Client', 'OAuth2Token', 'OAuth2AuthorizationCode')


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel):
    username = db.Column(db.String(40), unique=True)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return password == 'password'


class OAuth2Client(BaseModel, OAuth2ClientMixin):
    """OAuth2客户端"""
    __tablename__ = 'oauth2_client'

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(BaseModel, OAuth2TokenMixin):
    """OAuth2 token"""
    __tablename__ = 'oauth2_token'

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2AuthorizationCode(BaseModel, OAuth2AuthorizationCodeMixin):
    """OAuth2认证码"""
    __tablename__ = 'oauth2_code'

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
