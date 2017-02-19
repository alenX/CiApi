# -*- coding: utf-8 -*-
from flask import Flask
from ext import db as my_db
from views.v_ci import ci_v

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def create_app():
    app.config.from_object('config')
    my_db.init_app(app)
    app.register_blueprint(ci_v)
    with app.app_context():
        my_db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()


@app.teardown_request
def handle_teardown_request(exception):
    my_db.session.remove()
