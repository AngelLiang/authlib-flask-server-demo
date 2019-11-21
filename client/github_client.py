# coding=utf-8
"""
doc: https://developer.github.com/apps/building-github-apps/identifying-and-authorizing-users-for-github-apps/
"""
import os
from flask import Flask, url_for, session, current_app, jsonify
from flask import redirect, render_template_string
from authlib.integrations.flask_client import OAuth
from authlib.specs.rfc6749 import OAuth2Token

from dotenv import load_dotenv
if os.path.exists('.env'):
    load_dotenv('.env', override=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

TOKEN_KEY = 'github_token'

app = Flask(__name__)
app.secret_key = '!secret'


def fetch_token(name):
    return OAuth2Token(params=session[TOKEN_KEY])


oauth = OAuth(app, fetch_token=fetch_token)
oauth.register(
    name='github',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/resource',  # 资源服务器url
    client_kwargs={'scope': 'email'},
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
    current_app.logger.debug(session)
    user = session.get('user')
    current_app.logger.debug(user)
    return render_template_string(home, user=user)


@app.route('/login')
def login():
    """登录"""
    redirect_uri = url_for('auth', _external=True)
    current_app.logger.debug(redirect_uri)
    return oauth.github.authorize_redirect(redirect_uri=redirect_uri)


@app.route('/auth')
def auth():
    """客户端处理认证"""
    # 获取 access token
    token = oauth.github.authorize_access_token()
    user = oauth.github.parse_id_token(token)
    session['user'] = user
    current_app.logger.debug(f'user:{user}')
    current_app.logger.debug(f'token:{token}')
    if token:
        session[TOKEN_KEY] = token
    return token


@app.route('/profile')
def profile():
    current_app.logger.debug(session)
    if TOKEN_KEY in session:
        resp = oauth.github.get('/user/profile')
        return jsonify(resp.json())
    return redirect('/')


@app.route('/email')
def email():
    current_app.logger.debug(session)
    if TOKEN_KEY in session:
        resp = oauth.github.get('/user/emails')
        return jsonify(resp.json())
    return redirect('/')


@app.route('/public_emails')
def public_emails():
    current_app.logger.debug(session)
    if TOKEN_KEY in session:
        resp = oauth.github.get('/user/public_emails')
        return jsonify(resp.json())
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(port=9000, debug=True)
