# coding: utf-8
'''
app.jsl.views
------------------

'''

import jinja2
from flask import (
    current_app,
    request,
    make_response,
    abort,
    jsonify,
    render_template,
)

from . import jsl

from .. import csrf
from ..accessory.auth_util import check_auth

@jsl.route('/')
@check_auth
def gen():
    response = make_response('ok')
    response.set_cookie('test_cookie_name', 'test_cookie_value', path='/')
    return response

@jsl.route('/index')
@check_auth
def test_endopint():
    # response = make_response(render_template('jsl/index.html'))
    response = make_response('ok')
    # response.set_cookie('test_cookie_name', 'test_cookie_value2', path='/')
    return response
    # return render_template('jsl/index.html')

@jsl.route('/index/2')
@check_auth
def test_endopint2():
    return 'ok' 


@jsl.route('/backspace')
def test_backspace():
    return render_template('jsl/backspace.html')


@jsl.route('/filter')
def test_filter():
    # abort(501)
    from ..accessory.facilities import TestException
    raise TestException('caoni')
    return render_template('jsl/filter.html')

@jsl.route('/dw')
def test_dw():
    return render_template(
            'jsl/dw.html',
            # s='''<script>console.log('caonima?');<\/script>'''
            s='''<script type='text/javascript' src='/jsl/sleep_script'><\/script>'''
            )

@jsl.route('/sleep_script')
def test_script():
    import time
    time.sleep(3)
    return '''console.log('caonima sleeping?')'''

