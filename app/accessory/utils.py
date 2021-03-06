# coding: utf-8

import random
import string

from flask import request


def to_int(o, d=0):
    if o is None:
        return d
    try:
        i = int(o)
    except (TypeError, ValueError):
        return d
    return i


def make_random_str(length):
    letters = string.ascii_letters
    return ''.join([random.choice(letters) for i in range(length)])


def format_date(d):
    if not d:
        return None

    return d.strftime('%Y-%m-%d')


def format_datetime(d):
    if not d:
        return None

    return d.strftime('%Y-%m-%d %H:%M:%S')


def get_remote_addr():
    if request.access_route:
        return request.access_route[0]
    else:
        return request.remote_addr or '127.0.0.1'
