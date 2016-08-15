# coding: utf-8

import os
import logging
import redis


class ConfigurationError(Exception):
    pass


class Config:
    LOGGING_LEVEL = logging.INFO

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY',
                           'jsr0jrzq609r431qd8x8y1hbdbiadcyg')

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis.from_url(REDIS_URL)

    # SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SESSION_KEY_PREFIX = 'session:flower:'

    WTF_CSRF_TIME_LIMIT = 36000

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG


class TestConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
}


def of_env(env):
    return config.get(env, DevelopmentConfig)
