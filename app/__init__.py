import os
import logging

from flask import Flask
from flask.ext.session import Session
from flask_wtf.csrf import CsrfProtect
from flask.ext.redis import FlaskRedis

import config


session = Session()
csrf = CsrfProtect()
redis = FlaskRedis()


def create_app(env):
    app = Flask(__name__)

    conf = config.of_env(env)
    conf.init_app(app)
    app.config.from_object(conf)

    init_logging(app)

    session.init_app(app)
    csrf.init_app(app)
    redis.init_app(app)

    from .main import main as blueprint_main
    app.register_blueprint(blueprint_main, url_prefix='/')

    from .tests import tests as blueprint_tests
    app.register_blueprint(blueprint_tests, url_prefix='/tests')

    from flask_wtf.csrf import generate_csrf
    @app.after_request
    def set_xsrf_cookie(resp):
        max_age = app.config.get('WTF_CSRF_TIME_LIMIT', 3600)
        resp.set_cookie('our-csrftoken', generate_csrf(), max_age=max_age)
        return resp

    return app


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def init_logging(app):
    log_path = os.path.join(basedir, 'log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_file = os.path.join(log_path, 'app.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d]: %(message)s'))

    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
