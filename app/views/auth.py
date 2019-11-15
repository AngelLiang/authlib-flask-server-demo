# coding=utf-8

from flask import Blueprint, session, request, render_template, redirect

from app.extensions import db
from app.models import User, OAuth2Client
from app.views.utils import current_user

auth_bp = Blueprint(__name__, 'auth_bp')


@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        # 创建一个帐号
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect('/')
    user = current_user()
    if user:
        # 获取该帐号的客户端
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []
    return render_template('home.html', user=user, clients=clients)
