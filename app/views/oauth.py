# coding=utf-8

from flask import Blueprint, session, jsonify, request, render_template, current_app, redirect
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error

from app.models import User
from app.oauth2 import authorization, require_oauth
from app.views.utils import current_user, login_user


oauth_bp = Blueprint(__name__, 'oauth_bp')


@oauth_bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """"认证页面"""
    print(session)
    user = current_user()

    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            current_app.logger.debug(error)
            return error.error
        # return authorization.create_authorization_response(grant_user=user)
        return render_template('authorize.html', user=user, grant=grant)
    if request.method == 'POST' and user is None:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return redirect(request.url)
        login_user(user)

    grant_user = user

    return authorization.create_authorization_response(grant_user=grant_user)


@oauth_bp.route('/oauth/token', methods=['POST'])
def issue_token():
    """发布token

    http://127.0.0.1:5000/oauth/token
    """
    return authorization.create_token_response()


@oauth_bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    """撤销token

    http://127.0.0.1:5000/oauth/revoke
    """
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
