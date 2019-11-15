# coding=utf-8

from flask import Blueprint, session, jsonify, request, render_template, current_app
from authlib.flask.oauth2 import current_token
from authlib.oauth2 import OAuth2Error

from app.models import User
from app.oauth2 import authorization, require_oauth
from app.views.utils import current_user


oauth_bp = Blueprint(__name__, 'oauth_bp')


@oauth_bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """"认证页面"""
    user = current_user()
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            current_app.logger.debug(error)
            return error.error
        current_app.logger.debug(f'user:{user}')
        current_app.logger.debug(f'grant:{grant}')
        return render_template('authorize.html', user=user, grant=grant)

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None

    return authorization.create_authorization_response(grant_user=grant_user)


@oauth_bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@oauth_bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@oauth_bp.route('/api/me')
@require_oauth()
def api_me():
    user = current_token.user
    return jsonify(username=user.username)


@oauth_bp.route('/api/profile')
@require_oauth('profile')
def profile():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)
