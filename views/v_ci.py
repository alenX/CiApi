# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, jsonify, render_template
from models.model_user import User, Ci
import hashlib
import datetime
from ext import ci_redis, db as my_db
from ci_decorate import login_require

app = Flask(__name__)
ci_v = Blueprint('ci', __name__, template_folder='templates',url_prefix='/v1')


@ci_v.route('/ci/login', methods=['POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        username = request.form['username']
        password = request.form['password']
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
        ci_redis.hmset('user:%s' % user.mobile, {'token': token, 'username': username})
        ci_redis.set('token:%s' % token, user.mobile)
        # ci_redis.expire('token:%s' % token, 3600)
        return jsonify({'code': 1, 'content': '登陆成功', 'mobile': user.mobile})
    else:
        return render_template('ci/index.html')


@ci_v.route('/ci/register', methods=['POST'])
def register():
    user = request.form['username']
    password = request.form['password']
    mobile = request.form['mobile']
    u = User()
    u.pwd = password
    u.username = user
    u.mobile = mobile
    my_db.session.add(u)
    my_db.session.commit()
    return jsonify({'code': 1, 'content': '注册成功!'})


@ci_v.route('/ci/register_view')
def register_view():
    return render_template('ci/register.html')


@ci_v.route('/ci/cis', methods=['GET'])
@login_require
def ci_cis():
    # if 'TOKEN' not in request.headers:
    #     return jsonify({'code': 0, 'content': '需要验证用户信息'})
    token = request.headers['token']
    # print(token)
    # if not token:
    #     return jsonify({'code': 0, 'content': '需要验证用户信息'})
    mobile = ci_redis.get('token:%s' % token)
    # if not mobile and token != ci_redis.hget('user:%s' % int(mobile), 'token'):
    #     return jsonify({'code': 0, 'content': '验证信息错误!'})
    username = ci_redis.hget('user:%s' % int(mobile), 'username')
    print(username)
    if username is None:
        return jsonify({'code': 1, 'content': '用户姓名错误!'})
    return jsonify({'code': 1, 'content': '登陆成功，用户名' + str(username)})


@ci_v.route('/ci/<int:ci_id>')
@login_require
def ci_ci(ci_id):
    # cis = [{'id': 1, 'title': '定风波', 'author': '苏轼'}, {'id': 2, 'title': '卜算子', 'author': '陆游'}]
    # try:
    #     ci = filter(lambda x: x['id'] == id, cis)
    #     return jsonify(next(ci))
    # except StopIteration as e:
    #     return jsonify({'code': 0, 'content': '不存在该记录'})
    ci = Ci.query.filter_by(id=ci_id).first()
    if not ci or Ci is None:
        return jsonify({'code': 0, 'content': '不存在该记录'})
    else:
        ci_dict = ci.__dict__
        ci_dict.pop('_sa_instance_state')
        for key, value in ci.__dict__.items():
            print(key)
        return jsonify(ci_dict)