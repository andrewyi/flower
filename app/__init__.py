import os
import logging
from datetime import datetime

import json_log_formatter

from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CsrfProtect
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

import config


session = Session()
csrf = CsrfProtect()
redis = FlaskRedis()
login_manager = LoginManager()
limiter = Limiter(key_func=get_ipaddr)


def create_app(env):
    app = Flask(__name__)

    conf = config.of_env(env)
    conf.init_app(app)
    app.config.from_object(conf)

    init_logging(app)

    session.init_app(app)
    csrf.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    from .main import main as blueprint_main
    app.register_blueprint(blueprint_main)

    from .tests import tests as blueprint_tests
    app.register_blueprint(blueprint_tests, url_prefix='/tests')

    from .jsl import jsl as blueprint_jsl
    app.register_blueprint(blueprint_jsl, url_prefix='/jsl')

    from .upload import upload as blueprint_upload
    app.register_blueprint(blueprint_upload, url_prefix='/upload')

    from .block_test import block_test as blueprint_block_test
    app.register_blueprint(blueprint_block_test, url_prefix='/block_test')

    from flask_wtf.csrf import generate_csrf
    @app.after_request
    def set_xsrf_cookie(resp):
        max_age = app.config.get('WTF_CSRF_TIME_LIMIT', 3600)
        resp.set_cookie('our-csrftoken', generate_csrf(), max_age=max_age)
        return resp

    from .accessory.facilities import app_func
    app.context_processor(app_func)


    '''
    @app.errorhandler(500)
    def error_handler(error):
        from flask import current_app
        current_app.logger.error('----error is : %s, %s.', error, type(error))
        return 'error_handler for 500'
    '''

    return app


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['message'] = message
        extra['@timestamp'] = datetime.utcnow().isoformat()[:-3] + 'Z'
        extra['logger'] = record.name
        extra['level'] = record.levelname
        extra['filename'] = record.filename
        extra['lineno'] = record.lineno
        extra['func'] = record.funcName
        extra['pid'] = record.process
        extra['process'] = record.processName
        if record.exc_info:
            extra['exception'] = self.formatException(record.exc_info)
        return extra

    def mutate_json_record(self, json_record):
        return json_record

def init_logging(app):
    formatter = JSONFormatter()
    log_handler = logging.StreamHandler() 
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
