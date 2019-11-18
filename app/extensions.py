# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()

from app.views.admin import HomeView  # noqa
admin = Admin(index_view=HomeView())


def register_extensions(app):
    from app.views.admin import init_admin
    db.init_app(app)
    admin.init_app(app)
    init_admin(admin, app=app)
