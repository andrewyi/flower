# coding: utf-8
'''
app.tests.views
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

from . import tests
from . import forms

from .. import csrf
from ..accessory.auth_util import check_auth


@tests.route('/ep')
@check_auth
def test_endopint():
    return request.endpoint


@tests.route('/test_abort')
@csrf.exempt
def test_abort():
    code = request.args.get('code')
    try:
        code = int(code)
    except:
        code = 400

    import time
    # time.sleep(3)

    if code >= 400:
        current_app.logger.info('gonna abort(%s).', code)
        abort(code)
    else:
        return make_response('return with code', code)

    return 'ok'


@tests.errorhandler(400)
def invalid_params_handler(e):
    return make_response(jsonify(code=400, message='访问参数有误'), 200)


@tests.route('/form', methods=['POST'])
@csrf.exempt
def form_parameters():
    form = forms.ParamForm()
    # form.csrf_enabled = False

    if not form.validate_on_submit():
        current_app.logger.error(
                'form.validate_on_submit failed, error: %s.', form.errors)
    var1 = form.var1.data
    current_app.logger.info('get var1: %s.', var1)

    return 'form'


@tests.route('/post', methods=['POST'])
@csrf.exempt
def post_parameters():
    var1 = request.form.get('var1')
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))
    return 'post'


@tests.route('/get')
def get_parameters():
    var1 = request.args.get('var1')
    current_app.logger.info('----> var1: %s.', var1)
    current_app.logger.info('----> typeof var1: %s.', type(var1))
    return 'get'


@tests.route('/echo')
def do_echo():
    q = request.args.get('q')
    current_app.logger.info('get q: %s.', q)
    # return q
    return jsonify(echo=q)


@tests.route('/exception')
def raise_exp():
    e = request.args.get('e')
    current_app.logger.info('get e: %s.', e)
    raise Exception(e)
    return ''

class T(object):
    def __init__(self, v):
        self.v = v

@tests.route('/render')
def render():
    # args = {'test_key':'test_value'}
    t = T('test args ..........')
    return render_template('tests/index.html', args=t)

@jinja2.contextfilter
@tests.app_template_filter()
def cvalue(context, t):
    return ('cvalue converted input: %s' % (t.v,))

@tests.app_context_processor
def fvalue_wrapper():
    def fvalue(t):
        return ('fvalue converted input: %s' % (t.v,))
    return dict(fvalue=fvalue)
