# coding=utf-8
import os
from flask import Flask, url_for, session, current_app, jsonify
from flask import redirect, render_template_string
from authlib.integrations.flask_client import OAuth
from authlib.specs.rfc6749 import OAuth2Token

from dotenv import load_dotenv
if os.path.exists('.env'):
    load_dotenv('.env', override=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = '!secret'
# app.config.update({
#     'REMOTE_CLIENT_ID': CLIENT_ID,
#     'REMOTE_CLIENT_SECRET': CLIENT_SECRET,
#     # 'REMOTE_AUTHORIZE_URL': 'http://127.0.0.1:5000/oauth/authorize',
#     # 'REMOTE_ACCESS_TOKEN_URL': 'http://127.0.0.1:5000/oauth/token'
# })


def fetch_token(name):
    return OAuth2Token(params=session['token'])


oauth = OAuth(app, fetch_token=fetch_token)
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
    current_app.logger.debug(session)
    # if 'token' in session:
    #     resp = oauth.remote.get('me')
    #     if resp.status >= 200 and resp.status <= 299:
    #         return jsonify(resp.data)
    #     return resp.data

    user = session.get('user')
    current_app.logger.debug(user)
    return render_template_string(home, user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    current_app.logger.debug(redirect_uri)
    return oauth.remote.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.remote.authorize_access_token()
    user = oauth.remote.parse_id_token(token)
    current_app.logger.debug(f'user:{user}')
    session['user'] = user
    current_app.logger.debug(f'token:{token}')
    if token:
        session['token'] = token
    return token


@app.route('/me')
def me():
    current_app.logger.debug(session)
    if 'token' in session:
        resp = oauth.remote.get('me')
        if resp.status_code >= 200 and resp.status_code <= 299:
            return jsonify(resp.json())
        return resp.text
    return redirect('/')


@app.route('/profile')
def profile():
    current_app.logger.debug(session)
    if 'token' in session:
        resp = oauth.remote.get('profile')
        return jsonify(resp.json())
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(port=8000, debug=True)
