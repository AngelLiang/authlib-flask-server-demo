# coding=utf-8

from flask import Blueprint, session, request, render_template, redirect

from app.extensions import db
from app.models import User, OAuth2Client
from app.views.utils import current_user, login_user,logout_user

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
        login_user(user)
        return redirect('/admin')
    user = current_user()
    if user:
        # 获取该帐号的客户端
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []
    print(session)
    return render_template('home.html', user=user, clients=clients)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
