# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import redis
ci_redis = redis.Redis(host='localhost', port=6379, db=1)
db = SQLAlchemy()