# -*- coding: utf-8 -*-
from ext import db as my_db
from werkzeug.security import generate_password_hash, check_password_hash


class User(my_db.Model):
    __tablename__ = 'ci_users'
    id = my_db.Column(my_db.Integer, primary_key=True)
    username = my_db.Column(my_db.String(64), unique=True, index=True)
    password = my_db.Column(my_db.String(256))
    mobile = my_db.Column(my_db.String(32))
    login_count = my_db.Column(my_db.Integer, default=0)
    last_login_ip = my_db.Column(my_db.String(32), default='unknown')
    nickname = my_db.Column(my_db.String(64))

    # 不能读取
    @property
    def pwd(self):
        raise Exception("you cant read it")

    @pwd.setter
    def pwd(self, password):
        self.password = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

