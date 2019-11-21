# coding=utf-8
import os
from flask import Flask, url_for, session, current_app, jsonify, request
from flask import redirect, render_template_string
from authlib.integrations.flask_client import OAuth
from authlib.oauth2.rfc6749 import OAuth2Token
from authlib.integrations._client import OAuthError

from dotenv import load_dotenv
if os.path.exists('.env'):
    load_dotenv('.env', override=True)


CLIENT_ID = os.getenv('REMOTE2_CLIENT_ID')
CLIENT_SECRET = os.getenv('REMOTE2_CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = '!secret'
app.config.update({
    'SESSION_COOKIE_NAME': 'client2',
})


def fetch_token(name):
    return OAuth2Token(params=session['token'])


oauth = OAuth(fetch_token=fetch_token)
oauth.register(
    name='remote',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    request_token_url=None,
    access_token_url='http://127.0.0.1:5000/oauth/token',
    access_token_params=None,
    authorize_url='http://127.0.0.1:5000/oauth/authorize',
    authorize_params=None,
    api_base_url='http://127.0.0.1:5000/api/',  # 资源服务器url
    client_kwargs={'scope': 'profile'},
)

home = """
{% if user %}
<pre>
{{ user|tojson }}
</pre>
<a href="/logout">logout</a>
{% else %}
<a href="/login">login</a>
{% endif %}
"""


@app.route('/')
def homepage():
    session['host'] = request.url
    current_app.logger.debug(session)
    user = session.get('user') or session.get('token')
    current_app.logger.debug(user)
    return render_template_string(home, user=user)


@app.route('/login')
def login():
    """登录"""
    current_app.logger.debug(session)
    redirect_uri = url_for('auth', _external=True)
    current_app.logger.debug(redirect_uri)
    return oauth.remote.authorize_redirect(redirect_uri=redirect_uri)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect('/')


@app.route('/auth')
def auth():
    """客户端处理认证"""
    try:
        # 获取 access token
        # code只能使用一次
        token = oauth.remote.authorize_access_token()
    except OAuthError as e:
        current_app.logger.info(e)
        return {'error': e.error, 'description': e.description}
    user = oauth.remote.parse_id_token(token)
    session['user'] = user
    current_app.logger.debug(f'user:{user}')
    current_app.logger.debug(f'token:{token}')
    if token:
        session['token'] = token
    current_app.logger.debug(session)
    return token


@app.route('/me')
def me():
    current_app.logger.debug(session)
    if 'token' in session:
        resp = oauth.remote.get('me')
        return jsonify(resp.json())
    return redirect('/')


@app.route('/profile')
def profile():
    current_app.logger.debug(session)
    if 'token' in session:
        resp = oauth.remote.get('profile')
        return jsonify(resp.json())
    return redirect('/')


if __name__ == "__main__":
    oauth.init_app(app)
    app.run(port=8001, debug=True)
