# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, jsonify
from models.model_user import User
import hashlib, datetime
from ext import ci_redis, db as my_db

app = Flask(__name__)
ci_v = Blueprint('ci', __name__, template_folder='templates')


@ci_v.route('/ci/login', methods=['post', 'get'])
def login():
    mobile = request.args['mobile']
    username = request.args['username']
    password = request.args['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'code': 0, 'content': '不存在该用户'})

    if not user.check_password_hash(password=password):
        return jsonify({'code': 0, 'content': '密码错误！'})

    m = hashlib.md5()
    m.update(str(mobile).encode('utf-8'))
    m.update(str(password).encode('utf-8'))
    m.update(str(datetime.datetime.now()).encode('utf-8'))
    token = m.hexdigest()
    ci_redis.hmset('user:%s' % user.mobile, {'token': token})
    ci_redis.set('token:%s' % token, user.mobile)
    ci_redis.expire('token:%s' % token, 3600)
    return jsonify({'code': 1, 'content': '登陆成功', 'mobile': user.mobile})


@ci_v.route('/ci/register', methods=['post', 'get'])
def register():
    user = request.args['user']
    password = request.args['password']
    u = User()
    u.pwd = password
    u.username = user
    my_db.session.add(u)
    my_db.session.commit()
    return jsonify({'code': 1, 'content': '注册成功!'})
