import os
import logging
from datetime import datetime

import json_log_formatter

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

    from .accessory.facilities import app_func
    app.context_processor(app_func)

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
