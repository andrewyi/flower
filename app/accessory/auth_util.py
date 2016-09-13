#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from flask import (
        abort,
        current_app,
        request
        )

from .. import redis
from flask_login import current_user

def check_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_app.logger.error('in check auth, endpoint: %s, current user: %s.', request.endpoint, current_user)
        return f(*args, **kwargs)
    return wrapper
