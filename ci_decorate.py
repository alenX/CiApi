# -*- coding: utf-8 -*-
from flask import request, Flask, jsonify
from ext import ci_redis
from functools import wraps

app = Flask(__name__)


def login_require(func):
    @wraps(func)
    def decr(*args, **kwargs):
        if 'TOKEN' not in request.headers:
            return jsonify({'code': 0, 'content': '需要验证用户信息'})
        token = request.headers['token']
        print(token)
        if not token:
            return jsonify({'code': 0, 'content': '需要验证用户信息'})
        mobile = ci_redis.get('token:%s' % token)
        if not mobile and token != ci_redis.hget('user:%s' % int(mobile), 'token'):
            return jsonify({'code': 0, 'content': '验证信息错误!'})
        return func(*args, **kwargs)
    return decr