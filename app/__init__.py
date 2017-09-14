# -*- python3 sources -*-

import logging

from flask import g, Flask
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
    app.register_blueprint(blueprint_main, subdomain='<subdomain>')

    from .upload import upload as blueprint_upload
    app.register_blueprint(blueprint_upload, url_prefix='/upload')
    app.register_blueprint(
            blueprint_upload, url_prefix='/upload', subdomain='<subdomain>')

    from .html_loading_blocking_test import html_loading_blocking_test \
            as blueprint_html_loading_blocking_test
    app.register_blueprint(
            blueprint_html_loading_blocking_test,
            url_prefix='/html_loading_blocking_test'
            )
    app.register_blueprint(
            blueprint_html_loading_blocking_test,
            url_prefix='/html_loading_blocking_test',
            subdomain='<subdomain>'
            )

    from .form import form as blueprint_form
    app.register_blueprint(blueprint_form, url_prefix='/form')
    app.register_blueprint(
            blueprint_form, url_prefix='/form', subdomain='<subdomain>')

    from .test_stuff import test_stuff as blueprint_test_stuff
    app.register_blueprint(blueprint_test_stuff, url_prefix='/test_stuff')
    app.register_blueprint(
            blueprint_test_stuff,
            url_prefix='/test_stuff',
            subdomain='<subdomain>'
            )

    @app.before_request
    def setup_globals():
        pass

    @app.after_request
    def set_xsrf_cookie(resp):
        from flask_wtf.csrf import generate_csrf
        max_age = app.config.get('WTF_CSRF_TIME_LIMIT', 3600)
        resp.set_cookie('our-csrftoken', generate_csrf(), max_age=max_age)
        return resp

    add_subdomain_support(app)

    return app


def init_logging(app):
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(pathname)s:%(lineno)s] - %(message)s'))
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    if app.debug:
        sa_logger = logging.getLogger('sqlalchemy.engine')
        sa_logger.setLevel(logging.INFO)
        sa_logger.addHandler(handler)


def add_subdomain_to_global(endpoint, values):
    if values:
        g.subdomain = values.pop('subdomain', None)
    else:
        g.subdomain = None


def add_subdomain_to_url_params(endpoint, values):
    if 'subdomain' in g and 'subdomain' not in values:
        values['subdomain'] = g.subdomain


def add_subdomain_support(app):
    app.url_value_preprocessor(add_subdomain_to_global)
    app.url_defaults(add_subdomain_to_url_params)
